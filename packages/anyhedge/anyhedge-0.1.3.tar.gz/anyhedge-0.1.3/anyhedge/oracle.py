# Built-in imports
from __future__ import annotations
from codecs import decode
from dataclasses import dataclass
from functools import cached_property
from typing import (
    Sequence,
    Type,
)

# Library imports
from arrow import Arrow

# Local imports
from . import validators
from .bch_primitives import (
    PublicKey,
    ScriptTimestamp,
)

# Oracle prices are stored and limited to a 4 byte field.
# It may be unsigned, but I'm not sure so I use 31 bits to be safe
ORACLE_MAX_PRICE = (2 ** 31) - 1
GENERIC_4_BYTE_NUMBER = 2 ** 30


@dataclass(frozen=True)
class StrictPricepoints:
    """Sorted, unique pricepoints all from the same oracle"""
    all: tuple[Pricepoint, ...]

    def __post_init__(self):
        self._validate_pricepoints(self.all)

    @classmethod
    def new(cls, pricepoints: Sequence[Pricepoint]):
        unique_pricepoints = cls._make_pricepoints_unique(pricepoints)
        sorted_pricepoints = cls._sort_pricepoints(unique_pricepoints)
        cls._validate_pricepoints(sorted_pricepoints)
        return cls(sorted_pricepoints)

    @classmethod
    def _validate_pricepoints(cls, pricepoints: Sequence[Pricepoint]):
        # The point of separating validation and post_init is to allow direct
        # setting of values as well as using new() constructor.

        # first validate oracle pubkeys (raise an exception in any case if mixed oracles)
        if pricepoints:
            oracle_pubkey = pricepoints[0].oracle_pubkey
            for p in pricepoints:
                validators.equal(p.oracle_pubkey, oracle_pubkey)

        # ensure uniqueness. not efficient but performance is not yet an issue
        unique_pricepoints = cls._make_pricepoints_unique(pricepoints)
        validators.equal(pricepoints, unique_pricepoints)

        # ensure sorting. not efficient but performance is not yet an issue
        sorted_pricepoints = cls._sort_pricepoints(unique_pricepoints)
        validators.equal(unique_pricepoints, sorted_pricepoints)

    @staticmethod
    def _sort_pricepoints(pricepoints: Sequence[Pricepoint]) -> tuple[Pricepoint]:
        return tuple(sorted(pricepoints, key=lambda p: p.timestamp))

    @staticmethod
    def _make_pricepoints_unique(pricepoints: Sequence[Pricepoint]) -> tuple[Pricepoint]:
        lookup = {}
        for p in pricepoints:
            existing = lookup.get(p.timestamp)
            if existing is None:
                lookup[p.timestamp] = p
            else:
                if p == existing:
                    # it's an equal duplicate so just ignore it
                    pass
                else:
                    raise ValueError(f'same timestamp, same oracle, different value: {p} vs {existing}')
        return tuple(lookup.values())

    def __str__(self):
        return f'StrictPricepoints: {len(self.all)} prices for {self.all[0].oracleUnit_name}'

    def __repr__(self):
        return self.__str__()


def interleave_pricepoints(pricepoints_by_oracle_pubkey: dict[PublicKey, StrictPricepoints]) -> list[Pricepoint]:
    # TODO: There could be duplicates or bad overlapping messages hiding in this
    #       To solve that, make a formalized PricepointsByOracle class that strongly validates match between pubkey and pricepoints
    # let the optimized sorting algorithm sort it out even though we could do it in O(n) manually
    all_pricepoints = sum((list(p.all) for p in pricepoints_by_oracle_pubkey.values()), start=[])
    all_pricepoints.sort(key=lambda p: p.timestamp)
    return all_pricepoints


