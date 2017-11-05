from enum import Enum


class PrintableEnum(Enum):
    def __repr__(self):
        return getattr(self, '_labels', {}).get(self, self.name)

    __str__ = __repr__
