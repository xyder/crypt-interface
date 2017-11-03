class BaseVolume(object):
    """ Holds information about an encrypted BaseVolume """

    def __init__(self):
        self.is_mounted = False
        self.path = ''
        self.label = ''
        self.volume_id = b''
        self.disk_length = 0
        self.enc_algorithm = 0
        self.volume_type = 0
        self.truecrypt_mode = False

    def __repr__(self):
        return '<{}: {}>'.format(self.__class__.__name__, self.__dict__)

    __str__ = __repr__
