# Built-in imports
import unittest

# Library imports
from arrow import Arrow

# Local imports
from .bch_primitives import (
    SATS_PER_BCH,
    Sats,
    ScriptTimestamp,
    UtxoSats,
)
from .contract import (
    ContractFunding,
    ContractProposal,
    LongLeverage,
    NominalOracleUnitsXSatsPerBch,
    RedemptionType,
    Side,
    UnredeemableError,
)
from .fee import FeeAgreement
from .oracle import (
    OracleUnit,
    ScriptPriceInOracleUnitsPerBch,
    UsdEM2Beta,
)
from .role import Role


###################
# Contract Tests
###################
# Generic intent values, not always perfectly reproducible from the contract
START_TIMESTAMP = ScriptTimestamp(Arrow(year=2021, month=10, day=21).int_timestamp)
MATURITY_TIMESTAMP = ScriptTimestamp(Arrow(year=2021, month=10, day=23).int_timestamp)  # 2 days later
NOMINAL_USDEM2 = UsdEM2Beta(100_00.0)  # $100.00
LONG_LEVERAGE = LongLeverage(4.5)
START_PRICE_USDEM2_PER_BCH = ScriptPriceInOracleUnitsPerBch(200_00)  # $200.00 / BCH

# Derived values

# The compound nominal value is a giant number stored in the original AnyHedge contract and needed
# to get around the lack of multiplication by optimizing the contract into a single division operation
# = NominalOracleUnitsXSatsPerBch(round(NOMINAL_USDEM2 * SATS_PER_BCH))
DERIVED_NOMINAL_UNITS_X_SATS_PER_BCH = NominalOracleUnitsXSatsPerBch(1_000_000_000_000)

# Long liquidation Price is the price where total bch covers exactly nominal units
# At this price, the long party is liquidated (has no funds remaining in the contract)
# Calculate as round(START_PRICE_USDEM2_PER_BCH * (1 - 1 / LONG_LEVERAGE))
# $155.56 / BCH
DERIVED_LONG_LIQUIDATION_PRICE = ScriptPriceInOracleUnitsPerBch(155_56)

# Short liquidation Price is the price where the short party is
# liquidated (has no funds remaining in the contract). In the current design of
# AnyHedge where hedge is always a 1x short, there is no meaningful short
# liquidation price. In the real contract, there is a "high" settlement price
# that can trigger early settlement, but it is an unused contract feature
# rather than a liquidation price.
NO_SHORT_LIQUIDATION_PRICE = None

# The bch amount to cover the initial nominal units at the start price
# = round(NOMINAL_USDEM2 * SATS_PER_BCH / START_PRICE_USDEM2_PER_BCH)
# 0.5 BCH
DERIVED_HEDGE_INPUT_SATS = UtxoSats(50_000_000)

# The total bch amount needed to cover nominal units at liquidation
# Calculated as ceil((NOMINAL_USDEM2 * SATS_PER_BCH) / DERIVED_LIQUIDATION_PRICE_UNITS_PER_BCH)
DERIVED_TOTAL_INPUT_SATS = UtxoSats(64_283_878)

# The bch amount to provide volatility protection as specified by the multiplier
# This is the amount to cover the difference between hedge bch at start and hedge bch at liquidation
# Calculated as DERIVED_TOTAL_INPUT_SATS - DERIVED_HEDGE_INPUT_SATS
DERIVED_LONG_INPUT_SATS = UtxoSats(14_283_878)

# Converting the input amounts into original units at start
# for hedge, it's DERIVED_NOMINAL_UNITS_X_SATS_PER_BCH / SATS_PER_BCH
DERIVED_HEDGE_INPUT_ORACLE_UNITS = UsdEM2Beta(100_00.0)
# for long, it's DERIVED_LONG_INPUT_SATS * START_PRICE_USDEM2_PER_BCH / SATS_PER_BCH
DERIVED_LONG_INPUT_ORACLE_UNITS = UsdEM2Beta(2856.7756)
DERIVED_TOTAL_INPUT_ORACLE_UNITS = UsdEM2Beta(DERIVED_HEDGE_INPUT_ORACLE_UNITS + DERIVED_LONG_INPUT_ORACLE_UNITS)


