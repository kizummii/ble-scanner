def bytes_to_hex_string(barray, with_prefix=False):
    if not barray:
        return ""
    hex_str = "".join(f"{b:02X}" for b in barray)
    return "0x" + hex_str if with_prefix else hex_str


def hex_string_to_bytes(hex_str):
    hex_str = hex_str.replace("0x", "").replace("0X", "")
    if len(hex_str) % 2 != 0:
        hex_str = "0" + hex_str
    return bytes.fromhex(hex_str)


def to_string(data):
    if data is None:
        return ""
    if isinstance(data, bytearray):
        data = bytes(data)
    if isinstance(data, bytes):
        try:
            return data.decode("utf-8", errors="replace")
        except Exception:
            return data.hex()
    return str(data)


def concat(a, b):
    if isinstance(a, bytearray):
        a = bytes(a)
    if isinstance(b, bytearray):
        b = bytes(b)
    return a + b


def int_to_bytes_le(value, length=4):
    return value.to_bytes(length, "little")


def bytes_to_int_le(data):
    return int.from_bytes(data, "little")
