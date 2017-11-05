from enum import Enum

from crypt_interface.driver_interfaces import base_constants
from crypt_interface.driver_interfaces.win.veracrypt import utils

VERACRYPT_DRIVER_PATH = r'\\.\VeraCrypt'
TC_MAX_PATH = 260
MAX_PASSWORD = 64


class CtlCodes(Enum):
    TC_IOCTL_GET_DRIVER_VERSION = utils.vc_ctl_code(1)
    TC_IOCTL_MOUNT_VOLUME = utils.vc_ctl_code(3)
    TC_IOCTL_DISMOUNT_VOLUME = utils.vc_ctl_code(4)
    TC_IOCTL_DISMOUNT_ALL_VOLUMES = utils.vc_ctl_code(5)
    TC_IOCTL_GET_MOUNTED_VOLUMES = utils.vc_ctl_code(6)
    TC_IOCTL_GET_VOLUME_PROPERTIES = utils.vc_ctl_code(7)


class EncryptionAlgorithm(base_constants.PrintableEnum):
    NONE = 0
    AES = 1
    SERPENT = 2
    TWOFISH = 3
    CAMELLIA = 4
    GOST89 = 5
    KUZNYECHIK = 6
    AES_TWOFISH = 7
    AES_TWOFISH_SERPENT = 8
    SERPENT_AES = 9
    SERPENT_TWOFISH_AES = 10
    TWOFISH_SERPENT = 11


class VolumeType(base_constants.PrintableEnum):
    PROP_VOL_TYPE_NORMAL = 0
    PROP_VOL_TYPE_HIDDEN = 1
    # Outer / normal(hidden volume protected)
    PROP_VOL_TYPE_OUTER = 2
    # Outer / normal(hidden volume protected AND write already prevented)
    PROP_VOL_TYPE_OUTER_VOL_WRITE_PREVENTED = 3
    PROP_VOL_TYPE_SYSTEM = 4
    PROP_NBR_VOLUME_TYPES = 5


class UnMountErrorCodes(base_constants.PrintableEnum):
    VOLUME_NOT_MOUNTED = 5
    FILES_OPENED = 6

UnMountErrorCodes._labels = {
        UnMountErrorCodes.VOLUME_NOT_MOUNTED: 'Volume is not mounted.',
        UnMountErrorCodes.FILES_OPENED: 'Volumes contains files/folders '
                                        'in use by another program.',
    }


class MountErrorCodes(base_constants.PrintableEnum):
    ACCESS_DENIED = 3
    DRIVE_OCCUPIED = 5

MountErrorCodes._labels = {
    MountErrorCodes.ACCESS_DENIED: 'Access denied!',
    MountErrorCodes.DRIVE_OCCUPIED: 'Selected drive is occupied.'
}
