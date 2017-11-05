import ctypes
import ctypes.wintypes as wintypes
from functools import partialmethod

from crypt_interface.driver_interfaces import win
from crypt_interface.driver_interfaces.win import base_win_driver_models
from crypt_interface.driver_interfaces.win.veracrypt import constants


class VCPConverters(base_win_driver_models.PConverters):

    enc_algorithm = partialmethod(
        base_win_driver_models.PConverters.enum_converter,
        enum_class=constants.EncryptionAlgorithm)

    volume_type = partialmethod(
        base_win_driver_models.PConverters.enum_converter,
        enum_class=constants.VolumeType)


class VCCConverters(base_win_driver_models.CConverters):
    bytes_to_password_text = partialmethod(
        base_win_driver_models.CConverters.bytestring_to_ubyte_array,
        size=constants.MAX_PASSWORD + 1)


# noinspection PyUnresolvedReferences
class MountListStruct(base_win_driver_models.BaseStruct):
    """ src/Common/Apidrvr.h: MOUNT_LIST_STRUCT """
    field_list = [
        # bitfield of all mounted drive letters
        base_win_driver_models.Field(
            name='ulMountedDrives', alias='mounted_drives',
            field_type=ctypes.c_uint32),

        # volume names of mounted volumes
        base_win_driver_models.Field(
            name='wszVolume', alias='path', field_type=(
                ctypes.c_wchar * constants.TC_MAX_PATH
                * win.win_constants.MAX_VOLUMES),
            is_indexed=True,
            converter=VCPConverters.wchar_array_path),

        # labels of mounted volumes
        base_win_driver_models.Field(
            name='wszLabel', alias='label', field_type=(
                ctypes.c_wchar * win.win_constants.VOLUME_LABEL_SIZE
                * win.win_constants.MAX_VOLUMES),
            is_indexed=True,
            converter=VCPConverters.wchar_array),

        # IDs of mounted volumes
        base_win_driver_models.Field(
            name='volumeID', alias='volume_id', field_type=(
                ctypes.c_wchar * win.win_constants.VOLUME_ID_SIZE
                * win.win_constants.MAX_VOLUMES),
            is_indexed=True,
            converter=VCPConverters.wchar_utf16_surrogate_pass_byte_array),

        # disk size in bytes
        base_win_driver_models.Field(
            name='diskLength', alias='disk_length', field_type=(
                ctypes.c_uint64 * win.win_constants.MAX_VOLUMES),
            is_indexed=True),

        # encryption algorithm
        base_win_driver_models.Field(
            name='ea', alias='enc_algorithm', field_type=(
                ctypes.c_int * win.win_constants.MAX_VOLUMES),
            is_indexed=True,
            converter=VCPConverters.enc_algorithm),

        # volume type (e.g. PROP_VOL_TYPE_OUTER, etc.)
        base_win_driver_models.Field(
            name='volumeType', alias='volume_type', field_type=(
                ctypes.c_int * win.win_constants.MAX_VOLUMES),
            is_indexed=True,
            converter=VCPConverters.volume_type),

        # truecrypt mode
        base_win_driver_models.Field(
            name='truecryptMode', alias='truecrypt_mode', field_type=(
                wintypes.BOOL * win.win_constants.MAX_VOLUMES),
            is_indexed=True,
            converter=VCPConverters.win_bool),
    ] + base_win_driver_models.BaseStruct.base_fields

    _fields_ = base_win_driver_models.Field.iterable_to_struct_fields(
        field_list)


# noinspection PyTypeChecker
class PasswordStruct(base_win_driver_models.BaseStruct):
    field_list = [
        base_win_driver_models.Field(
            name='Length', alias='length', field_type=ctypes.c_uint32),

        base_win_driver_models.Field(
            name='Text', alias='key',
            field_type=ctypes.c_ubyte * (constants.MAX_PASSWORD + 1)),

        # keep 64-bit alignment
        base_win_driver_models.Field(
            name='Pad', alias='_junk', field_type=ctypes.c_char * 3)
    ]

    _fields_ = base_win_driver_models.Field.iterable_to_struct_fields(
        field_list)


