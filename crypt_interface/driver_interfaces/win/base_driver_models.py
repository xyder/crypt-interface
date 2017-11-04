import array
import ctypes

from crypt_interface.driver_interfaces.exceptions import DriverException


class BaseStruct(ctypes.Structure):
    """ Base Struct for all VeraCrypt Structs """
    _base_fields = [
        # buffer field to catch bytes when misaligned
        ('_buffer', ctypes.c_ubyte * 10000)
    ]

    def __init__(self, *args, **kwargs):
        self._processed_buffer = None

        super().__init__(*args, **kwargs)

    def check_excess_buffer(self):
        """ Checks the excess buffer for stray bytes. This happens when
        the struct is not aligned.
        """

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
