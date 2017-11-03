class BaseCryptInterface(object):
    """ Abstract interface for all Crypt Interfaces """

    def get_mounted_volumes(self):
        """ Retrieves a list of mounted volumes """

        raise NotImplementedError


class CryptInterface(BaseCryptInterface):
    """ Light wrapper over an interface, for dynamic switching """

    def __init__(self, interface_class, *args, **kwargs):
        self.interface = interface_class(*args, **kwargs)

    def get_mounted_volumes(self):
        return self.interface.get_mounted_volumes()
