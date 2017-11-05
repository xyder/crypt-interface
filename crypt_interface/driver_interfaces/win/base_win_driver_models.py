import array
import ctypes
from functools import partialmethod

from crypt_interface.driver_interfaces.exceptions import DriverException


class PConverters(object):
    """ Provides converters from C/C++/Win types to Python types """

    @staticmethod
    def wchar_array(val):
        """ WChar[] to unicode string """

        return val.value

    @staticmethod
    def wchar_array_path(val):
        """ WChar[] to unicode string containing a file path """

        output = val.value
        if output.startswith('\\??\\'):
            output = output[4:]

        return output

    @staticmethod
    def wchar_byte_array(val, encoding, errors):
        """ WChar[] to bytes """

        return bytes(val.value, encoding=encoding, errors=errors)

    @staticmethod
    def win_bool(val):
        """ wintypes.BOOL to bool """

        return bool(val)

    @staticmethod
    def enum_converter(val, enum_class):
        """ c_int to Enum """

        try:
            output = enum_class(val)
        except ValueError:
            output = val

        return output

    # WChar[] to utf-16 bytes
    wchar_utf16_byte_array = partialmethod(wchar_byte_array, encoding='utf-16')

    # WChar[] to utf-16 bytes with surrogate pass error handler
    wchar_utf16_surrogate_pass_byte_array = partialmethod(
        wchar_utf16_byte_array, errors='surrogatepass')


class CConverters(object):
    """ Provides converters from Python to C/C++/Win types """
    @staticmethod
    def bytestring_to_ubyte_array(val, size):
        """ Bytes to zeros initialized unsigned c_char[] """

        return (ctypes.c_ubyte * size).from_buffer_copy(
            val + bytes(size - len(val)))


class Field(object):
    """ Defines a Field for conversions to/from Python objects
    and ctypes.Structure
    """

    def __init__(self, name, alias, field_type, is_indexed=False,
                 converter=lambda x: x):
        """
        :param name: Struct name of the field
        :param alias: Python instance name of the field
        :param field_type: ctypes type of the field
        :param is_indexed: if True, it will be treated as an array
        :param converter: function to convert field to a Python type
        """

        self.type = field_type
        self.alias = alias
        self.name = name
        self.converter = converter
        self.is_indexed = is_indexed

    def to_struct_field(self):
        """ Returns a ctypes.Structure field definition """

        return self.name, self.type

    def to_object_attr(self, obj, struct, index=None, set_missing=False):
        """ Fills an instance attribute with the converted Python value

        :param obj: the instance to be modified
        :param struct: the struct from which the value is retrieved
        :param index: the index, which, if is_indexed is True, will represent
        the index within the corresponding struct array field
        :param set_missing: if False, it will only set the attribute if the
        instance already has the attribute defined

        :return: True - the operation succeeded
        """

        try:
            if not set_missing:
                # try to crash it
                _ = getattr(obj, self.alias)

            if not self.is_indexed:
                # ~= obj.<alias> = converter(struct.<name>)
                setattr(obj, self.alias, self.converter(
                    getattr(struct, self.name, None)))
            else:
                # ~= obj.<alias> = converter(struct.<name>[index])
                setattr(obj, self.alias, self.converter(
                    getattr(struct, self.name, [])[index]))

        except AttributeError:
            return False
        return True

    @staticmethod
    def struct_to_object(obj, struct, index=None, set_missing=False):
        """ Fills the attributes of an instance with the converted
        Python values

        :param obj: the instance to be modified
        :param struct: the struct from which the values are retrieved
        :param index: common index used accross all array fields
        :param set_missing: if False, it will only set the attributes
        if they are already defined for the instance
        """

        for field in struct.field_list:
            field.to_object_attr(obj, struct, index, set_missing)

    @staticmethod
    def iterable_to_struct_fields(it):
        """ Constructs a list of struct fields from an iterable of Fields

        :param it: iterable that contains Fields
        :return: list of struct fields (tuples of name and type)
        """

        fields = []
        for field in iter(it):
            fields.append(field.to_struct_field())

        return fields


# noinspection PyTypeChecker
class BaseStruct(ctypes.Structure):
    """ Base Struct for all Crypt Structs """

    base_fields = [
        # buffer field to catch bytes when misaligned
        Field(name='_buffer', alias='_buffer',
              field_type=ctypes.c_ubyte * 10000)
    ]

    field_list = []

    def __init__(self, *args, **kwargs):
        self._processed_buffer = None

        super().__init__(*args, **kwargs)

    def check_excess_buffer(self):
        """ Checks the excess buffer for stray bytes. This happens when
        the struct is not aligned.
        """

        # if the struct doesn't define the buffer, abort check
        if not getattr(self, '_buffer', None):
            return

        buffers = []
        aux = []
        pos = -1

        # a bit more processing for debugging purposes
        # todo: add a DEBUG config and condition the debug-only code
        # store continuous bytes as separate (position, bytes) tuples
        for i in range(len(self._buffer)):
            b = self._buffer[i]
            if b:
                if not aux:
                    pos = i
                aux.append(b)
            else:
                if not len(aux):
                    continue

                buffers.append((pos, aux))
                aux = []

        self._processed_buffer = {}

        # convert to a nice dict
        for i in range(len(buffers)):
            pos = buffers[i][0]
            buffer = array.array('B', buffers[i][1]).tostring()
            self._processed_buffer[pos] = buffer

        if self._processed_buffer:
            # todo: expose more info here when debugging
            raise DriverException(
                '{}:{} Excess buffer contains data. '
                'Struct is not aligned.'.format(
                    self.__class__.__name__,
                    self.check_excess_buffer.__name__))
