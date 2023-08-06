import binascii
from base64 import urlsafe_b64encode, urlsafe_b64decode
from typing import Optional
from os.path import split as _split


S3_BUCKET_OBJECT_KEY_ENCODING = 'utf-8'


class KeyDecodeException(Exception):
    """
    Raised if decoding an HEAObject id or name string to an AWS S3 bucket object key failed. A possible nested
    exception may provide more details about why, but the types of nested exception raised are specific to the
    decoding algorithm implementation and are not part of HEA's public API.
    """
    pass


def encode_key(key: str) -> str:
    """
    Encodes an AWS S3 bucket object key to a string that can be inserted into URL paths. Bucket keys are /-separated
    paths, and URLs with escaped slashes are rejected or handled incorrectly by many servers and clients. This
    function encodes bucket keys to a limited character set that is URL-safe. This implementation currently uses
    URL-safe base 64 encoding, described at https://datatracker.ietf.org/doc/html/rfc4648#section-5, but the encoding
    algorithm is not part of HEA's public API and is subject to change.

    :param key: an AWS S3 bucket key.
    :return: the encoded string.
    """
    return urlsafe_b64encode(key.encode(S3_BUCKET_OBJECT_KEY_ENCODING)).decode(S3_BUCKET_OBJECT_KEY_ENCODING)


def decode_key(encoded_key: str) -> str:
    """
    Decodes the provided string to an AWS S3 object bucket key. This implementation currently uses URL-safe base 64
    decoding, described at https://datatracker.ietf.org/doc/html/rfc4648#section-5, but the encoding algorithm is not
    part of HEA's public API and is subject to change.

    :param encoded_key: the encoded key (required).
    :return: the actual AWS S3 bucket key.
    :raises _DecodeException: if the provided string could not be decoded.
    """
    try:
        return urlsafe_b64decode(encoded_key.encode(S3_BUCKET_OBJECT_KEY_ENCODING)).decode(S3_BUCKET_OBJECT_KEY_ENCODING)
    except (UnicodeDecodeError, binascii.Error) as e:
        raise KeyDecodeException(f'Failed to decode {encoded_key} to an AWS S3 bucket key') from e


def is_folder(key: Optional[str]) -> bool:
    """
    Returns whether the provided key represents a folder (ends with a /).

    :param key: the key.
    :return: True if the key represents a folder, False if not.
    """
    return key.endswith('/') if key is not None else False


def split(key: str) -> tuple[str, str]:
    """
    Splits the key's pathname into a pair, (head, tail), where tail is the last pathname component and head is
    everything leading up to that.

    :param key: the key to split.
    :return: a two-tuple containing the head and the tail. If the object is at the root of the bucket, then the head
    will be the empty string.
    """
    if is_folder(key):
        key_ = key.rstrip('/')
    else:
        key_ = key
    result = _split(key_)
    return result[0] + ('/' if result[0] else ''), (result[1] + '/') if is_folder(key) else result[1]


def join(head: str | None, tail: str) -> str:
    """
    Join a folder head to an object tail.

    :param head: the head. If None or the empty string, the head is assumed to be the root folder of a bucket.
    :param tail: the tail.
    :return: the resulting key.
    :raises ValueError: if the head is not a folder.
    """
    if head and not head.endswith('/'):
        raise ValueError(f'head must be a folder but was {head}')
    return f'{head}{tail}'


def replace_parent_folder(source_key: str, target_key: str) -> str:
    """
    Replace the key's folder with another folder, such as in an object copy.

    :param source_key: the source key.
    :param target_key: the target_key.
    :return: the resulting key.
    """
    return join(split(target_key)[0], split(source_key)[1])
