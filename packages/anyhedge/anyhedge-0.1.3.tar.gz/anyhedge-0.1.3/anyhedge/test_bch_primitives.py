# Built-in imports
import unittest

# Local imports
from . import bch_primitives as bchp


VALID_PUBLIC_KEY_HEX = '0123456789abcdef0123456789ABCDEF0123456789abcdef0123456789abcdef01'
VALID_TIMESTAMP_INT = 5_000_000_000
VALID_SATS = 1


class TestPublicKey(unittest.TestCase):
    def test_value_is_string_matching_source_public_key_hex(self):
        pk = bchp.PublicKey(VALID_PUBLIC_KEY_HEX)
        self.assertEqual(pk, VALID_PUBLIC_KEY_HEX)

    def test_ValueError_if_source_has_hex_prefix(self):
        with self.assertRaises(ValueError):
            valid_key_with_prefx = f'0x{VALID_PUBLIC_KEY_HEX}'
            bchp.PublicKey(valid_key_with_prefx)

    def test_ValueError_if_source_is_not_33_bytes_66_hex_chars(self):
        self.assertEqual(len(VALID_PUBLIC_KEY_HEX), 66)
        with self.assertRaises(ValueError):
            too_short = VALID_PUBLIC_KEY_HEX[2:]
            bchp.PublicKey(too_short)
        with self.assertRaises(ValueError):
            too_long = VALID_PUBLIC_KEY_HEX + '00'
            bchp.PublicKey(too_long)
        with self.assertRaises(ValueError):
            odd_length = VALID_PUBLIC_KEY_HEX + '0'
            bchp.PublicKey(odd_length)


class TestScriptTimestamp(unittest.TestCase):
    def test_value_is_integer_matching_source(self):
        timestamp = bchp.ScriptTimestamp(VALID_TIMESTAMP_INT)
        self.assertEqual(timestamp, VALID_TIMESTAMP_INT)

    def test_AssertionError_if_source_is_not_int(self):
        with self.assertRaises(AssertionError):
            bchp.ScriptTimestamp(VALID_TIMESTAMP_INT + 0.1)

    def test_AssertionError_if_source_greater_than_safe_javascript_integer_as_conservative_proxy_for_script_integers(self):
        basically_max_javascript_safe_int = 2**53
        # should work
        bchp.ScriptTimestamp(basically_max_javascript_safe_int)

        # should fail
        with self.assertRaises(AssertionError):
            bchp.ScriptTimestamp(basically_max_javascript_safe_int + 1)

    def test_AssertionError_if_source_less_than_minimum_valid_nlocktime_timestamp(self):
        # should work
        bchp.ScriptTimestamp(500_000_000)

        # should fail
        with self.assertRaises(AssertionError):
            bchp.ScriptTimestamp(500_000_000 - 1)


class TestSats(unittest.TestCase):
    def test_value_is_integer_matching_source(self):
        sats = bchp.Sats(VALID_SATS)
        self.assertEqual(sats, VALID_SATS)

    def test_AssertionError_if_source_is_not_int(self):
        with self.assertRaises(AssertionError):
            bchp.Sats(VALID_SATS + 0.1)

    def test_AssertionError_if_source_is_less_or_greater_than_plus_minus_arbitrary_max_reasonable_sats(self):
        # fails above max
        with self.assertRaises(AssertionError):
            bchp.Sats(bchp.MAX_REASONABLE_SATS + 1)

        # fails below negative max
        with self.assertRaises(AssertionError):
            bchp.Sats(-bchp.MAX_REASONABLE_SATS - 1)

    def test_returns_eight_digits_of_float_bch_value(self):
        original_sats = bchp.Sats(1234)
        bch_equivalent = original_sats.bch
        self.assertEqual(bch_equivalent, 0.00001234)


class TestUtxoSats(unittest.TestCase):
    def test_behaves_mostly_like_sats(self):
        self.assertTrue(issubclass(bchp.UtxoSats, bchp.Sats))

    def test_AssertionError_if_source_is_less_than_positive_dust(self):
        # works
        bchp.UtxoSats(bchp.DUST)

        # doesn't work
        with self.assertRaises(AssertionError):
            bchp.UtxoSats(bchp.DUST - 1)


if __name__ == '__main__':
    unittest.main()
