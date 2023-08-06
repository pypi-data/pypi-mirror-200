# Built-in imports
import unittest

# Local imports
from .bch_primitives import Sats
from .role import Role
from .fee import (
    fees_from_role,
    fees_to_role,
    FeeAgreement,
)


fee_100000_taker_to_ss = FeeAgreement(name='a', amount_sats=Sats(100000), receiving=Role.SETTLEMENT_SERVICE, paying=Role.TAKER)
fee_200000_maker_to_ss = FeeAgreement(name='b', amount_sats=Sats(200000), receiving=Role.SETTLEMENT_SERVICE, paying=Role.MAKER)
fee_400000_ss_to_maker = FeeAgreement(name='c', amount_sats=Sats(400000), receiving=Role.MAKER, paying=Role.SETTLEMENT_SERVICE)
set_of_fees = [fee_100000_taker_to_ss, fee_200000_maker_to_ss, fee_400000_ss_to_maker]
expected_fees_from_ss = [fee_400000_ss_to_maker]
expected_fees_to_ss = [fee_100000_taker_to_ss, fee_200000_maker_to_ss]


class TestFeeFilters(unittest.TestCase):
    def test_fees_from_role(self):
        fees_from_taker = fees_from_role(fees=set_of_fees, role=Role.SETTLEMENT_SERVICE)
        self.assertCountEqual(fees_from_taker, expected_fees_from_ss)

    def test_fees_to_role(self):
        fees_to_ss = fees_to_role(fees=set_of_fees, role=Role.SETTLEMENT_SERVICE)
        self.assertCountEqual(fees_to_ss, expected_fees_to_ss)
