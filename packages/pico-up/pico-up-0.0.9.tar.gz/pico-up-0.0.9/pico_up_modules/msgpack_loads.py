'''
This module code is taken from https://github.com/vsergeev/u-msgpack-python
Notes:
* only supports unpacking, all other functionality has been removed
'''

import io
import struct
import sys
import collections
import time


class InvalidString(bytes):
    pass


class PackException(Exception):
    pass


class UnpackException(Exception):
    pass


class UnsupportedTypeException(PackException):
    pass


class InsufficientDataException(UnpackException):
    pass


class InvalidStringException(UnpackException):
    pass


class UnsupportedTimestampException(UnpackException):
    pass


class ReservedCodeException(UnpackException):
    pass


class UnhashableKeyException(UnpackException):
    pass


class DuplicateKeyException(UnpackException):
    pass


class Ext(object):
    """
    The Ext class facilitates creating a serializable extension object to store
    an application-defined type and data byte array.
    """

    def __init__(self, type, data):
        """
        Construct a new Ext object.

        Args:
            type: application-defined type integer
            data: application-defined data byte array

        TypeError:
            Type is not an integer.
        ValueError:
            Type is out of range of -128 to 127.
        TypeError::
            Data is not type 'bytes' (Python 3) or not type 'str' (Python 2).

        Example:
        >>> foo = umsgpack.Ext(5, b"\x01\x02\x03")
        >>> umsgpack.packb({u"special stuff": foo, u"awesome": True})
        '\x82\xa7awesome\xc3\xadspecial stuff\xc7\x03\x05\x01\x02\x03'
        >>> bar = umsgpack.unpackb(_)
        >>> print(bar["special stuff"])
        Ext Object (Type: 5, Data: 01 02 03)
        >>>
        """
        # Check type is type int and in range
        if not isinstance(type, int):
            raise TypeError("ext type is not type integer")
        elif not (-2 ** 7 <= type <= 2 ** 7 - 1):
            raise ValueError("ext type value {:d} is out of range (-128 to 127)".format(type))
        # Check data is type bytes or str
        elif sys.version_info[0] == 3 and not isinstance(data, bytes):
            raise TypeError("ext data is not type \'bytes\'")
        elif sys.version_info[0] == 2 and not isinstance(data, str):
            raise TypeError("ext data is not type \'str\'")

        self.type = type
        self.data = data

    def __eq__(self, other):
        """
        Compare this Ext object with another for equality.
        """
        return isinstance(other, self.__class__) \
            and self.type == other.type and self.data == other.data

    def __ne__(self, other):
        """
        Compare this Ext object with another for inequality.
        """
        return not self.__eq__(other)

    def __str__(self):
        """
        String representation of this Ext object.
        """
        s = "Ext Object (Type: {:d}, Data: ".format(self.type)
        s += " ".join(["0x{:02x}".format(ord(self.data[i:i + 1]))
                       for i in range(min(len(self.data), 8))])
        if len(self.data) > 8:
            s += " ..."
        s += ")"
        return s

    def __hash__(self):
        """
        Provide a hash of this Ext object.
        """
        return hash((self.type, self.data))


def _read_except(fp, n):
    if n == 0:
        return b""

    data = fp.read(n)
    if len(data) == 0:
        raise InsufficientDataException()

    while len(data) < n:
        chunk = fp.read(n - len(data))
        if len(chunk) == 0:
            raise InsufficientDataException()

        data += chunk

    return data


