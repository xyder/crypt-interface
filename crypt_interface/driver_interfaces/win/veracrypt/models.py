import array
import ctypes

from crypt_interface.driver_interfaces.exceptions import DriverException
from crypt_interface.driver_interfaces.win import constants


class BaseStruct(ctypes.Structure):
    """ Base Struct for all VeraCrypt Structs """
    _base_fields = [
        # buffer field to catch bytes when misaligned
        ('_buffer', ctypes.c_ubyte * 10000)
    ]

    def __repr__(self):
        return '<{}: {}>'.format(
            self.__class__.__name__, self.to_volume_list())

    __str__ = __repr__

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
            # todo: find a way to store this info safely for debugging purposes
            raise DriverException(
                '{}:{} Excess buffer contains data. '
                'Struct is not aligned.'.format(
                    self.__class__.__name__,
                    self.check_excess_buffer.__name__))


class MountListStruct(BaseStruct):
    """ src/Common/Apidrvr.h: MOUNT_LIST_STRUCT """

    _fields_ = [
                   # bitfield of all mounted drive letters
                   ('ulMountedDrives', ctypes.c_uint32),

                   # volume names of mounted volumes
                   ('wszVolume', ctypes.c_wchar
                    * constants.TC_MAX_PATH * constants.MAX_VOLUMES),

                   # labels of mounted volumes
                   ('wszLabel', ctypes.c_wchar
                    * constants.VOLUME_LABEL_SIZE * constants.MAX_VOLUMES),

                   # IDs of mounted volumes
                   ('volumeID', ctypes.c_wchar
                    * constants.VOLUME_ID_SIZE * constants.MAX_VOLUMES),

                   # disk size in bytes
                   ('diskLength', ctypes.c_uint64 * constants.MAX_VOLUMES),

                   # encryption algorithm
                   ('ea', ctypes.c_int * constants.MAX_VOLUMES),

                   # volume type (e.g. PROP_VOL_TYPE_OUTER, etc.)
                   ('volumeType', ctypes.c_int * constants.MAX_VOLUMES),

                   ('truecryptMode', ctypes.c_bool * constants.MAX_VOLUMES),
               ] + BaseStruct._base_fields