def standard_contract_proposal(
    start_timestamp: ScriptTimestamp = START_TIMESTAMP,
    maturity_timestamp: ScriptTimestamp = MATURITY_TIMESTAMP,
    nominal_oracleUnits: OracleUnit = NOMINAL_USDEM2,
    long_leverage: LongLeverage = LONG_LEVERAGE,
    start_price_oracleUnits_per_bch: ScriptPriceInOracleUnitsPerBch = START_PRICE_USDEM2_PER_BCH,
    maker_side: Side = Side.HEDGE,
) -> ContractProposal:
    return ContractProposal.new_from_intent(
        start_timestamp=start_timestamp,
        maturity_timestamp=maturity_timestamp,
        nominal_oracleUnits=nominal_oracleUnits,
        long_leverage=long_leverage,
        start_price_oracleUnits_per_bch=start_price_oracleUnits_per_bch,
        maker_side=maker_side,
    )


class TestContractProposalDerivedValues(unittest.TestCase):
    ######################
    # Exact contract parameters, some root values, some derived from root values
    ######################
    def test_nominal_oracleUnits_x_satsPerBch(self):
        self.assertEqual(standard_contract_proposal().nominal_oracleUnits_x_satsPerBch, DERIVED_NOMINAL_UNITS_X_SATS_PER_BCH)

    def test_long_liquidation_price_oracleUnits_per_bch(self):
        self.assertEqual(standard_contract_proposal().long_liquidation_price_oracleUnits_per_bch, DERIVED_LONG_LIQUIDATION_PRICE)

    def test_short_liquidation_price_oracleUnits_per_bch(self):
        # Until two-sided leverage is enabled in AnyHedge, this is always None
        self.assertEqual(standard_contract_proposal().short_liquidation_price_oracleUnits_per_bch, NO_SHORT_LIQUIDATION_PRICE)

    def test_maker_side(self):
        self.assertEqual(standard_contract_proposal().maker_side, Side.HEDGE)

    ######################
    # Exact secondary values derived from contract parameters
    ######################
    def test_hedge_input_sats(self):
        self.assertEqual(standard_contract_proposal().hedge_input_sats, DERIVED_HEDGE_INPUT_SATS)

    def test_total_input_sats(self):
        self.assertEqual(standard_contract_proposal().total_input_sats, DERIVED_TOTAL_INPUT_SATS)

    def test_long_input_sats(self):
        self.assertEqual(standard_contract_proposal().long_input_sats, DERIVED_LONG_INPUT_SATS)

    ######################
    # Reverse calculated intent values from the contract's perspective
    ######################
    def test_effective_long_leverage(self):
        self.assertAlmostEqual(standard_contract_proposal().effective_long_leverage, LONG_LEVERAGE, delta=.001)

    ######################
    # Unit values
    ######################
    def test_total_input_oracleUnits(self):
        self.assertEqual(standard_contract_proposal().total_input_oracleUnits, DERIVED_TOTAL_INPUT_ORACLE_UNITS)

    def test_hedge_input_oracleUnits(self):
        self.assertEqual(standard_contract_proposal().hedge_input_oracleUnits, DERIVED_HEDGE_INPUT_ORACLE_UNITS)

    def test_long_input_oracleUnits(self):
        self.assertEqual(standard_contract_proposal().long_input_oracleUnits, DERIVED_LONG_INPUT_ORACLE_UNITS)

    ######################
    # Role versions of values
    ######################
    def test_all_sided_values(self):
        hedge_maker_contract = standard_contract_proposal(maker_side=Side.HEDGE)
        self.assertEqual(hedge_maker_contract.maker_side, Side.HEDGE)
        self.assertEqual(hedge_maker_contract.taker_side, Side.LONG)
        self.assertEqual(hedge_maker_contract.maker_input_sats, DERIVED_HEDGE_INPUT_SATS)
        self.assertEqual(hedge_maker_contract.taker_input_sats, DERIVED_LONG_INPUT_SATS)
        self.assertEqual(hedge_maker_contract.maker_input_oracleUnits, DERIVED_HEDGE_INPUT_ORACLE_UNITS)
        self.assertEqual(hedge_maker_contract.taker_input_oracleUnits, DERIVED_LONG_INPUT_ORACLE_UNITS)

        long_maker_contract = standard_contract_proposal(maker_side=Side.LONG)
        self.assertEqual(long_maker_contract.maker_side, Side.LONG)
        self.assertEqual(long_maker_contract.taker_side, Side.HEDGE)
        self.assertEqual(long_maker_contract.maker_input_sats, DERIVED_LONG_INPUT_SATS)
        self.assertEqual(long_maker_contract.taker_input_sats, DERIVED_HEDGE_INPUT_SATS)
        self.assertEqual(long_maker_contract.maker_input_oracleUnits, DERIVED_LONG_INPUT_ORACLE_UNITS)
        self.assertEqual(long_maker_contract.taker_input_oracleUnits, DERIVED_HEDGE_INPUT_ORACLE_UNITS)

    ######################
    # Role versions of values
    ######################
    def test_parameterized_lookup_error_on_invalid_combinations(self):
        maker_hedge_contract = standard_contract_proposal(maker_side=Side.HEDGE)
        with self.assertRaises(ValueError):
            maker_hedge_contract.input_sats(role=Role.MAKER, side=Side.LONG)
        with self.assertRaises(ValueError):
            maker_hedge_contract.input_sats(role=Role.TAKER, side=Side.HEDGE)

        taker_hedge_contract = standard_contract_proposal(maker_side=Side.LONG)
        with self.assertRaises(ValueError):
            taker_hedge_contract.input_sats(role=Role.TAKER, side=Side.LONG)
        with self.assertRaises(ValueError):
            taker_hedge_contract.input_sats(role=Role.MAKER, side=Side.HEDGE)


