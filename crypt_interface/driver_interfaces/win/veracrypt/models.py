from crypt_interface.driver_interfaces import win
from crypt_interface.driver_interfaces.win.veracrypt import constants
from crypt_interface.driver_interfaces.win.veracrypt.driver_models import (
    MountListStruct,)


class Volume(win.base_win_models.BaseVolume):
    @staticmethod
    def from_veracrypt_mount_list_struct(mount_list: MountListStruct,
                                         index: int):
        """ Converts an element of a MountListStruct to a BaseVolume

        :param mount_list: the instance from which the element is extracted
        :param index: the index of the element

        :rtype: Union[BaseVolume, None]
        :return: the created BaseVolume instance or None if it's not mounted
        """

        # quit early if no volume is mounted
        if not mount_list.wszVolume[index].value:
            return None

        # set args for a new BaseVolume instance
        volume = Volume()

        # since it has a volume name, it's mounted
        volume.is_mounted = True

        # determine the volume path
        volume.path = mount_list.wszVolume[index].value

        # trim the prefix from the path
        if volume.path.startswith('\\??\\'):
            volume.path = volume.path[4:]

        # get the volume label if any
        volume.label = mount_list.wszLabel[index].value

        # get the volume id
        volume.volume_id = bytes(
            mount_list.volumeID[index].value, 'utf-16', 'surrogatepass')

        # get the volume size
        volume.disk_length = mount_list.diskLength[index]

        # get the encryption algorithm
        volume.enc_algorithm = mount_list.ea[index]

        # try to convert it to the EncryptionAlgorithm enum
        try:
            volume.enc_algorithm = constants.EncryptionAlgorithm(
                volume.enc_algorithm)
        except ValueError:
            pass

        # get the volume type
        volume.volume_type = mount_list.volumeType[index]

        # try to convert it to the VolumeType enum
        try:
            volume.volume_type = constants.VolumeType(volume.volume_type)
        except ValueError:
            pass

        # get the TrueCrypt mode
        volume.truecrypt_mode = mount_list.truecryptMode[index]
        return volume

    @classmethod
    def mount_list_to_volume_list(cls, mount_list: MountListStruct):
        """ Converts a MountListStruct list to a list of Volumes

        :param mount_list: the instance which will be converted

        :rtype: List[BaseVolume]
        :return: the list of volumes
        """
        volumes = []
        for i in range(win.constants.MAX_VOLUMES):
            vol = cls.from_veracrypt_mount_list_struct(mount_list, i)
            if vol:
                volumes.append(vol)

        return volumes
