"""Minimal CBOR codec for the subset Rumoca Bitcode uses.

Rumoca writes definite-length maps and arrays, text strings, integers, 64-bit
floats, booleans and null. That is a small enough subset to implement here,
which keeps the SDK dependency-free: reading a ``.rbc`` file needs nothing but
the standard library.

If ``cbor2`` is installed it is used instead, since it is faster and handles
anything a future producer might emit.
"""

from __future__ import annotations

import struct
from typing import Any, BinaryIO

try:  # pragma: no cover - exercised only when the optional dep is present
    import cbor2 as _cbor2
except ImportError:  # pragma: no cover
    _cbor2 = None


class CborError(ValueError):
    """The byte stream is not CBOR this decoder understands."""


_FLOAT_WIDTHS = {25: 2, 26: 4, 27: 8}
_ARGUMENT_WIDTHS = {24: 1, 25: 2, 26: 4, 27: 8}


# ── Decoding ─────────────────────────────────────────────────────────────────


def loads(data: bytes) -> Any:
    """Decode a CBOR document."""
    if _cbor2 is not None:
        return _cbor2.loads(data)
    value, offset = _decode(data, 0)
    if offset != len(data):
        raise CborError(f"{len(data) - offset} trailing byte(s) after CBOR document")
    return value


def load(stream: BinaryIO) -> Any:
    return loads(stream.read())


def _decode(data: bytes, offset: int) -> tuple[Any, int]:
    if offset >= len(data):
        raise CborError("truncated CBOR: expected a header byte")
    initial = data[offset]
    major = initial >> 5
    minor = initial & 0x1F

    # Major type 7 carries floats and simple values; its minor value selects the
    # payload width directly, so it is read before the generic argument decode.
    if major == 7:
        return _decode_simple(data, offset, minor)

    argument, offset = _argument(data, offset, minor)

    if major == 0:
        return argument, offset
    if major == 1:
        return -1 - argument, offset
    if major == 2:
        end = _end(data, offset, argument, "byte string")
        return data[offset:end], end
    if major == 3:
        end = _end(data, offset, argument, "text string")
        return data[offset:end].decode("utf-8"), end
    if major == 4:
        items = []
        for _ in range(argument):
            item, offset = _decode(data, offset)
            items.append(item)
        return items, offset
    if major == 5:
        result: dict[Any, Any] = {}
        for _ in range(argument):
            key, offset = _decode(data, offset)
            value, offset = _decode(data, offset)
            result[key] = value
        return result, offset
    if major == 6:
        # A tag we do not interpret; decode the tagged item transparently.
        return _decode(data, offset)
    raise CborError(f"unsupported CBOR major type {major}")


def _argument(data: bytes, offset: int, minor: int) -> tuple[int, int]:
    offset += 1
    if minor < 24:
        return minor, offset
    width = _ARGUMENT_WIDTHS.get(minor)
    if width is None:
        # 28..30 are reserved; 31 is an indefinite length, which Rumoca never
        # emits. Refuse rather than guess.
        raise CborError(f"unsupported CBOR additional information {minor}")
    if offset + width > len(data):
        raise CborError("truncated CBOR: incomplete argument")
    return int.from_bytes(data[offset : offset + width], "big"), offset + width


def _end(data: bytes, offset: int, length: int, what: str) -> int:
    end = offset + length
    if end > len(data):
        raise CborError(f"truncated CBOR {what}")
    return end


def _decode_simple(data: bytes, offset: int, minor: int) -> tuple[Any, int]:
    if minor == 20:
        return False, offset + 1
    if minor == 21:
        return True, offset + 1
    if minor in (22, 23):  # null, undefined
        return None, offset + 1
    width = _FLOAT_WIDTHS.get(minor)
    if width is None:
        raise CborError(f"unsupported CBOR simple value {minor}")
    start = offset + 1
    if start + width > len(data):
        raise CborError("truncated CBOR float")
    if minor == 25:
        (raw,) = struct.unpack_from(">H", data, start)
        return _half_to_float(raw), start + 2
    if minor == 26:
        (value,) = struct.unpack_from(">f", data, start)
        return value, start + 4
    (value,) = struct.unpack_from(">d", data, start)
    return value, start + 8


def _half_to_float(raw: int) -> float:
    sign = (raw >> 15) & 0x1
    exponent = (raw >> 10) & 0x1F
    fraction = raw & 0x3FF
    if exponent == 0:
        value = fraction * 2.0**-24
    elif exponent == 31:
        value = float("inf") if fraction == 0 else float("nan")
    else:
        value = (1024 + fraction) * 2.0 ** (exponent - 25)
    return -value if sign else value


# ── Encoding ─────────────────────────────────────────────────────────────────


def dumps(value: Any) -> bytes:
    """Encode a document as CBOR."""
    if _cbor2 is not None:
        return _cbor2.dumps(value)
    out = bytearray()
    _encode(value, out)
    return bytes(out)


def dump(value: Any, stream: BinaryIO) -> None:
    stream.write(dumps(value))


def _encode_head(major: int, argument: int, out: bytearray) -> None:
    if argument < 24:
        out.append((major << 5) | argument)
    elif argument < 0x100:
        out.append((major << 5) | 24)
        out.append(argument)
    elif argument < 0x10000:
        out.append((major << 5) | 25)
        out.extend(struct.pack(">H", argument))
    elif argument < 0x1_0000_0000:
        out.append((major << 5) | 26)
        out.extend(struct.pack(">I", argument))
    else:
        out.append((major << 5) | 27)
        out.extend(struct.pack(">Q", argument))


def _encode(value: Any, out: bytearray) -> None:
    # bool before int: Python's bool is a subclass of int.
    if value is None:
        out.append(0xF6)
    elif isinstance(value, bool):
        out.append(0xF5 if value else 0xF4)
    elif isinstance(value, int):
        if value >= 0:
            _encode_head(0, value, out)
        else:
            _encode_head(1, -1 - value, out)
    elif isinstance(value, float):
        out.append(0xFB)
        out.extend(struct.pack(">d", value))
    elif isinstance(value, str):
        encoded = value.encode("utf-8")
        _encode_head(3, len(encoded), out)
        out.extend(encoded)
    elif isinstance(value, (bytes, bytearray)):
        _encode_head(2, len(value), out)
        out.extend(value)
    elif isinstance(value, (list, tuple)):
        _encode_head(4, len(value), out)
        for item in value:
            _encode(item, out)
    elif isinstance(value, dict):
        _encode_head(5, len(value), out)
        for key, item in value.items():
            _encode(key, out)
            _encode(item, out)
    else:
        raise CborError(f"cannot encode {type(value).__name__} as CBOR")
