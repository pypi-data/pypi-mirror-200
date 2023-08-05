from pathlib import Path
import shutil
from typing import Optional, Union, List

try:
    import gzip
    import tarfile
except:
    raise ImportError


def get_path(path: Union[Path, str]) -> Path:
    """Transform to `Path`.

    Args:
        path (str): The path to be transformed.

    Returns:
        Path: the `pathlib.Path` class
    """
    if isinstance(path, Path):
        return path
    else:
        return Path(path)


def get_path_out(
    path_in: Path, rename: str, path_out: Optional[Union[Path, str]] = None
):
    r"""
    Adaptor pathout to path_in
    """
    if path_out is None:
        return path_in.parent / rename
    else:
        _path_out = get_path(path_out)
        if _path_out.is_dir():
            return _path_out / rename
        elif path_out.is_file():
            return _path_out


def zip(path_in: Union[Path, str], path_out: Optional[Union[Path, str]] = None):
    r""" """
    _path_in = get_path(path_in)
    assert _path_in.is_file(), f"{path_in} is not a file"
    rename = _path_in.name + ".gz"
    _path_out = get_path_out(_path_in, rename, path_out)
    with open(_path_in, "rb") as f_in:
        with gzip.open(_path_out, "wb") as f_out:
            f_out.write(f_in.read())


def unzip(path_in: Union[Path, str], path_out: Optional[Union[Path, str]] = None):
    _path_in = get_path(path_in)
    assert _path_in.is_file(), f"{path_in} is not a file"
    assert _path_in.suffix == ".gz", f"not .gz file name"
    rename = _path_in.name.rstrip(".gz")  # rip
    _path_out = get_path_out(_path_in, rename, path_out)

    with gzip.open(_path_in, "rb") as f_in:
        with open(_path_out, "wb") as f_out:
            f_out.write(f_in.read())


def tar(
    path: Union[Path, str], staffs: Union[List[Union[Path, str]], Union[Path, str]]
):
    _path = get_path(path)
    with tarfile.open(_path, "w:gz") as tar:
        if isinstance(staffs, (str, Path)):
            tar.add(staffs)
            print(f"add {staffs}")
        elif isinstance(staffs, List):
            for staff in staffs:
                tar.add(staff)
                print(f"add {staff}")


def untar(path_in: Union[Path, str], path_out: Optional[Union[Path, str]] = None):
    _path_in = get_path(path_in)

    assert _path_in.is_file(), f"{path_in} is not a file"
    rename = _path_in.name.rstrip(".tar.gz")  # rip
    _path_out = get_path_out(_path_in, rename, path_out)

    with tarfile.open(_path_in, "r:gz") as tar:
        tar.extract(_path_out)