class TestContractProposalValidation(unittest.TestCase):
    def test_ValueError_if_duration_too_short(self):
        with self.assertRaises(ValueError):
            too_short_maturity_timestamp = ScriptTimestamp(START_TIMESTAMP + 60 - 1)
            standard_contract_proposal(maturity_timestamp=too_short_maturity_timestamp)


# Create the standard set of fees
FEE_100000_TAKER_TO_MAKER = FeeAgreement(name='fee type a', amount_sats=Sats(100000), receiving=Role.MAKER, paying=Role.TAKER)
FEE_200000_TAKER_TO_MAKER = FeeAgreement(name='fee type b', amount_sats=Sats(200000), receiving=Role.MAKER, paying=Role.TAKER)
FEE_400000_TAKER_TO_SETTLEMENT_SERVICE = FeeAgreement(name='fee type ss', amount_sats=Sats(400000), receiving=Role.SETTLEMENT_SERVICE, paying=Role.TAKER)
FEES = [FEE_100000_TAKER_TO_MAKER, FEE_200000_TAKER_TO_MAKER, FEE_400000_TAKER_TO_SETTLEMENT_SERVICE]


# Group them for reference
TOTAL_FEES_TO_MAKER_SATS = Sats(
    + FEE_100000_TAKER_TO_MAKER.amount_sats
    + FEE_200000_TAKER_TO_MAKER.amount_sats
)
DERIVED_TOTAL_FEES_TO_MAKER_ORACLE_UNITS = UsdEM2Beta(TOTAL_FEES_TO_MAKER_SATS * START_PRICE_USDEM2_PER_BCH / SATS_PER_BCH)
TOTAL_FEES_TO_TAKER_SATS = Sats(
    - FEE_100000_TAKER_TO_MAKER.amount_sats
    - FEE_200000_TAKER_TO_MAKER.amount_sats
    - FEE_400000_TAKER_TO_SETTLEMENT_SERVICE.amount_sats
)
DERIVED_TOTAL_FEES_TO_TAKER_ORACLE_UNITS = UsdEM2Beta(TOTAL_FEES_TO_TAKER_SATS * START_PRICE_USDEM2_PER_BCH / SATS_PER_BCH)


