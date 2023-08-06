# Library imports
from arrow import Arrow

# Local imports
from . import validators

DUST = 546
PUBLIC_KEY_BYTES_LENGTH = 33
SCRIPT_INT_MAX_WHEN_JAVASCRIPT = int(2 ** 53)
SATS_PER_BCH = int(1e8)
MAX_REASONABLE_SATS = int(10e6 * SATS_PER_BCH)  # 10 million BCH
MIN_NLOCKTIME_TIMESTAMP = 500_000_000


class PublicKey(str):
    """Validated BCH public key that can be used as a string."""
    def __init__(self, value):
        super().__init__()

        # don't allow silent coercion
        validators.instance(value, str)

        # use a strict format
        if self[:2].lower() == '0x':
            raise ValueError('public key should not include the 0x prefix')

        # require hex value validity
        try:
            bytes.fromhex(self)
        except Exception as e:
            raise ValueError(f'unable to interpret {self} as a hex string: {e}')

        # require strict length
        if len(self) != 2 * PUBLIC_KEY_BYTES_LENGTH:
            raise ValueError(f'public key should be 33 bytes but got {len(self) / 2} ({self})')


class ScriptTimestamp(int):
    """Validated BCH timestamp (seconds) that can be used as an integer."""
    def __init__(self, value):
        super().__init__()
        validators.instance(value, int)  # i.e. don't allow silent coercion
        validators.less_equal(self, SCRIPT_INT_MAX_WHEN_JAVASCRIPT)
        validators.greater_equal(self, MIN_NLOCKTIME_TIMESTAMP)

    def __str__(self):
        return f'{int(self)} ({Arrow.utcfromtimestamp(self)})'

    def __repr__(self):
        return self.__str__()

    @classmethod
    def earliest_possible(cls):
        return cls(MIN_NLOCKTIME_TIMESTAMP)

    @classmethod
    def latest_possible(cls):
        return cls(SCRIPT_INT_MAX_WHEN_JAVASCRIPT)


class Sats(int):
    """Validated amount of sats that can be used in calculations (positive or negative)."""
    _min_value = -MAX_REASONABLE_SATS

    def __init__(self, value):
        super().__init__()
        validators.instance(value, int)  # i.e. don't allow silent coercion
        validators.less_equal(self, MAX_REASONABLE_SATS)
        validators.greater_equal(self, self._min_value)

    @property
    def bch(self) -> float:
        return round(self / SATS_PER_BCH, ndigits=8)


class UtxoSats(Sats):
    """Validated amount of sats that can exist in a utxo."""
    _min_value = DUST
