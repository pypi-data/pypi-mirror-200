from typing import Any, Callable, Dict, IO, Iterable, Iterator, List, Optional, Tuple
import os
import gzip
import bz2
import lzma
import tarfile
import zipfile
import pathlib
import sys
import hashlib
import urllib
import requests
import contextlib

import warnings
import re
import itertools
from tqdm import tqdm
from urllib.parse import urlparse


# https://github.com/pytorch/vision/blob/main/torchvision/datasets/utils.py#L433
def download_and_extract_archive(
    url: str,
    download_root: str,
    extract_root: Optional[str] = None,
    filename: Optional[str] = None,
    md5: Optional[str] = None,
    remove_finished: bool = False,
) -> None:
    download_root = os.path.expanduser(download_root)
    if extract_root is None:
        extract_root = download_root
    if not filename:
        filename = os.path.basename(url)

    download_url(url, download_root, filename, md5)

    archive = os.path.join(download_root, filename)
    print(f"Extracting {archive} to {extract_root}")
    extract_archive(archive, extract_root, remove_finished)


# https://github.com/pytorch/vision/blob/main/torchvision/datasets/utils.py#L119
def download_url(
    url: str, root: str, filename: Optional[str] = None, md5: Optional[str] = None, max_redirect_hops: int = 3
) -> None:
    """Download a file from a url and place it in root.
    Args:
        url (str): URL to download file from
        root (str): Directory to place downloaded file in
        filename (str, optional): Name to save the file under. If None, use the basename of the URL
        md5 (str, optional): MD5 checksum of the download. If None, do not check
        max_redirect_hops (int, optional): Maximum number of redirect hops allowed
    """
    root = os.path.expanduser(root)
    if not filename:
        filename = os.path.basename(url)
    fpath = os.path.join(root, filename)

    os.makedirs(root, exist_ok=True)

    # check if file is already present locally
    if check_integrity(fpath, md5):
        print("Using downloaded and verified file: " + fpath)
        return

    if _is_remote_location_available():
        _download_file_from_remote_location(fpath, url)
    else:
        # expand redirect chain if needed
        url = _get_redirect_url(url, max_hops=max_redirect_hops)

        # check if file is located on Google Drive
        file_id = _get_google_drive_file_id(url)
        if file_id is not None:
            return download_file_from_google_drive(file_id, root, filename, md5)

        # download the file
        try:
            print("Downloading " + url + " to " + fpath)
            _urlretrieve(url, fpath)
        except (urllib.error.URLError, OSError) as e:  # type: ignore[attr-defined]
            if url[:5] == "https":
                url = url.replace("https:", "http:")
                print("Failed download. Trying https -> http instead. Downloading " + url + " to " + fpath)
                _urlretrieve(url, fpath)
            else:
                raise e

    # check integrity of downloaded file
    if not check_integrity(fpath, md5):
        raise RuntimeError("File not found or corrupted.")



# https://github.com/pytorch/vision/blob/main/torchvision/datasets/utils.py#L397
def extract_archive(from_path: str, to_path: Optional[str] = None, remove_finished: bool = False) -> str:
    """Extract an archive.
    The archive type and a possible compression is automatically detected from the file name. If the file is compressed
    but not an archive the call is dispatched to :func:`decompress`.
    Args:
        from_path (str): Path to the file to be extracted.
        to_path (str): Path to the directory the file will be extracted to. If omitted, the directory of the file is
            used.
        remove_finished (bool): If ``True``, remove the file after the extraction.
    Returns:
        (str): Path to the directory the file was extracted to.
    """
    if to_path is None:
        to_path = os.path.dirname(from_path)

    suffix, archive_type, compression = _detect_file_type(from_path)
    if not archive_type:
        return _decompress(
            from_path,
            os.path.join(to_path, os.path.basename(from_path).replace(suffix, "")),
            remove_finished=remove_finished,
        )

    # We don't need to check for a missing key here, since this was already done in _detect_file_type()
    extractor = _ARCHIVE_EXTRACTORS[archive_type]

    extractor(from_path, to_path, compression)
    if remove_finished:
        os.remove(from_path)

    return 