def standard_contract_funding(proposal: ContractProposal | None = None) -> ContractFunding:
    proposal = proposal or standard_contract_proposal()
    return proposal.fund(fee_agreements=FEES)


class TestContractFundingDerivedValues(unittest.TestCase):
    def test_fee_sats_to_side(self):
        # Confirm hedge maker and long taker
        hedge_maker_contract = standard_contract_funding(standard_contract_proposal(maker_side=Side.HEDGE))
        long_maker_contract = standard_contract_funding(standard_contract_proposal(maker_side=Side.LONG))

        expected_fees_sats_to_maker = TOTAL_FEES_TO_MAKER_SATS
        expected_fees_sats_to_taker = TOTAL_FEES_TO_TAKER_SATS

        # Hedge Maker
        self.assertEqual(hedge_maker_contract.fee_sats_to_hedge, expected_fees_sats_to_maker)
        self.assertEqual(hedge_maker_contract.fee_sats_to_maker, expected_fees_sats_to_maker)

        # Long Taker
        self.assertEqual(hedge_maker_contract.fee_sats_to_long, expected_fees_sats_to_taker)
        self.assertEqual(hedge_maker_contract.fee_sats_to_taker, expected_fees_sats_to_taker)

        # Long Maker
        self.assertEqual(long_maker_contract.fee_sats_to_long, expected_fees_sats_to_maker)
        self.assertEqual(long_maker_contract.fee_sats_to_maker, expected_fees_sats_to_maker)

        # Hedge Taker
        self.assertEqual(long_maker_contract.fee_sats_to_hedge, expected_fees_sats_to_taker)
        self.assertEqual(long_maker_contract.fee_sats_to_taker, expected_fees_sats_to_taker)

    def test_fee_oracleUnits_to_side(self):
        # Confirm hedge maker and long taker
        hedge_maker_contract = standard_contract_funding(standard_contract_proposal(maker_side=Side.HEDGE))
        long_maker_contract = standard_contract_funding(standard_contract_proposal(maker_side=Side.LONG))
        oracle_class = hedge_maker_contract.base_proposal.oracle_unit_cls

        expected_fee_oracleUnits_to_maker_at_funding = oracle_class(TOTAL_FEES_TO_MAKER_SATS * START_PRICE_USDEM2_PER_BCH / SATS_PER_BCH)
        expected_fee_oracleUnits_to_taker_at_funding = oracle_class(TOTAL_FEES_TO_TAKER_SATS * START_PRICE_USDEM2_PER_BCH / SATS_PER_BCH)

        # Hedge Maker
        self.assertEqual(hedge_maker_contract.fee_oracleUnits_to_hedge, expected_fee_oracleUnits_to_maker_at_funding)
        self.assertEqual(hedge_maker_contract.fee_oracleUnits_to_maker, expected_fee_oracleUnits_to_maker_at_funding)

        # Long Taker
        self.assertEqual(hedge_maker_contract.fee_oracleUnits_to_long, expected_fee_oracleUnits_to_taker_at_funding)
        self.assertEqual(hedge_maker_contract.fee_oracleUnits_to_taker, expected_fee_oracleUnits_to_taker_at_funding)

        # Long Maker
        self.assertEqual(long_maker_contract.fee_oracleUnits_to_long, expected_fee_oracleUnits_to_maker_at_funding)
        self.assertEqual(long_maker_contract.fee_oracleUnits_to_maker, expected_fee_oracleUnits_to_maker_at_funding)

        # Hedge Taker
        self.assertEqual(long_maker_contract.fee_oracleUnits_to_hedge, expected_fee_oracleUnits_to_taker_at_funding)
        self.assertEqual(long_maker_contract.fee_oracleUnits_to_taker, expected_fee_oracleUnits_to_taker_at_funding)


# Valid timestamp, just before maturity
BEFORE_MATURITY_TIMESTAMP = ScriptTimestamp(MATURITY_TIMESTAMP - 1)

