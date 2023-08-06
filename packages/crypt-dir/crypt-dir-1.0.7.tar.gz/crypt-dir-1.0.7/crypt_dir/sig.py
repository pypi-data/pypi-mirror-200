import io
import os

from .crypt import sha1_hash, HASH_SIZE
from .util import uint64_to_bytes, UINT64_SIZE, bytes_to_uint64

KEY_SIGNATURE_SIZE = HASH_SIZE
FILE_SIGNATURE_SIZE = UINT64_SIZE


def get_key_signature(key: bytes) -> bytes:
    return sha1_hash(io.BytesIO(key))


def get_file_signature(path: str) -> bytes:
    stat = os.stat(path)
    mtime = stat.st_mtime_ns
    return uint64_to_bytes(mtime)


def set_file_signature(path: str, sig: bytes):
    mtime = bytes_to_uint64(sig)
    atime = mtime
    os.utime(path=path, ns=(atime, mtime))