def _unpack_integer(code, fp, options):
    if (ord(code) & 0xe0) == 0xe0:
        return struct.unpack("b", code)[0]
    elif code == b'\xd0':
        return struct.unpack("b", _read_except(fp, 1))[0]
    elif code == b'\xd1':
        return struct.unpack(">h", _read_except(fp, 2))[0]
    elif code == b'\xd2':
        return struct.unpack(">i", _read_except(fp, 4))[0]
    elif code == b'\xd3':
        return struct.unpack(">q", _read_except(fp, 8))[0]
    elif (ord(code) & 0x80) == 0x00:
        return struct.unpack("B", code)[0]
    elif code == b'\xcc':
        return struct.unpack("B", _read_except(fp, 1))[0]
    elif code == b'\xcd':
        return struct.unpack(">H", _read_except(fp, 2))[0]
    elif code == b'\xce':
        return struct.unpack(">I", _read_except(fp, 4))[0]
    elif code == b'\xcf':
        return struct.unpack(">Q", _read_except(fp, 8))[0]
    raise Exception("logic error, not int: 0x{:02x}".format(ord(code)))


def _deep_list_to_tuple(obj):
    if isinstance(obj, list):
        return tuple([_deep_list_to_tuple(e) for e in obj])
    return obj


def _unpack_map(code, fp, options):
    if (ord(code) & 0xf0) == 0x80:
        length = (ord(code) & ~0xf0)
    elif code == b'\xde':
        length = struct.unpack(">H", _read_except(fp, 2))[0]
    elif code == b'\xdf':
        length = struct.unpack(">I", _read_except(fp, 4))[0]
    else:
        raise Exception("logic error, not map: 0x{:02x}".format(ord(code)))

    d = {} if not options.get('use_ordered_dict') else collections.OrderedDict()
    for _ in range(length):
        # Unpack key
        k = _unpack(fp, options)

        if isinstance(k, list):
            # Attempt to convert list into a hashable tuple
            k = _deep_list_to_tuple(k)
        # elif not isinstance(k, Hashable):
        #     raise UnhashableKeyException(
        #         "encountered unhashable key: \"{:s}\" ({:s})".format(str(k), str(type(k))))
        elif k in d:
            raise DuplicateKeyException(
                "encountered duplicate key: \"{:s}\" ({:s})".format(str(k), str(type(k))))

        # Unpack value
        v = _unpack(fp, options)

        try:
            d[k] = v
        except TypeError:
            raise UnhashableKeyException(
                "encountered unhashable key: \"{:s}\"".format(str(k)))
    return d


def _unpack_array(code, fp, options):
    if (ord(code) & 0xf0) == 0x90:
        length = (ord(code) & ~0xf0)
    elif code == b'\xdc':
        length = struct.unpack(">H", _read_except(fp, 2))[0]
    elif code == b'\xdd':
        length = struct.unpack(">I", _read_except(fp, 4))[0]
    else:
        raise Exception("logic error, not array: 0x{:02x}".format(ord(code)))

    if options.get('use_tuple'):
        return tuple((_unpack(fp, options) for i in range(length)))

    return [_unpack(fp, options) for i in range(length)]


def _unpack_string(code, fp, options):
    if (ord(code) & 0xe0) == 0xa0:
        length = ord(code) & ~0xe0
    elif code == b'\xd9':
        length = struct.unpack("B", _read_except(fp, 1))[0]
    elif code == b'\xda':
        length = struct.unpack(">H", _read_except(fp, 2))[0]
    elif code == b'\xdb':
        length = struct.unpack(">I", _read_except(fp, 4))[0]
    else:
        raise Exception("logic error, not string: 0x{:02x}".format(ord(code)))

    # Always return raw bytes in compatibility mode
    global compatibility
    if compatibility:
        return _read_except(fp, length)

    data = _read_except(fp, length)
    try:
        return bytes.decode(data, 'utf-8')
    except UnicodeDecodeError:
        if options.get("allow_invalid_utf8"):
            return InvalidString(data)
        raise InvalidStringException("unpacked string is invalid utf-8")


def _unpack_nil(code, fp, options):
    if code == b'\xc0':
        return None
    raise Exception("logic error, not nil: 0x{:02x}".format(ord(code)))


def _unpack_boolean(code, fp, options):
    if code == b'\xc2':
        return False
    elif code == b'\xc3':
        return True
    raise Exception("logic error, not boolean: 0x{:02x}".format(ord(code)))