def _detect_file_type(file: str) -> Tuple[str, Optional[str], Optional[str]]:
    """Detect the archive type and/or compression of a file.
    Args:
        file (str): the filename
    Returns:
        (tuple): tuple of suffix, archive type, and compression
    Raises:
        RuntimeError: if file has no suffix or suffix is not supported
    """
    suffixes = pathlib.Path(file).suffixes
    if not suffixes:
        raise RuntimeError(
            f"File '{file}' has no suffixes that could be used to detect the archive type and compression."
        )
    suffix = suffixes[-1]

    # check if the suffix is a known alias
    if suffix in _FILE_TYPE_ALIASES:
        return (suffix, *_FILE_TYPE_ALIASES[suffix])

    # check if the suffix is an archive type
    if suffix in _ARCHIVE_EXTRACTORS:
        return suffix, suffix, None

    # check if the suffix is a compression
    if suffix in _COMPRESSED_FILE_OPENERS:
        # check for suffix hierarchy
        if len(suffixes) > 1:
            suffix2 = suffixes[-2]

            # check if the suffix2 is an archive type
            if suffix2 in _ARCHIVE_EXTRACTORS:
                return suffix2 + suffix, suffix2, suffix

        return suffix, None, suffix

    valid_suffixes = sorted(set(_FILE_TYPE_ALIASES) | set(_ARCHIVE_EXTRACTORS) | set(_COMPRESSED_FILE_OPENERS))
    raise RuntimeError(f"Unknown compression or archive type: '{suffix}'.\nKnown suffixes are: '{valid_suffixes}'.")




def _decompress(from_path: str, to_path: Optional[str] = None, remove_finished: bool = False) -> str:
    r"""Decompress a file.
    The compression is automatically detected from the file name.
    Args:
        from_path (str): Path to the file to be decompressed.
        to_path (str): Path to the decompressed file. If omitted, ``from_path`` without compression extension is used.
        remove_finished (bool): If ``True``, remove the file after the extraction.
    Returns:
        (str): Path to the decompressed file.
    """
    suffix, archive_type, compression = _detect_file_type(from_path)
    if not compression:
        raise RuntimeError(f"Couldn't detect a compression from suffix {suffix}.")

    if to_path is None:
        to_path = from_path.replace(suffix, archive_type if archive_type is not None else "")

    # We don't need to check for a missing key here, since this was already done in _detect_file_type()
    compressed_file_opener = _COMPRESSED_FILE_OPENERS[compression]

    with compressed_file_opener(from_path, "rb") as rfh, open(to_path, "wb") as wfh:
        wfh.write(rfh.read())

    if remove_finished:
        os.remove(from_path)

    return to_path


def _extract_tar(from_path: str, to_path: str, compression: Optional[str]) -> None:
    with tarfile.open(from_path, f"r:{compression[1:]}" if compression else "r") as tar:
        tar.extractall(to_path)

def _extract_zip(from_path: str, to_path: str, compression: Optional[str]) -> None:
    with zipfile.ZipFile(
        from_path, "r", compression=_ZIP_COMPRESSION_MAP[compression] if compression else zipfile.ZIP_STORED
    ) as zip:
        zip.extractall(to_path)



_ARCHIVE_EXTRACTORS: Dict[str, Callable[[str, str, Optional[str]], None]] = {
    ".tar": _extract_tar,
    ".zip": _extract_zip,
}
_COMPRESSED_FILE_OPENERS: Dict[str, Callable[..., IO]] = {
    ".bz2": bz2.open,
    ".gz": gzip.open,
    ".xz": lzma.open,
}
_FILE_TYPE_ALIASES: Dict[str, Tuple[Optional[str], Optional[str]]] = {
    ".tbz": (".tar", ".bz2"),
    ".tbz2": (".tar", ".bz2"),
    ".tgz": (".tar", ".gz"),
}

_ZIP_COMPRESSION_MAP: Dict[str, int] = {
    ".bz2": zipfile.ZIP_BZIP2,
    ".xz": zipfile.ZIP_LZMA,
}
USER_AGENT = "pytorch/vision"


def check_integrity(fpath: str, md5: Optional[str] = None) -> bool:
    if not os.path.isfile(fpath):
        return False
    if md5 is None:
        return True
    return check_md5(fpath, md5)



def calculate_md5(fpath: str, chunk_size: int = 1024 * 1024) -> str:
    # Setting the `usedforsecurity` flag does not change anything about the functionality, but indicates that we are
    # not using the MD5 checksum for cryptography. This enables its usage in restricted environments like FIPS. Without
    # it torchvision.datasets is unusable in these environments since we perform a MD5 check everywhere.
    if sys.version_info >= (3, 9):
        md5 = hashlib.md5(usedforsecurity=False)
    else:
        md5 = hashlib.md5()
    with open(fpath, "rb") as f:
        for chunk in iter(lambda: f.read(chunk_size), b""):
            md5.update(chunk)
    return md5.hexdigest()


def check_md5(fpath: str, md5: str, **kwargs: Any) -> bool:
    return md5 == calculate_md5(fpath, **kwargs)

def _is_remote_location_available() -> bool:
    return False

def _download_file_from_remote_location(fpath: str, url: str) -> None:
    pass