# A valid maturity price, just somewhat over the start price so no chance of low liquidation
NAIVE_MATURITY_PRICE_USDEM2_PER_BCH = ScriptPriceInOracleUnitsPerBch(220_00)  # $220.00
BELOW_LIQUIDATING_PRICE_USDEM2_PER_BCH = ScriptPriceInOracleUnitsPerBch(DERIVED_LONG_LIQUIDATION_PRICE - 10)


class TestMaturityRedemption(unittest.TestCase):
    def test_matures_at_maturity_time(self):
        redemption = standard_contract_funding().redeem(
            price_timestamp=MATURITY_TIMESTAMP,
            price_oracleUnits_per_bch=NAIVE_MATURITY_PRICE_USDEM2_PER_BCH,
            force_maturity=False,
        )
        self.assertEqual(redemption.redemption_type, RedemptionType.MATURATION)

    def test_matures_at_maturity_time_even_if_liquidating_price(self):
        redemption = standard_contract_funding().redeem(
            price_timestamp=MATURITY_TIMESTAMP,
            price_oracleUnits_per_bch=DERIVED_LONG_LIQUIDATION_PRICE,
            force_maturity=False,
        )
        self.assertEqual(redemption.redemption_type, RedemptionType.MATURATION)

    def test_fails_to_mature_before_maturity_time(self):
        with self.assertRaises(UnredeemableError):
            standard_contract_funding().redeem(
                price_timestamp=BEFORE_MATURITY_TIMESTAMP,
                price_oracleUnits_per_bch=NAIVE_MATURITY_PRICE_USDEM2_PER_BCH,
                force_maturity=False,
            )

    def test_liquidates_before_maturity_time_at_low_liquidation_price(self):
        redemption = standard_contract_funding().redeem(
            price_timestamp=BEFORE_MATURITY_TIMESTAMP,
            price_oracleUnits_per_bch=DERIVED_LONG_LIQUIDATION_PRICE,
            force_maturity=False,
        )
        self.assertEqual(redemption.redemption_type, RedemptionType.LIQUIDATION)

    def test_fails_to_liquidate_before_maturity_time_at_one_over_low_liquidation_price(self):
        valid_liquidation_timestamp = ScriptTimestamp(MATURITY_TIMESTAMP - 1)
        one_over_liquidation_price = ScriptPriceInOracleUnitsPerBch(DERIVED_LONG_LIQUIDATION_PRICE + 1)
        with self.assertRaises(UnredeemableError):
            standard_contract_funding().redeem(
                price_timestamp=valid_liquidation_timestamp,
                price_oracleUnits_per_bch=one_over_liquidation_price,
                force_maturity=False,
            )

    def test_maturation_works_if_force(self):
        too_early_maturation_timestamp = ScriptTimestamp(MATURITY_TIMESTAMP - 1)
        redemption = standard_contract_funding().redeem(
            price_timestamp=too_early_maturation_timestamp,
            price_oracleUnits_per_bch=NAIVE_MATURITY_PRICE_USDEM2_PER_BCH,
            force_maturity=True,
        )
        self.assertEqual(redemption.redemption_type, RedemptionType.MATURATION)


###################
# Redeemed Contract Tests
###################
# Derived hedge payout sats and units
# Calculated as max(dust, HEDGE_COMPOSITE // CLAMPED_PRICE) (Note the integer division //)
DERIVED_HEDGE_PAYOUT_SATS = UtxoSats(45_454_545)  # 0.45454545... Bch
# Calculated as DERIVED_HEDGE_PAYOUT_SATS * MATURITY_PRICE / SATS_PER_BCH
DERIVED_HEDGE_PAYOUT_ORACLE_UNITS = UsdEM2Beta(9999.999900)  # 99.99999900000 USD

# Derived long payout sats and units
# Calculated as max(dust, TOTAL_INPUT - HEDGE_PAYOUT)
DERIVED_LONG_PAYOUT_SATS = UtxoSats(18_829_333)  # 0.18829... Bch
# Calculated as DERIVED_LONG_PAYOUT_SATS * MATURITY_PRICE / SATS_PER_BCH
DERIVED_LONG_PAYOUT_ORACLE_UNITS = UsdEM2Beta(4142.45326)