@dataclass(frozen=True)
class Pricepoint:
    oracle_pubkey: PublicKey
    message: str
    signature: str | None

    def __post_init__(self):
        # cheat for some early validation
        _, _, _, _ = self._message_parts

    def __str__(self):
        return f'{self.price_oracleUnits_per_bch} {self.oracleUnit_name} @ {self.timestamp} ({Arrow.utcfromtimestamp(self.timestamp)})'

    def __repr__(self):
        return self.__str__()

    @property
    def oracleUnit_name(self) -> str:
        return oracle_pubkey_to_unit_class[self.oracle_pubkey].name_of_oracleUnits

    @property
    def standardUnit_name(self) -> str:
        return oracle_pubkey_to_unit_class[self.oracle_pubkey].name_of_standardUnits

    @property
    def timestamp(self) -> ScriptTimestamp:
        return self._message_parts[0]

    @property
    def message_sequence(self) -> int:
        return self._message_parts[1]

    @property
    def price_sequence(self) -> int:
        return self._message_parts[2]

    @property
    def price_oracleUnits_per_bch(self) -> ScriptPriceInOracleUnitsPerBch:
        return ScriptPriceInOracleUnitsPerBch(self._message_parts[3])

    @property
    def price_standardUnits_per_bch(self) -> float:
        return float(self.price_oracleUnits_per_bch) / oracle_pubkey_to_unit_class[self.oracle_pubkey].oracleUnits_per_standardUnit

    @cached_property
    def _message_parts(self):
        # timestamp, message_sequence, price_sequence, price
        return parse_oracle_price_message(self.message)

    @classmethod
    def new_from_details(cls,
                         oracle_pubkey: PublicKey,
                         timestamp: ScriptTimestamp,
                         price_oracleUnits_per_bch: ScriptPriceInOracleUnitsPerBch,
                         message_sequence: int  = GENERIC_4_BYTE_NUMBER,
                         price_sequence: int  = GENERIC_4_BYTE_NUMBER,
                         signature: str | None = None,
                         ) -> Pricepoint:
        message_parts = []
        for data in (timestamp, message_sequence, price_sequence, price_oracleUnits_per_bch):
            message_parts.append(_swap_hex_endianness(f'{data:08x}'))
        message = ''.join(message_parts)
        pricepoint = Pricepoint(oracle_pubkey=oracle_pubkey, message=message, signature=signature)

        # do a sanity reverse check on the parsed values
        validators.equal(pricepoint.timestamp, timestamp)
        validators.equal(pricepoint.price_oracleUnits_per_bch, price_oracleUnits_per_bch)
        validators.equal(pricepoint.message_sequence, message_sequence)
        validators.equal(pricepoint.price_sequence, price_sequence)

        return pricepoint


class OracleUnit(float):
    name_of_oracleUnits: str = None
    name_of_standardUnits: str = None
    oracleUnits_per_standardUnit: int = None
    public_key: PublicKey = None

    def __init__(self, value):
        super().__init__()
        validators.instance(value, float)  # i.e. don't allow silent coercion
        # validators.greater_equal(self, 0)

    def __eq__(self, other: OracleUnit):
        if self.name_of_oracleUnits != other.name_of_oracleUnits:
            return False
        if self.name_of_standardUnits != other.name_of_standardUnits:
            return False
        if self.oracleUnits_per_standardUnit != other.oracleUnits_per_standardUnit:
            return False
        if self.public_key != other.public_key:
            return False
        if float(self) != float(other):
            return False
        return True

    def __hash__(self):
        return self.public_key

    @property
    def in_standard_units(self) -> float:
        return float(self) / self.oracleUnits_per_standardUnit


class ScriptPriceInOracleUnitsPerBch(int):
    def __new__(cls, value, *args, **kwargs):
        return super().__new__(cls, value)

    def __init__(self, value):
        super().__init__()
        validators.instance(value, int)  # i.e. don't allow silent coercion
        validators.less_equal(self, ORACLE_MAX_PRICE)
        validators.greater_equal(self, 1)


# GP Oracles
class BtcEM6(OracleUnit):
    name_of_oracleUnits = 'BTC(e-6)'
    name_of_standardUnits = 'BTC'
    oracleUnits_per_standardUnit = 1000000
    public_key = PublicKey('0245a107de5c6aabc9e7b976f26625b01474f90d1a7d11c180bec990b6938e731e')


