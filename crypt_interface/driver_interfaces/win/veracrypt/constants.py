from enum import Enum

from crypt_interface.driver_interfaces.win.veracrypt import utils

VERACRYPT_DRIVER_PATH = r'\\.\VeraCrypt'


class CtlCodes(Enum):
    TC_IOCTL_MOUNT_VOLUME = utils.vc_ctl_code(3)
    TC_IOCTL_DISMOUNT_VOLUME = utils.vc_ctl_code(4)
    TC_IOCTL_DISMOUNT_ALL_VOLUMES = utils.vc_ctl_code(5)
    TC_IOCTL_GET_MOUNTED_VOLUMES = utils.vc_ctl_code(6)


class PrintableEnum(Enum):
    def __repr__(self):
        return getattr(self, '_labels', {}).get(self, self.name)

    __str__ = __repr__


class EncryptionAlgorithm(PrintableEnum):
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


class VolumeType(PrintableEnum):
    PROP_VOL_TYPE_NORMAL = 0
    PROP_VOL_TYPE_HIDDEN = 1
    # Outer / normal(hidden volume protected)
    PROP_VOL_TYPE_OUTER = 2
    # Outer / normal(hidden volume protected AND write already prevented)
    PROP_VOL_TYPE_OUTER_VOL_WRITE_PREVENTED = 3
    PROP_VOL_TYPE_SYSTEM = 4
    PROP_NBR_VOLUME_TYPES = 5


class UnMountErrors(PrintableEnum):
    VOLUME_NOT_MOUNTED = 5
    FILES_OPENED = 6

UnMountErrors._labels = {
        UnMountErrors.VOLUME_NOT_MOUNTED: 'Volume is not mounted.',
        UnMountErrors.FILES_OPENED: 'Volumes contains files/folders'
                                    ' in use by another program.',
    }