# Derived total payout sats and units
# Calculated as hedge + long
DERIVED_TOTAL_PAYOUT_SATS = UtxoSats(64283878)
# Calculated as DERIVED_HEDGE_PAYOUT_ORACLE_UNITS + DERIVED_LONG_PAYOUT_ORACLE_UNITS
DERIVED_TOTAL_PAYOUT_ORACLE_UNITS = UsdEM2Beta(14142.4532)


def standard_maturation(
        funding: ContractFunding | None = None
):
    funding = funding if funding is not None else standard_contract_funding()
    return funding.redeem(
        price_timestamp=MATURITY_TIMESTAMP,
        price_oracleUnits_per_bch=NAIVE_MATURITY_PRICE_USDEM2_PER_BCH,
        force_maturity=False,
    )


def standard_liquidation(
    price_timestamp: ScriptTimestamp = MATURITY_TIMESTAMP,
    price_oracleUnits_per_bch: ScriptPriceInOracleUnitsPerBch = DERIVED_LONG_LIQUIDATION_PRICE,
    force_maturity: bool = False,
):
    return standard_contract_funding().redeem(
        price_timestamp=price_timestamp,
        price_oracleUnits_per_bch=price_oracleUnits_per_bch,
        force_maturity=force_maturity,
    )


class TestNewRedemptionDerivedValues(unittest.TestCase):
    ######################
    # Exact secondary values derived from contract parameters
    ######################
    def test_price_is_not_clamped_at_liquidation_price(self):
        liquidation = standard_liquidation()
        self.assertEqual(liquidation.clamped_end_price_oracleUnits_per_bch, liquidation.naive_end_price_oracleUnits_per_bch)

    def test_price_is_clamped_below_liquidation(self):
        liquidation = standard_liquidation(price_oracleUnits_per_bch=BELOW_LIQUIDATING_PRICE_USDEM2_PER_BCH)
        self.assertGreater(liquidation.clamped_end_price_oracleUnits_per_bch, liquidation.naive_end_price_oracleUnits_per_bch)

    def test_total_payout_sats_has_correct_value(self):
        self.assertEqual(standard_maturation().total_payout_sats, DERIVED_TOTAL_PAYOUT_SATS)

    def test_hedge_payout_sats_has_correct_value(self):
        self.assertEqual(standard_maturation().hedge_payout_sats, DERIVED_HEDGE_PAYOUT_SATS)

    def test_long_payout_sats_has_correct_value(self):
        self.assertEqual(standard_maturation().long_payout_sats, DERIVED_LONG_PAYOUT_SATS)

    ######################
    # Exact secondary unit values
    ######################
    def test_total_payout_units_has_correct_value(self):
        self.assertAlmostEqual(standard_maturation().total_payout_oracleUnits, DERIVED_TOTAL_PAYOUT_ORACLE_UNITS, delta=.001)

    def test_hedge_payout_units_has_correct_value(self):
        self.assertAlmostEqual(standard_maturation().hedge_payout_oracleUnits, DERIVED_HEDGE_PAYOUT_ORACLE_UNITS, delta=.001)

    def test_long_payout_units_has_correct_value(self):
        self.assertAlmostEqual(standard_maturation().long_payout_oracleUnits, DERIVED_LONG_PAYOUT_ORACLE_UNITS, delta=.001)

    ######################
    # Exact secondary gain values
    ######################
    def test_gain_sats(self):
        # Hedge Maker / Long Taker
        expected_gain_sats_to_hedge_maker_at_redemption = DERIVED_HEDGE_PAYOUT_SATS - DERIVED_HEDGE_INPUT_SATS + TOTAL_FEES_TO_MAKER_SATS
        expected_gain_sats_to_long_taker_at_redemption = DERIVED_LONG_PAYOUT_SATS - DERIVED_LONG_INPUT_SATS + TOTAL_FEES_TO_TAKER_SATS
        hedge_maker_contract = standard_maturation(standard_contract_funding(standard_contract_proposal(maker_side=Side.HEDGE)))

        # Hedge Maker
        self.assertEqual(hedge_maker_contract.hedge_gain_sats, expected_gain_sats_to_hedge_maker_at_redemption)
        self.assertEqual(hedge_maker_contract.maker_gain_sats, expected_gain_sats_to_hedge_maker_at_redemption)

        # Long Taker
        self.assertEqual(hedge_maker_contract.long_gain_sats, expected_gain_sats_to_long_taker_at_redemption)
        self.assertEqual(hedge_maker_contract.taker_gain_sats, expected_gain_sats_to_long_taker_at_redemption)

        # Long Maker / Hedge Taker
        expected_gain_sats_to_long_maker_at_redemption = DERIVED_LONG_PAYOUT_SATS - DERIVED_LONG_INPUT_SATS + TOTAL_FEES_TO_MAKER_SATS
        expected_gain_sats_to_hedge_taker_at_redemption = DERIVED_HEDGE_PAYOUT_SATS - DERIVED_HEDGE_INPUT_SATS + TOTAL_FEES_TO_TAKER_SATS
        long_maker_contract = standard_maturation(standard_contract_funding(standard_contract_proposal(maker_side=Side.LONG)))

        # Long Maker
        self.assertEqual(long_maker_contract.long_gain_sats, expected_gain_sats_to_long_maker_at_redemption)
        self.assertEqual(long_maker_contract.maker_gain_sats, expected_gain_sats_to_long_maker_at_redemption)

        # Hedge Taker
        self.assertEqual(long_maker_contract.hedge_gain_sats, expected_gain_sats_to_hedge_taker_at_redemption)
        self.assertEqual(long_maker_contract.taker_gain_sats, expected_gain_sats_to_hedge_taker_at_redemption)

    def test_gain_oracleUnits(self):
        # Hedge Maker / Long Taker
        expected_gain_oracleUnits_to_hedge_maker_at_redemption = UsdEM2Beta(
            DERIVED_HEDGE_PAYOUT_ORACLE_UNITS - DERIVED_HEDGE_INPUT_ORACLE_UNITS + DERIVED_TOTAL_FEES_TO_MAKER_ORACLE_UNITS
        )
        expected_gain_oracleUnits_to_long_taker_at_redemption = UsdEM2Beta(
            DERIVED_LONG_PAYOUT_ORACLE_UNITS - DERIVED_LONG_INPUT_ORACLE_UNITS + DERIVED_TOTAL_FEES_TO_TAKER_ORACLE_UNITS
        )
        hedge_maker_contract = standard_maturation(standard_contract_funding(standard_contract_proposal(maker_side=Side.HEDGE)))

        # Hedge Maker
        self.assertAlmostEqual(hedge_maker_contract.hedge_gain_oracleUnits, expected_gain_oracleUnits_to_hedge_maker_at_redemption)
        self.assertAlmostEqual(hedge_maker_contract.maker_gain_oracleUnits, expected_gain_oracleUnits_to_hedge_maker_at_redemption)

        # Long Taker
        self.assertAlmostEqual(hedge_maker_contract.long_gain_oracleUnits, expected_gain_oracleUnits_to_long_taker_at_redemption)
        self.assertAlmostEqual(hedge_maker_contract.taker_gain_oracleUnits, expected_gain_oracleUnits_to_long_taker_at_redemption)

        # Long Maker / Hedge Taker
        expected_gain_oracleUnits_to_long_maker_at_redemption = UsdEM2Beta(
            DERIVED_LONG_PAYOUT_ORACLE_UNITS - DERIVED_LONG_INPUT_ORACLE_UNITS + DERIVED_TOTAL_FEES_TO_MAKER_ORACLE_UNITS
        )
        expected_gain_oracleUnits_to_hedge_taker_at_redemption = UsdEM2Beta(
            DERIVED_HEDGE_PAYOUT_ORACLE_UNITS - DERIVED_HEDGE_INPUT_ORACLE_UNITS + DERIVED_TOTAL_FEES_TO_TAKER_ORACLE_UNITS
        )
        long_maker_contract = standard_maturation(standard_contract_funding(standard_contract_proposal(maker_side=Side.LONG)))

        # Long Maker
        self.assertAlmostEqual(long_maker_contract.long_gain_oracleUnits, expected_gain_oracleUnits_to_long_maker_at_redemption)
        self.assertAlmostEqual(long_maker_contract.maker_gain_oracleUnits, expected_gain_oracleUnits_to_long_maker_at_redemption)

        # Hedge Taker
        self.assertAlmostEqual(long_maker_contract.hedge_gain_oracleUnits, expected_gain_oracleUnits_to_hedge_taker_at_redemption)
        self.assertAlmostEqual(long_maker_contract.taker_gain_oracleUnits, expected_gain_oracleUnits_to_hedge_taker_at_redemption)

    ######################
    # Sided versions of values
    ######################
    def test_all_sided_values(self):
        c = standard_maturation()
        self.assertEqual(c.maker_payout_sats, c.hedge_payout_sats)
        self.assertEqual(c.taker_payout_sats, c.long_payout_sats)
        self.assertEqual(c.maker_payout_oracleUnits, c.hedge_payout_oracleUnits)
        self.assertEqual(c.taker_payout_oracleUnits, c.long_payout_oracleUnits)
        self.assertEqual(c.maker_gain_sats, c.hedge_gain_sats)
        self.assertEqual(c.taker_gain_sats, c.long_gain_sats)
        self.assertEqual(c.maker_gain_oracleUnits, c.hedge_gain_oracleUnits)
        self.assertEqual(c.taker_gain_oracleUnits, c.long_gain_oracleUnits)
        self.assertEqual(c.maker_gain_percent_of_own_input, c.hedge_gain_percent_of_own_input)
        self.assertEqual(c.taker_gain_percent_of_own_input, c.long_gain_percent_of_own_input)

        c = standard_maturation(standard_contract_funding(standard_contract_proposal(maker_side=Side.LONG)))
        self.assertEqual(c.maker_payout_sats, c.long_payout_sats)
        self.assertEqual(c.taker_payout_sats, c.hedge_payout_sats)
        self.assertEqual(c.maker_payout_oracleUnits, c.long_payout_oracleUnits)
        self.assertEqual(c.taker_payout_oracleUnits, c.hedge_payout_oracleUnits)
        self.assertEqual(c.maker_gain_sats, c.long_gain_sats)
        self.assertEqual(c.taker_gain_sats, c.hedge_gain_sats)
        self.assertEqual(c.maker_gain_oracleUnits, c.long_gain_oracleUnits)
        self.assertEqual(c.taker_gain_oracleUnits, c.hedge_gain_oracleUnits)
        self.assertEqual(c.maker_gain_percent_of_own_input, c.long_gain_percent_of_own_input)
        self.assertEqual(c.taker_gain_percent_of_own_input, c.hedge_gain_percent_of_own_input)

    def test_parameterized_lookup_error_on_invalid_combinations(self):
        maker_hedge_maturation = standard_maturation(standard_contract_funding(standard_contract_proposal(maker_side=Side.HEDGE)))
        with self.assertRaises(ValueError):
            maker_hedge_maturation.payout_sats(role=Role.MAKER, side=Side.LONG)
        with self.assertRaises(ValueError):
            maker_hedge_maturation.payout_sats(role=Role.TAKER, side=Side.HEDGE)

        taker_hedge_maturation = standard_maturation(standard_contract_funding(standard_contract_proposal(maker_side=Side.LONG)))
        with self.assertRaises(ValueError):
            taker_hedge_maturation.payout_sats(role=Role.TAKER, side=Side.LONG)
        with self.assertRaises(ValueError):
            taker_hedge_maturation.payout_sats(role=Role.MAKER, side=Side.HEDGE)


if __name__ == '__main__':
    unittest.main()