class CnyEM2(OracleUnit):
    name_of_oracleUnits = 'CNY(e-2)'
    name_of_standardUnits = 'CNY'
    oracleUnits_per_standardUnit = 100
    public_key = PublicKey('030654b9598186fe4bc9e1b0490c6b85b13991cdb9a7afa34af1bbeee22a35487a')


class DogeEM1(OracleUnit):
    name_of_oracleUnits = 'DOGE(e-1)'
    name_of_standardUnits = 'DOGE'
    oracleUnits_per_standardUnit = 10
    public_key = PublicKey('02461db2aead56ea67543c8196a248152185cb824802a2e7ff12bfc2a493898b8f')


class EthEM5(OracleUnit):
    name_of_oracleUnits = 'ETH(e-5)'
    name_of_standardUnits = 'ETH'
    oracleUnits_per_standardUnit = 100000
    public_key = PublicKey('038ab22e37cf020f6bbef40111ddc51083a936f0821de56ac01f799cf15b87904d')


class InrEM0(OracleUnit):
    name_of_oracleUnits = 'INR'
    name_of_standardUnits = 'INR'
    oracleUnits_per_standardUnit = 1
    public_key = PublicKey('02e82ad82eb88fcdfd02fd5e2e0a67bc6ef4139bbcb63ce0b107a7604deb9f7ce1')


class UsdEM2(OracleUnit):
    name_of_oracleUnits = 'USD(e-2)'
    name_of_standardUnits = 'USD'
    oracleUnits_per_standardUnit = 100
    public_key = PublicKey('02d09db08af1ff4e8453919cc866a4be427d7bfe18f2c05e5444c196fcf6fd2818')


class XagEM3(OracleUnit):
    name_of_oracleUnits = 'XAG(e-3)'
    name_of_standardUnits = 'XAG'
    oracleUnits_per_standardUnit = 1000
    public_key = PublicKey('02712c349ebb7555b17bdbbe9f7aad5a337fa4179d0680eec3f6c8d77bac9cfa79')


class XauEM5(OracleUnit):
    name_of_oracleUnits = 'XAU(e-5)'
    name_of_standardUnits = 'XAU'
    oracleUnits_per_standardUnit = 100000
    public_key = PublicKey('021f8338ccd45a7790025de198a266f252ac43c95bf81d2469feff110beeac89dd')


# GP Beta Oracles
class BtcEM6Beta(OracleUnit):
    name_of_oracleUnits = 'BTC(e-6)'
    name_of_standardUnits = 'BTC'
    oracleUnits_per_standardUnit = 1000000
    public_key = PublicKey('03c22127c967bb28ec518fcc225164100df40470a1f6b457cd3a85adb051dcaa56')


class CnyEM2Beta(OracleUnit):
    name_of_oracleUnits = 'CNY(e-2)'
    name_of_standardUnits = 'CNY'
    oracleUnits_per_standardUnit = 100
    public_key = PublicKey('03c5e3e6a2fe9ed9be3c71a11e7808cf8428bc9ca48808d05a6fa2526865964f06')


class DogeEM1Beta(OracleUnit):
    name_of_oracleUnits = 'DOGE(e-1)'
    name_of_standardUnits = 'DOGE'
    oracleUnits_per_standardUnit = 10
    public_key = PublicKey('0330779426934d4fe5d18a3721e9eae246150501ebc537e866d2841369daeb0691')


class EthEM5Beta(OracleUnit):
    name_of_oracleUnits = 'ETH(e-5)'
    name_of_standardUnits = 'ETH'
    oracleUnits_per_standardUnit = 100000
    public_key = PublicKey('03518d199a4ca5dc06ecb1068416acde321df1b8d6f09149744b1e0fb38c92c92c')


