# Built-in imports
from enum import Enum


class Role(str, Enum):
    MAKER = 'Maker'
    TAKER = 'Taker'
    SETTLEMENT_SERVICE = 'Settlement Service'
    OTHER = 'Other'

    def __str__(self):
        return self.value

    def __repr__(self):
        return self.__str__()