def _unpack_float(code, fp, options):
    if code == b'\xca':
        return struct.unpack(">f", _read_except(fp, 4))[0]
    elif code == b'\xcb':
        return struct.unpack(">d", _read_except(fp, 8))[0]
    raise Exception("logic error, not float: 0x{:02x}".format(ord(code)))


def _unpack_reserved(code, fp, options):
    if code == b'\xc1':
        raise ReservedCodeException(
            "encountered reserved code: 0x{:02x}".format(ord(code)))
    raise Exception(
        "logic error, not reserved code: 0x{:02x}".format(ord(code)))


def _unpack_binary(code, fp, options):
    if code == b'\xc4':
        length = struct.unpack("B", _read_except(fp, 1))[0]
    elif code == b'\xc5':
        length = struct.unpack(">H", _read_except(fp, 2))[0]
    elif code == b'\xc6':
        length = struct.unpack(">I", _read_except(fp, 4))[0]
    else:
        raise Exception("logic error, not binary: 0x{:02x}".format(ord(code)))

    return _read_except(fp, length)


_ext_class_to_type = {}
_ext_type_to_class = {}


def ext_serializable(ext_type):
    """
    Return a decorator to register a class for automatic packing and unpacking
    with the specified Ext type code. The application class should implement a
    `packb()` method that returns serialized bytes, and an `unpackb()` class
    method or static method that accepts serialized bytes and returns an
    instance of the application class.

    Args:
        ext_type: application-defined Ext type code

    Raises:
        TypeError:
            Ext type is not an integer.
        ValueError:
            Ext type is out of range of -128 to 127.
        ValueError:
            Ext type or class already registered.
    """

    def wrapper(cls):
        if not isinstance(ext_type, int):
            raise TypeError("Ext type is not type integer")
        elif not (-2 ** 7 <= ext_type <= 2 ** 7 - 1):
            raise ValueError("Ext type value {:d} is out of range of -128 to 127".format(ext_type))
        elif ext_type in _ext_type_to_class:
            raise ValueError(
                "Ext type {:d} already registered with class {:s}".format(ext_type, repr(_ext_type_to_class[ext_type])))
        elif cls in _ext_class_to_type:
            raise ValueError("Class {:s} already registered with Ext type {:d}".format(repr(cls), ext_type))

        _ext_type_to_class[ext_type] = cls
        _ext_class_to_type[cls] = ext_type

        return cls

    return wrapper


def _unpack_ext(code, fp, options):
    if code == b'\xd4':
        length = 1
    elif code == b'\xd5':
        length = 2
    elif code == b'\xd6':
        length = 4
    elif code == b'\xd7':
        length = 8
    elif code == b'\xd8':
        length = 16
    elif code == b'\xc7':
        length = struct.unpack("B", _read_except(fp, 1))[0]
    elif code == b'\xc8':
        length = struct.unpack(">H", _read_except(fp, 2))[0]
    elif code == b'\xc9':
        length = struct.unpack(">I", _read_except(fp, 4))[0]
    else:
        raise Exception("logic error, not ext: 0x{:02x}".format(ord(code)))

    ext_type = struct.unpack("b", _read_except(fp, 1))[0]
    ext_data = _read_except(fp, length)

    # Unpack with ext handler, if we have one
    ext_handlers = options.get("ext_handlers")
    if ext_handlers and ext_type in ext_handlers:
        return ext_handlers[ext_type](Ext(ext_type, ext_data))

    # Unpack with ext classes, if type is registered
    if ext_type in _ext_type_to_class:
        try:
            return _ext_type_to_class[ext_type].unpackb(ext_data)
        except AttributeError:
            raise NotImplementedError("Ext serializable class {:s} is missing implementation of unpackb()".format(
                repr(_ext_type_to_class[ext_type])))

    # Timestamp extension
    if ext_type == -1:
        return _unpack_ext_timestamp(ext_data, options)

    return Ext(ext_type, ext_data)


