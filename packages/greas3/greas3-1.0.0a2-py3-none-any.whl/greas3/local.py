from hashlib import sha256
from pathlib import Path
from typing import Optional, Union

from greas3.logging import logger


def has_expected_hash(
    path: Union[Path, str],
    expect: bytes,
    offset: int = 0,
    length: Optional[int] = None,
) -> bool:
    """
    Indicates whether or not the local file (or chunk described by `offset` and
    `length`) at `path` has the expected hash `expected`.
    """

    digest = sha256(usedforsecurity=False)

    with open(path, "rb") as f:
        f.seek(offset)

        while True:
            if length is None:
                read_len = 4096
            else:
                read_len = min(length, 4096)
                length -= read_len

            if data := f.read(read_len):
                digest.update(data)
            elif digest.digest() == expect:
                logger.debug(
                    "%s (from byte %s for %s bytes) has expected hash %s",
                    path,
                    offset,
                    length or "all",
                    expect.hex(),
                )
                return True
            else:
                logger.debug(
                    "%s (from byte %s for %s bytes) has hash %s but expected %s",
                    path,
                    offset,
                    length or "all",
                    digest.digest(),
                    expect,
                )
                return False
