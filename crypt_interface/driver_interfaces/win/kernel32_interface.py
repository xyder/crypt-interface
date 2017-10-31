import ctypes
from ctypes import wintypes

from crypt_interface.driver_interfaces.exceptions import DriverException
from crypt_interface.driver_interfaces.win import constants


def ctl_code(device_type, func, method, access):
    """ Equivalent of:
    CTL_CODE (DEVICE, FUNC, METHOD, ACCESS))
    """

    return (device_type << 16) | (access << 14) | (func << 2) | method


def configure_create_file_function():
    """ Initializez the CreateFileW function signature """

    create_file_func = ctypes.windll.kernel32.CreateFileW
    create_file_func.argtypes = [
        # (in) LPCTSTR lpFileName
        wintypes.LPWSTR,
        # (in) DWORD dwDesiredAccess
        wintypes.DWORD,
        # (in) DWORD dwShareMode
        wintypes.DWORD,
        # (in, opt) LPSECURITY_ATTRIBUTES lpSecurityAttributes
        constants.LPSECURITY_ATTRIBUTES,
        # (in) DWORD dwCreationDisposition
        wintypes.DWORD,
        # (in) DWORD dwFlagsAndAttributes
        wintypes.DWORD,
        # (in, opt) HANDLE hTemplateFile
        wintypes.HANDLE]
    create_file_func.restype = wintypes.HANDLE


def configure_deviceiocontrol_function():
    """ Initializez the DeviceIoControl function signature """

    device_io_ctrl_func = ctypes.windll.kernel32.DeviceIoControl
    device_io_ctrl_func.argtypes = [
        # (in) HANDLE hDevice
        wintypes.HANDLE,
        # (in) DWORD dwIoControlCode
        wintypes.DWORD,
        # (in, opt)  LPVOID lpInBuffer
        wintypes.LPVOID,
        # (in) DWORD nInBufferSize
        wintypes.DWORD,
        # (out, opt) LPVOID lpOutBuffer
        wintypes.LPVOID,
        # (in) DWORD nOutBufferSize
        wintypes.DWORD,
        # (out, opt) LPDWORD lpBytesReturned
        constants.LPDWORD,
        # (in, out, opt)   LPOVERLAPPED lpOverlapped
        constants.LPOVERLAPPED]
    device_io_ctrl_func.restype = wintypes.BOOL


def create_file(filename, access, mode, creation, flags):
    """ Interface for CreateFile function

        Documentation:
        http://msdn.microsoft.com/en-us/library/windows/desktop/aa363858(v=vs.85).aspx

    :param filename: the name of the file/device to be created/opened
    :param access: file/device request access rights
    :param mode: file/device request sharing mode
    :param creation: action to take if file/device already exists or not
    :param flags: the file/device attributes
    """

    create_func = ctypes.windll.kernel32.CreateFileW
    handle = create_func(filename, access.value, mode.value, constants.NULL,
                         creation.value, flags, constants.NULL)

    return wintypes.HANDLE(handle)


def device_ioctl(device, control_code, in_buffer,
                 in_size, out_buffer, out_size):
    """ Interface for DeviceIoControl function
        Documentation
        http://msdn.microsoft.com/en-us/library/aa363216(v=vs.85).aspx
    """

    device_ioctl_func = ctypes.windll.kernel32.DeviceIoControl

    # allocate a DWORD, and take its reference
    returned = wintypes.DWORD(0)
    pointer_returned = ctypes.byref(returned)

    status = device_ioctl_func(device, control_code, in_buffer, in_size,
                               out_buffer, out_size, pointer_returned, None)

    return status, returned


class DeviceIoControl(object):
    """ Context Manager for DeviceIOControl """

    def __init__(self, path):
        self.path = path
        self._handle = None

    def _validate_handle(self):
        """ Validates the device/file handle """

        if self._handle is None:
            raise DriverException('No file handle')

        if self._handle.value == constants.INVALID_HANDLE.value:
            raise DriverException(
                'Failed to open {}. GetLastError(): {}'.format(
                    self.path, ctypes.windll.kernel32.GetLastError()))

    def ioctl(self, control_code, in_buffer, in_size, out_buffer, out_size):
        """ Calls the DeviceIOControl function

        :param control_code: the control code of the method
        :param in_buffer: input buffer
        :param in_size: size of the input buffer
        :param out_buffer: output buffer
        :param out_size: size of the output buffer
        :return: the return value of the DeviceIOControl call, a tuple which
        contains the returned bytes count as first element
        """

        self._validate_handle()
        return device_ioctl(self._handle, control_code, in_buffer,
                            in_size, out_buffer, out_size)

    def __enter__(self):
        self._handle = create_file(
            self.path,
            constants.GenericAccessRights.READ,
            constants.ShareMode.READ_WRITE,
            constants.CreationDisposition.OPEN_EXISTING,
            0)
        self._validate_handle()
        return self

    def __exit__(self, typ, val, tb):
        self._validate_handle()
        ctypes.windll.kernel32.CloseHandle(self._handle)