def _unpack_ext_timestamp(ext_data, options):
    obj_len = len(ext_data)
    if obj_len == 4:
        # 32-bit timestamp
        seconds = struct.unpack(">I", ext_data)[0]
    elif obj_len == 8:
        # 64-bit timestamp
        value = struct.unpack(">Q", ext_data)[0]
        seconds = value & 0x3ffffffff
    elif obj_len == 12:
        # 96-bit timestamp
        seconds = struct.unpack(">q", ext_data[4:12])[0]
    else:
        raise UnsupportedTimestampException(
            "unsupported timestamp with data length {:d}".format(len(ext_data)))

    return time.gmtime(seconds)


def loads(s, **options):
    if not isinstance(s, (bytes, bytearray)):
        raise TypeError("packed data must be type 'bytes' or 'bytearray'")
    return _unpack(io.BytesIO(s), options)


def _unpack(fp, options):
    code = _read_except(fp, 1)
    return _unpack_dispatch_table[code](code, fp, options)


def __init():
    global compatibility
    global _float_precision
    global _unpack_dispatch_table

    # Compatibility mode for handling strings/bytes with the old specification
    compatibility = False
    _float_precision = "single"

    # Build a dispatch table for fast lookup of unpacking function

    _unpack_dispatch_table = {}
    # Fix uint
    for code in range(0, 0x7f + 1):
        _unpack_dispatch_table[struct.pack("B", code)] = _unpack_integer
    # Fix map
    for code in range(0x80, 0x8f + 1):
        _unpack_dispatch_table[struct.pack("B", code)] = _unpack_map
    # Fix array
    for code in range(0x90, 0x9f + 1):
        _unpack_dispatch_table[struct.pack("B", code)] = _unpack_array
    # Fix str
    for code in range(0xa0, 0xbf + 1):
        _unpack_dispatch_table[struct.pack("B", code)] = _unpack_string
    # Nil
    _unpack_dispatch_table[b'\xc0'] = _unpack_nil
    # Reserved
    _unpack_dispatch_table[b'\xc1'] = _unpack_reserved
    # Boolean
    _unpack_dispatch_table[b'\xc2'] = _unpack_boolean
    _unpack_dispatch_table[b'\xc3'] = _unpack_boolean
    # Bin
    for code in range(0xc4, 0xc6 + 1):
        _unpack_dispatch_table[struct.pack("B", code)] = _unpack_binary
    # Ext
    for code in range(0xc7, 0xc9 + 1):
        _unpack_dispatch_table[struct.pack("B", code)] = _unpack_ext
    # Float
    _unpack_dispatch_table[b'\xca'] = _unpack_float
    _unpack_dispatch_table[b'\xcb'] = _unpack_float
    # Uint
    for code in range(0xcc, 0xcf + 1):
        _unpack_dispatch_table[struct.pack("B", code)] = _unpack_integer
    # Int
    for code in range(0xd0, 0xd3 + 1):
        _unpack_dispatch_table[struct.pack("B", code)] = _unpack_integer
    # Fixext
    for code in range(0xd4, 0xd8 + 1):
        _unpack_dispatch_table[struct.pack("B", code)] = _unpack_ext
    # String
    for code in range(0xd9, 0xdb + 1):
        _unpack_dispatch_table[struct.pack("B", code)] = _unpack_string
    # Array
    _unpack_dispatch_table[b'\xdc'] = _unpack_array
    _unpack_dispatch_table[b'\xdd'] = _unpack_array
    # Map
    _unpack_dispatch_table[b'\xde'] = _unpack_map
    _unpack_dispatch_table[b'\xdf'] = _unpack_map
    # Negative fixint
    for code in range(0xe0, 0xff + 1):
        _unpack_dispatch_table[struct.pack("B", code)] = _unpack_integer


__init()