class MountStruct(base_win_driver_models.BaseStruct):
    """ src/Common/Apidrvr.h: MOUNT_STRUCT """

    field_list = [
        # return code from driver
        base_win_driver_models.Field(
            name='nReturnCode', alias='return_code', field_type=ctypes.c_int),

        base_win_driver_models.Field(
            name='FilesystemDirty', alias='fs_dirty',
            field_type=wintypes.BOOL),

        base_win_driver_models.Field(
            name='VolumeMountedReadOnlyAfterAccessDenied',
            alias='ro_after_access_denied', field_type=wintypes.BOOL),

        base_win_driver_models.Field(
            name='VolumeMountedReadOnlyAfterDeviceWriteProtected',
            alias='ro_after_write_protect', field_type=wintypes.BOOL),

        # volume to be mounted
        base_win_driver_models.Field(
            name='wszVolume', alias='path',
            field_type=ctypes.c_wchar * constants.TC_MAX_PATH),

        # user password
        base_win_driver_models.Field(
            name='VolumePassword', alias='password',
            field_type=PasswordStruct),

        # cache passwords in driver
        base_win_driver_models.Field(
            name='bCache', alias='password_cache_enabled',
            field_type=wintypes.BOOL),

        # drive number to mount
        base_win_driver_models.Field(
            name='nDosDriveNo', alias='drive_no', field_type=ctypes.c_int),

        base_win_driver_models.Field(
            name='BytesPerSector', alias='bytes_per_sector',
            field_type=ctypes.c_uint32),

        # mount volume in read-only mode
        base_win_driver_models.Field(
            name='bMountReadOnly', alias='read_only_enabled',
            field_type=wintypes.BOOL),

        # mount volume as removable media
        base_win_driver_models.Field(
            name='bMountRemovable', alias='removable_enabled',
            field_type=wintypes.BOOL),

        # open host file/device in exclusive access mode
        base_win_driver_models.Field(
            name='bExclusiveAccess', alias='exclusive_enabled',
            field_type=wintypes.BOOL),

        # announce volume to mount manager
        base_win_driver_models.Field(
            name='bMountManager', alias='manager_notification_enabled',
            field_type=wintypes.BOOL),

        # preserve file container timestamp
        base_win_driver_models.Field(
            name='bPreserveTimestamp', alias='timestamp_preservation_enabled',
            field_type=wintypes.BOOL),

        # If TRUE, we are to attempt to mount a partition located
        # on an encrypted system drive without
        # pre-boot authentication
        base_win_driver_models.Field(
            name='bPartitionInInactiveSysEncScope',
            alias='inactive_enclosing_enc_partition',
            field_type=wintypes.BOOL),

        # If bPartitionInInactiveSysEncScope is TRUE, this contains
        # the drive number of the system drive on which the
        # partition is located
        base_win_driver_models.Field(
            name='nPartitionInInactiveSysEncScopeDriveNo',
            alias='inactive_enclosing_enc_partition_drive_no',
            field_type=ctypes.c_int),

        base_win_driver_models.Field(
            name='SystemFavorite', alias='system_favorite',
            field_type=wintypes.BOOL),

        # TRUE if the user wants the hidden volume within this
        # volume to be
        # protected against being overwritten (damaged)
        base_win_driver_models.Field(
            name='bProtectHiddenVolume', alias='hidden_vol_protected',
            field_type=wintypes.BOOL),

        # Password to the hidden volume to be protected
        # against overwriting
        base_win_driver_models.Field(
            name='ProtectedHidVolPassword',
            alias='hidden_vol_password',
            field_type=PasswordStruct),

        base_win_driver_models.Field(
            name='UseBackupHeader', alias='use_backup_header',
            field_type=wintypes.BOOL),

        base_win_driver_models.Field(
            name='RecoveryMode', alias='recovery_mode',
            field_type=wintypes.BOOL),

        base_win_driver_models.Field(
            name='pkcs5_prf', alias='pkcs5_prf', field_type=ctypes.c_int),

        base_win_driver_models.Field(
            name='ProtectedHidVolPkcs5Prf', alias='hidden_vol_pkcs5_prf',
            field_type=ctypes.c_int),

        base_win_driver_models.Field(
            name='bTrueCryptMode', alias='truecrypt_mode',
            field_type=wintypes.BOOL),

        base_win_driver_models.Field(
            name='BytesPerPhysicalSector', alias='bytes_per_physical_sector',
            field_type=ctypes.c_uint32),

        base_win_driver_models.Field(
            name='VolumePim', alias='pim', field_type=ctypes.c_int),

        base_win_driver_models.Field(
            name='ProtectedHidVolPim', alias='hidden_vol_pim',
            field_type=ctypes.c_int),

        # maximum label length is 32 for NTFS and 11 for FAT32
        base_win_driver_models.Field(
            name='wszLabel', alias='label',
            field_type=ctypes.c_wchar * win.win_constants.VOLUME_LABEL_SIZE),

        base_win_driver_models.Field(
            name='bIsNTFS', alias='is_ntfs', field_type=wintypes.BOOL),

        base_win_driver_models.Field(
            name='bDriverSetLabel', alias='driver_set_label',
            field_type=wintypes.BOOL),

        base_win_driver_models.Field(
            name='bCachePim', alias='pim_cache_enabled',
            field_type=wintypes.BOOL),

        base_win_driver_models.Field(
            name='MaximumTransferLength', alias='max_transfer_length',
            field_type=wintypes.ULONG),

        base_win_driver_models.Field(
            name='MaximumPhysicalPages', alias='max_physical_pages',
            field_type=wintypes.ULONG),

        base_win_driver_models.Field(
            name='AlignmentMask', alias='alignment_mask',
            field_type=wintypes.ULONG),
    ] + base_win_driver_models.BaseStruct.base_fields

    _fields_ = base_win_driver_models.Field.iterable_to_struct_fields(
        field_list)


class UnMountStruct(base_win_driver_models.BaseStruct):
    """ src/Common/Apidrvr.h: UNMOUNT_STRUCT """

    field_list = [
        # drive letter to unmount
        base_win_driver_models.Field(
            name='nDosDriveNo', alias='drive_no',
            field_type=ctypes.c_int),

        base_win_driver_models.Field(
            name='ignoreOpenFiles', alias='ignore_open_files_enabled',
            field_type=wintypes.BOOL),

        base_win_driver_models.Field(
            name='HiddenVolumeProtectionTriggered',
            alias='hidden_vol_protection_triggered',
            field_type=wintypes.BOOL),

        # return code back from the driver
        base_win_driver_models.Field(
            name='nReturnCode', alias='return_code',
            field_type=ctypes.c_int),
    ] + base_win_driver_models.BaseStruct.base_fields

    _fields_ = base_win_driver_models.Field.iterable_to_struct_fields(
        field_list)
