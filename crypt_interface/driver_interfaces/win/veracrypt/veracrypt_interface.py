import ctypes

from crypt_interface.driver_interfaces.base_crypt_interface import \
    BaseCryptInterface
from crypt_interface.driver_interfaces.exceptions import DriverException
from crypt_interface.driver_interfaces.win.kernel32_interface import \
    DeviceIoControl
from crypt_interface.driver_interfaces.win.veracrypt import (
    models, constants, driver_models)


class VeraCryptInterface(BaseCryptInterface):
    def get_mounted_volumes(self):

        mount_list = driver_models.MountListStruct()
        p_mount_list = ctypes.pointer(mount_list)

        with DeviceIoControl(constants.VERACRYPT_DRIVER_PATH) as dctl:
            returned_count, _ = dctl.ioctl(
                constants.CtlCodes.TC_IOCTL_GET_MOUNTED_VOLUMES.value,
                p_mount_list, ctypes.sizeof(driver_models.MountListStruct),
                p_mount_list, ctypes.sizeof(driver_models.MountListStruct))

        if not returned_count:
            raise DriverException('DeviceIoControl call failed: {}'.format(
                ctypes.windll.kernel32.GetLastError()))

        mount_list.check_excess_buffer()
        return models.Volume.mount_list_to_volume_list(mount_list)
