import ctypes
import ctypes.wintypes as wintypes

from crypt_interface.driver_interfaces.base_crypt_interface import \
    BaseCryptInterface
from crypt_interface.driver_interfaces.exceptions import DriverException
from crypt_interface.driver_interfaces.win.kernel32_interface import \
    DeviceIoControl
from crypt_interface.driver_interfaces.win.veracrypt import (
    models, constants, driver_models)


class VeraCryptInterface(BaseCryptInterface):
    def get_mounted_volumes(self):
        error_message_template = 'List mounted volumes failed: {}'

        mount_list = driver_models.MountListStruct()
        p_mount_list = ctypes.pointer(mount_list)

        with DeviceIoControl(constants.VERACRYPT_DRIVER_PATH) as dctl:
            returned_count, _ = dctl.ioctl(
                constants.CtlCodes.TC_IOCTL_GET_MOUNTED_VOLUMES.value,
                p_mount_list, ctypes.sizeof(driver_models.MountListStruct),
                p_mount_list, ctypes.sizeof(driver_models.MountListStruct))

        if not returned_count:
            raise DriverException(error_message_template.format(
                'DeviceIoControl call failed: {}'.format(
                    ctypes.windll.kernel32.GetLastError())))

        mount_list.check_excess_buffer()
        return models.Volume.mount_list_to_volume_list(mount_list)

    def dismount_volume(self, volume, ignore_open_files=False):
        drive_letter = chr(ord('A') + volume.drive_no)
        error_message_template = 'Dismount volume "{}" failed: {}'.format(
            drive_letter, '{}')
        dismount_buffer = driver_models.UnMountStruct()

        dismount_buffer.nDosDriveNo = volume.drive_no
        dismount_buffer.ignoreOpenFiles = wintypes.BOOL(ignore_open_files)
        p_dismount_buffer = ctypes.pointer(dismount_buffer)

        with DeviceIoControl(constants.VERACRYPT_DRIVER_PATH) as dctl:
            returned_count, _ = dctl.ioctl(
                constants.CtlCodes.TC_IOCTL_DISMOUNT_VOLUME.value,
                p_dismount_buffer, ctypes.sizeof(driver_models.UnMountStruct),
                p_dismount_buffer, ctypes.sizeof(driver_models.UnMountStruct))

        if not returned_count:
            raise DriverException(error_message_template.format(
                'DeviceIoControl call failed: {}'.format(
                    ctypes.windll.kernel32.GetLastError())))

        dismount_buffer.check_excess_buffer()

        if dismount_buffer.HiddenVolumeProtectionTriggered:
            raise DriverException(error_message_template.format(
                'Hidden volume protection was trigered!'.format(drive_letter)))

        if not dismount_buffer.nReturnCode == 0:
            try:
                error_message = constants.UnMountErrors(
                    dismount_buffer.nReturnCode)
            except ValueError:
                error_message = 'error code {}'.format(
                    dismount_buffer.nReturnCode)

            raise DriverException(error_message_template.format(
                error_message))
