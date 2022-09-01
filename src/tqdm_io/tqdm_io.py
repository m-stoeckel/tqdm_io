import sys
from io import TextIOWrapper
from os import PathLike
from pathlib import Path
from typing import AnyStr, IO, Iterable, Iterator, List, Optional, Union

from tqdm import tqdm


def utf8len(s):
    return len(s.encode('utf-8'))


def size_of(data):
    if isinstance(data, bytes):
        return len(data)
    elif hasattr(data, "iter"):
        return sum(size_of(el) for el in data)
    elif isinstance(data, str):
        return utf8len(data)
    else:
        return len(bytes(data))


class ProgressbarIO(IO[bytes]):
    def __init__(self, stream: IO[bytes], *args, **kwargs):
        self.stream: IO[bytes] = stream
        kwargs = {"unit": 'b', "unit_divisor": 1024, "unit_scale": True, "smoothing": 0} | kwargs
        self.tqdm = tqdm(*args, **kwargs)

    def read(self, size: int = -1):
        _read = self.stream.read(size)
        self.tqdm.update(size if size > 0 else size_of(_read))
        return _read

    def write(self, data):
        self.tqdm.update(data.__sizeof__())
        return self.stream.write(data)

    def close(self):
        self.stream.close()
        self.tqdm.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
        sys.stdout.flush()

    def fileno(self) -> int:
        return self.stream.fileno()

    def readline(self, limit: int = -1) -> AnyStr:
        _readline = self.stream.readline()
        self.tqdm.update(size_of(_readline))
        return _readline

    def readlines(self, hint: int = -1) -> List[AnyStr]:
        _readlines = self.stream.readlines(hint)
        self.tqdm.update(size_of(_readlines))
        return _readlines

    def seek(self, offset: int, whence: int = 0) -> int:
        return self.stream.seek(offset, whence)

    def seekable(self) -> bool:
        return self.stream.seekable()

    def tell(self) -> int:
        return self.stream.tell()

    def truncate(self, size: Optional[int] = None) -> int:
        return self.stream.truncate()

    def writable(self) -> bool:
        return self.stream.writable()

    def flush(self) -> None:
        self.stream.flush()

    def isatty(self) -> bool:
        return self.stream.isatty()

    def readable(self) -> bool:
        return self.stream.readable()

    def writelines(self, lines: Iterable[AnyStr]) -> None:
        self.tqdm.update(size_of(lines))
        return self.stream.writelines(lines)

    def __next__(self) -> AnyStr:
        _next = self.stream.__next__()
        self.tqdm.update(size_of(_next))
        return _next

    def __iter__(self) -> Iterator[AnyStr]:
        return self.stream.__iter__()

    @classmethod
    def open(
            cls,
            filepath: Union[str, PathLike],
            mode='rt',
            encoding='utf-8',
            **tqdm_kwargs
    ):
        """
        Opens a new file handle using pathlib.Path.open with the given mode for the given filepath.
        If the file is to be read, will determine the filesize and pass it on to the TQDM progressbar wrapper.

        :param filepath: The path of the file to open.
        :param mode: The opening mode. Wraps the raw IO in a TextIOWrapper if a 'text' mode is chosen.
        :param encoding: Encoding that is passed to the TextIOWrapper.
        :param tqdm_kwargs: Other kwargs for tqdm.
        :return: A ProgessbarIO wrapper around the opened file handle.
        """
        path = Path(filepath)

        tqdm_kwargs = {"total": path.stat().st_size if 'r' in mode else None} | tqdm_kwargs

        f_obj = cls(path.open('rb' if 'r' in mode else 'wb', buffering=2 ** 16), **tqdm_kwargs)
        if 't' in mode:
            f_obj = TextIOWrapper(f_obj, encoding=encoding)
        return f_obj