class InrEM0Beta(OracleUnit):
    name_of_oracleUnits = 'INR'
    name_of_standardUnits = 'INR'
    oracleUnits_per_standardUnit = 1
    public_key = PublicKey('03994dc2c759375e98afbf5049383cd987001c346d0f11aa262c105874fb1390c3')


class UsdEM2Beta(OracleUnit):
    name_of_oracleUnits = 'USD(e-2)'
    name_of_standardUnits = 'USD'
    oracleUnits_per_standardUnit = 100
    public_key = PublicKey('02d3c1de9d4bc77d6c3608cbe44d10138c7488e592dc2b1e10a6cf0e92c2ecb047')


class XagEM3Beta(OracleUnit):
    name_of_oracleUnits = 'XAG(e-3)'
    name_of_standardUnits = 'XAG'
    oracleUnits_per_standardUnit = 1000
    public_key = PublicKey('03e9342b4d07dc35db0f555b80e19645b2a2a95a22675b50ead248d551a900fdec')


class XauEM5Beta(OracleUnit):
    name_of_oracleUnits = 'XAU(e-5)'
    name_of_standardUnits = 'XAU'
    oracleUnits_per_standardUnit = 100000
    public_key = PublicKey('03e980928f14fc98e1f9d75d15f0b67dc58cdd3f5c641b8f825b146bcc04bd232c')


# Very old GP Testing Oracles
class UsdEM2Testing(OracleUnit):
    name_of_oracleUnits = 'USD(e-2)'
    name_of_standardUnits = 'USD'
    oracleUnits_per_standardUnit = 100
    public_key = PublicKey('03e4a5b4a1d9365492dfcad9a05adcdea259acb51a20eabb84584f7aa3c7009ebe')


known_unit_classes = [
    BtcEM6, CnyEM2, DogeEM1, EthEM5, InrEM0, UsdEM2, XagEM3, XauEM5,
    BtcEM6Beta, CnyEM2Beta, DogeEM1Beta, EthEM5Beta, InrEM0Beta, UsdEM2Beta, XagEM3Beta, XauEM5Beta,
    UsdEM2Testing,
]
oracle_pubkey_to_unit_class: dict[PublicKey, Type[OracleUnit]] = {
    u.public_key: u
    for u in known_unit_classes
}


def parse_oracle_price_message(msg_hex: str) -> tuple[ScriptTimestamp, int, int, ScriptPriceInOracleUnitsPerBch]:
    """
    [0, 8) timestamp (4 bytes)
    [8, 16) message sequence (4 bytes)
    [16, 24) price sequence (4 bytes)
    [24, 32) price (4 bytes)
    """
    if len(msg_hex) != 32:
        raise ValueError(f'wrong byte-length ({len(msg_hex)/2}) for a price message (16)')

    # timestamp, msg_sequence, price_sequence/metadatatype should always parse and be valid
    timestamp = ScriptTimestamp(_parse_as_little_endian_signed_int(msg_hex[0:8]))
    msg_sequence = _parse_as_little_endian_signed_int(msg_hex[8:16])
    price_sequence = _parse_as_little_endian_signed_int(msg_hex[16:24])

    if price_sequence == 0:
        raise RuntimeError('this message is out of specification with price sequence == 0')
    elif price_sequence < 0:
        raise ValueError('this is a metadata message, not a price message')

    # Price should always parse and be valid if we get to this point. Unspecified error if not.
    price = ScriptPriceInOracleUnitsPerBch(_parse_as_little_endian_signed_int(msg_hex[24:]))

    return timestamp, msg_sequence, price_sequence, price


def _swap_hex_endianness(data_hex: str) -> str:
    data_bytes = bytearray.fromhex(data_hex)
    data_bytes.reverse()
    data_hex_reversed = ''.join(format(x, '02x') for x in data_bytes)
    return data_hex_reversed


def _parse_as_little_endian_signed_int(data_hex: str) -> int:
    data_bin = decode(data_hex, 'hex_codec')
    value = int.from_bytes(data_bin, byteorder='little', signed=True)
    return value