def _get_redirect_url(url: str, max_hops: int = 3) -> str:
    initial_url = url
    headers = {"Method": "HEAD", "User-Agent": USER_AGENT}

    for _ in range(max_hops + 1):
        with urllib.request.urlopen(urllib.request.Request(url, headers=headers)) as response:
            if response.url == url or response.url is None:
                return url

            url = response.url
    else:
        raise RecursionError(
            f"Request to {initial_url} exceeded {max_hops} redirects. The last redirect points to {url}."
        )


def download_file_from_google_drive(file_id: str, root: str, filename: Optional[str] = None, md5: Optional[str] = None):
    """Download a Google Drive file from  and place it in root.
    Args:
        file_id (str): id of file to be downloaded
        root (str): Directory to place downloaded file in
        filename (str, optional): Name to save the file under. If None, use the id of the file.
        md5 (str, optional): MD5 checksum of the download. If None, do not check
    """
    # Based on https://stackoverflow.com/questions/38511444/python-download-files-from-google-drive-using-url

    root = os.path.expanduser(root)
    if not filename:
        filename = file_id
    fpath = os.path.join(root, filename)

    os.makedirs(root, exist_ok=True)

    if check_integrity(fpath, md5):
        print(f"Using downloaded {'and verified ' if md5 else ''}file: {fpath}")
        return

    url = "https://drive.google.com/uc"
    params = dict(id=file_id, export="download")
    with requests.Session() as session:
        response = session.get(url, params=params, stream=True)

        for key, value in response.cookies.items():
            if key.startswith("download_warning"):
                token = value
                break
        else:
            api_response, content = _extract_gdrive_api_response(response)
            token = "t" if api_response == "Virus scan warning" else None

        if token is not None:
            response = session.get(url, params=dict(params, confirm=token), stream=True)
            api_response, content = _extract_gdrive_api_response(response)

        if api_response == "Quota exceeded":
            raise RuntimeError(
                f"The daily quota of the file {filename} is exceeded and it "
                f"can't be downloaded. This is a limitation of Google Drive "
                f"and can only be overcome by trying again later."
            )

        _save_response_content(content, fpath)

    # In case we deal with an unhandled GDrive API response, the file should be smaller than 10kB and contain only text
    if os.stat(fpath).st_size < 10 * 1024:
        with contextlib.suppress(UnicodeDecodeError), open(fpath) as fh:
            text = fh.read()
            # Regular expression to detect HTML. Copied from https://stackoverflow.com/a/70585604
            if re.search(r"</?\s*[a-z-][^>]*\s*>|(&(?:[\w\d]+|#\d+|#x[a-f\d]+);)", text):
                warnings.warn(
                    f"We detected some HTML elements in the downloaded file. "
                    f"This most likely means that the download triggered an unhandled API response by GDrive. "
                    f"Please report this to torchvision at https://github.com/pytorch/vision/issues including "
                    f"the response:\n\n{text}"
                )

    if md5 and not check_md5(fpath, md5):
        raise RuntimeError(
            f"The MD5 checksum of the download file {fpath} does not match the one on record."
            f"Please delete the file and try again. "
            f"If the issue persists, please report this to torchvision at https://github.com/pytorch/vision/issues."
        )


def _get_google_drive_file_id(url: str) -> Optional[str]:
    parts = urlparse(url)

    if re.match(r"(drive|docs)[.]google[.]com", parts.netloc) is None:
        return None

    match = re.match(r"/file/d/(?P<id>[^/]*)", parts.path)
    if match is None:
        return None

    return match.group("id")


def _urlretrieve(url: str, filename: str, chunk_size: int = 1024 * 32) -> None:
    with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": USER_AGENT})) as response:
        _save_response_content(iter(lambda: response.read(chunk_size), b""), filename, length=response.length)


def _save_response_content(
    content: Iterator[bytes],
    destination: str,
    length: Optional[int] = None,
) -> None:
    with open(destination, "wb") as fh, tqdm(total=length) as pbar:
        for chunk in content:
            # filter out keep-alive new chunks
            if not chunk:
                continue

            fh.write(chunk)
            pbar.update(len(chunk))




def _extract_gdrive_api_response(response, chunk_size: int = 32 * 1024) -> Tuple[bytes, Iterator[bytes]]:
    content = response.iter_content(chunk_size)
    first_chunk = None
    # filter out keep-alive new chunks
    while not first_chunk:
        first_chunk = next(content)
    content = itertools.chain([first_chunk], content)

    try:
        match = re.search("<title>Google Drive - (?P<api_response>.+?)</title>", first_chunk.decode())
        api_response = match["api_response"] if match is not None else None
    except UnicodeDecodeError:
        api_response = None
    return api_response, content

            