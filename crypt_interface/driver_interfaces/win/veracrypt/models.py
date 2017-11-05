from crypt_interface.driver_interfaces import win
from crypt_interface.driver_interfaces.win.veracrypt.driver_models import (
    MountListStruct,)


class Volume(win.base_win_models.BaseVolume):
    @staticmethod
    def from_veracrypt_mount_list_struct(
            mount_list: MountListStruct, index: int):
        """ Converts an element of a MountListStruct to a Volume

        :param mount_list: the instance from which the element is extracted
        :param index: the index of the element

        :rtype: Union[BaseVolume, None]
        :return: the created BaseVolume instance or None if it's not mounted
        """

        volume = Volume()

        win.base_driver_models.Field.struct_to_object(
            volume, mount_list, index)

        # if path is None, the volume is not mounted
        if not volume.path:
            return

        volume.is_mounted = True
        volume.drive_no = index

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
