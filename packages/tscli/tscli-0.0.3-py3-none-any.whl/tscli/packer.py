import struct

_pack_types = {
    "int8": (1, "b"),
    "uint8": (1, "B"),
    "int16": (2, "h"),
    "uint16": (2, "H"),
    "int32": (4, "i"),
    "uint32": (4, "I"),
    "int64": (8, "q"),
    "uint64": (8, "Q"),
    "float": (4, "f"),
    "double": (8, "d"),
    "bool": (1, "B")
}

def is_valid_dtype(dtype):
    return dtype in _pack_types

def pack_to_bytes(arr, dtype):
    import struct
    assert  dtype in _pack_types
    item = _pack_types[dtype]
    ele_size = item[0]
    ele_fmt = item[1]


    fmt = "<" + str(len(arr)) + ele_fmt

    if dtype == "bool":
        arr = list(map(lambda x: int(x != 0), arr))

    ret = struct.pack(fmt, *arr)

    assert len(ret) == ele_size * len(arr)
    return ret


def unpack_from_bytes(binary, dtype):
    import struct
    assert  dtype in _pack_types
    item = _pack_types[dtype]
    ele_size = item[0]
    ele_fmt = item[1]

    cnt = int(len(binary) / ele_size)

    fmt = "<" + str(cnt) + ele_fmt

    ret = struct.unpack(fmt, binary)

    if dtype == "bool":
        ret = map(lambda x: x != 0, ret)

    return list(ret)