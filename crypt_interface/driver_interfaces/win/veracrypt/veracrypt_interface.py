import ctypes
import ctypes.wintypes as wintypes
from functools import partial

from crypt_interface.driver_interfaces import (
    win, exceptions, base_crypt_interface)
from crypt_interface.driver_interfaces.win.kernel32_interface import (
    DeviceIoControl,)
from crypt_interface.driver_interfaces.win.veracrypt import (
    models, constants, driver_models)


def prepend_error_message(val, prefix, enum_class):
    error_message = driver_models.VCPConverters.enum_converter(
        val, enum_class)

    if error_message == val:
        error_message = prefix.format(val)

    return error_message

prepend_error_code_message = partial(
    prepend_error_message, prefix='error code {}')


class VeraCryptInterface(base_crypt_interface.BaseCryptInterface):
    def get_mounted_volumes(self):
        error_message_template = 'List mounted volumes failed: {}'

        # build the output struct
        mount_list = driver_models.MountListStruct()
        p_mount_list = ctypes.pointer(mount_list)

        # run DeviceIoControl using the get_mounted_volumes control code
        with DeviceIoControl(constants.VERACRYPT_DRIVER_PATH) as dctl:
            returned_count, _ = dctl.ioctl(
                constants.CtlCodes.TC_IOCTL_GET_MOUNTED_VOLUMES.value,
                p_mount_list, ctypes.sizeof(driver_models.MountListStruct),
                p_mount_list, ctypes.sizeof(driver_models.MountListStruct))

        # check for failed execution
        if not returned_count:
            raise exceptions.DriverException(error_message_template.format(
                'DeviceIoControl call failed: {}'.format(
                    prepend_error_code_message(
                        val=ctypes.windll.kernel32.GetLastError(),
                        enum_class=win.constants.WinErrorCodes))))

        # check for struct alignment issues
        mount_list.check_excess_buffer()

        # convert resulting struct to Volume
        return models.Volume.mount_list_to_volume_list(mount_list)

    def mount_volume(self, volume, password):
        error_message_template = 'Mount volume "{}" failed: {}'.format(
            volume.path, '{}')

        # build the input/output struct
        mount_buffer = driver_models.MountStruct()
        mount_buffer.wszVolume = volume.path
        mount_buffer.VolumePassword.Length = len(password)
        mount_buffer.VolumePassword.Text = \
            driver_models.VCCConverters.bytes_to_password_text(password)
        mount_buffer.nDosDriveNo = volume.drive_no
        mount_buffer.bMountRemovable = win.constants.TRUE
        mount_buffer.bMountManager = win.constants.TRUE
        mount_buffer.bPreserveTimestamp = win.constants.TRUE

        p_mount_buffer = ctypes.pointer(mount_buffer)

        # run DeviceIoControl with the mount_volume control code
        with DeviceIoControl(constants.VERACRYPT_DRIVER_PATH) as dctl:
            returned_count, _ = dctl.ioctl(
                constants.CtlCodes.TC_IOCTL_MOUNT_VOLUME.value,
                p_mount_buffer, ctypes.sizeof(driver_models.MountStruct),
                p_mount_buffer, ctypes.sizeof(driver_models.MountStruct))

        # check for failed execution
        if not returned_count:
            raise exceptions.DriverException(error_message_template.format(
                'DeviceIoControl call failed: {}'.format(
                    prepend_error_code_message(
                        val=ctypes.windll.kernel32.GetLastError(),
                        enum_class=win.constants.WinErrorCodes))))

        # check for struct alignment issues
        mount_buffer.check_excess_buffer()

        # check for failed return code from driver
        if not mount_buffer.nReturnCode == 0:
            raise exceptions.DriverException(error_message_template.format(
                prepend_error_code_message(
                    val=mount_buffer.nReturnCode,
                    enum_class=constants.MountErrorCodes)))

    def dismount_volume(self, volume, ignore_open_files=False):
        drive_letter = chr(ord('A') + volume.drive_no)
        error_message_template = 'Dismount volume "{}" failed: {}'.format(
            drive_letter, '{}')

        # build the input/output struct
        dismount_buffer = driver_models.UnMountStruct()

        dismount_buffer.nDosDriveNo = volume.drive_no
        dismount_buffer.ignoreOpenFiles = wintypes.BOOL(ignore_open_files)
        p_dismount_buffer = ctypes.pointer(dismount_buffer)

        # run DeviceIoControl with the dismount_volume control code
        with DeviceIoControl(constants.VERACRYPT_DRIVER_PATH) as dctl:
            returned_count, _ = dctl.ioctl(
                constants.CtlCodes.TC_IOCTL_DISMOUNT_VOLUME.value,
                p_dismount_buffer, ctypes.sizeof(driver_models.UnMountStruct),
                p_dismount_buffer, ctypes.sizeof(driver_models.UnMountStruct))

        # check for failed execution
        if not returned_count:
            raise exceptions.DriverException(error_message_template.format(
                'DeviceIoControl call failed: {}'.format(
                    prepend_error_code_message(
                        val=ctypes.windll.kernel32.GetLastError(),
                        enum_class=win.constants.WinErrorCodes))))

        # check for struct alignment issues
        dismount_buffer.check_excess_buffer()

        # check for hidden volume protection trigger event
        if dismount_buffer.HiddenVolumeProtectionTriggered:
            raise exceptions.DriverException(error_message_template.format(
                'Hidden volume protection was trigered!'.format(drive_letter)))

        # check for failed return code from driver
        if not dismount_buffer.nReturnCode == 0:
            raise exceptions.DriverException(error_message_template.format(
                prepend_error_code_message(
                    val=dismount_buffer.nReturnCode,
                    enum_class=constants.UnMountErrorCodes)))
