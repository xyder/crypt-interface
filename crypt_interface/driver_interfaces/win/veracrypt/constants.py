from enum import Enum

from crypt_interface.driver_interfaces.win.veracrypt import utils


class CtlCodes(Enum):
    TC_IOCTL_GET_MOUNTED_VOLUMES = utils.vc_ctl_code(6)
