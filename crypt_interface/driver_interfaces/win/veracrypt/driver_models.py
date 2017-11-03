import ctypes

from crypt_interface.driver_interfaces import win
from crypt_interface.driver_interfaces.win import base_driver_models


class MountListStruct(base_driver_models.BaseStruct):
    """ src/Common/Apidrvr.h: MOUNT_LIST_STRUCT """

    _fields_ = [
                   # bitfield of all mounted drive letters
                   ('ulMountedDrives', ctypes.c_uint32),

                   # volume names of mounted volumes
                   ('wszVolume', ctypes.c_wchar
                    * win.constants.TC_MAX_PATH * win.constants.MAX_VOLUMES),

                   # labels of mounted volumes
                   ('wszLabel', ctypes.c_wchar
                    * win.constants.VOLUME_LABEL_SIZE
                    * win.constants.MAX_VOLUMES),

                   # IDs of mounted volumes
                   ('volumeID', ctypes.c_wchar
                    * win.constants.VOLUME_ID_SIZE
                    * win.constants.MAX_VOLUMES),

                   # disk size in bytes
                   ('diskLength', ctypes.c_uint64 * win.constants.MAX_VOLUMES),

                   # encryption algorithm
                   ('ea', ctypes.c_int * win.constants.MAX_VOLUMES),

                   # volume type (e.g. PROP_VOL_TYPE_OUTER, etc.)
                   ('volumeType', ctypes.c_int * win.constants.MAX_VOLUMES),

                   ('truecryptMode', ctypes.c_bool
                    * win.constants.MAX_VOLUMES),
               ] + base_driver_models.BaseStruct._base_fields
