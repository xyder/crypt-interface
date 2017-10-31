from crypt_interface.driver_interfaces.win import constants
from crypt_interface.driver_interfaces.win.kernel32_interface import ctl_code


def vc_ctl_code(code):
    """ Equivalent of:
    TC_IOCTL(CODE) (
        CTL_CODE (
            FILE_DEVICE_UNKNOWN, 0x800 + (CODE),
            METHOD_BUFFERED, FILE_ANY_ACCESS
        )
    )
    """

    return ctl_code(
        device_type=constants.FILE_DEVICE_UNKNOWN,
        func=0x800 + code,
        method=constants.METHOD_BUFFERED,
        access=constants.FILE_ANY_ACCESS)
