import ctypes
import ctypes.wintypes as wintypes
from enum import Enum

from crypt_interface.driver_interfaces import base_constants


# CTL codes constants
FILE_DEVICE_UNKNOWN = 0x00000022
METHOD_BUFFERED = 0x00000000
FILE_ANY_ACCESS = 0x00000000

# other
LPDWORD = ctypes.POINTER(wintypes.DWORD)
LPOVERLAPPED = wintypes.LPVOID
LPSECURITY_ATTRIBUTES = wintypes.LPVOID

INVALID_HANDLE = wintypes.HANDLE(-1)

NULL = 0
FALSE = wintypes.BOOL(False)
TRUE = wintypes.BOOL(True)

VOLUME_ID_SIZE = 32
VOLUME_LABEL_SIZE = 33
MAX_VOLUMES = 26


class GenericAccessRights(Enum):
    READ = 0x80000000
    WRITE = 0x40000000
    EXECUTE = 0x20000000
    ALL = 0x10000000
    NONE = 0x00000000


class ShareMode(Enum):
    READ = 0x00000001
    WRITE = 0x00000002
    DELETE = 0x00000004
    NONE = 0x00000000
    READ_WRITE = READ | WRITE


class CreationDisposition(Enum):
    CREATE_NEW = 1
    CREATE_ALWAYS = 2
    OPEN_EXISTING = 3
    OPEN_ALWAYS = 4
    TRUNCATE_EXISTING = 5


class FileAttributes(Enum):
    NORMAL = 0x00000080


class WinErrorCodes(base_constants.PrintableEnum):
    """ Source:
        https://msdn.microsoft.com/en-us/library/windows/desktop/ms681381(v=vs.85).aspx
    """

    # cannot access the file because it is being used by another process
    ERROR_SHARING_VIOLATION = 32

    # the data passed to a system call is too small
    ERROR_INSUFFICIENT_BUFFER = 122

WinErrorCodes._labels = {
    WinErrorCodes.ERROR_SHARING_VIOLATION: 'File is in use.',
    WinErrorCodes.ERROR_INSUFFICIENT_BUFFER: 'Data passed is too small.'
}
