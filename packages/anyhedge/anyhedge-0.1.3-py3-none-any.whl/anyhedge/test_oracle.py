# Built-in imports
import unittest

# Local imports
from .bch_primitives import (
    PublicKey,
    ScriptTimestamp,
)
from .oracle import (
    Pricepoint,
    ScriptPriceInOracleUnitsPerBch,
)


# Known price message for Usd(e-2) oracle:
#   public key: 02d3c1de9d4bc77d6c3608cbe44d10138c7488e592dc2b1e10a6cf0e92c2ecb047
#   signature: 9f66be2e0b542325303102afb584cdcee591b84a9ec6aba311e73b0f1cbba8d5d71c701b7b6c3230e4814170d79cafea0d90ea0e78d666d8f50dd80b28caf00e
#   message: 2f2635633fa80300a4a50300242d0000
#       timestamp:        1664427567
#       message sequence: 239679
#       price sequence:   239012
#       price:            11556
known_pricepoint = Pricepoint(
    oracle_pubkey=PublicKey('02d3c1de9d4bc77d6c3608cbe44d10138c7488e592dc2b1e10a6cf0e92c2ecb047'),
    message='2f2635633fa80300a4a50300242d0000',
    signature='9f66be2e0b542325303102afb584cdcee591b84a9ec6aba311e73b0f1cbba8d5d71c701b7b6c3230e4814170d79cafea0d90ea0e78d666d8f50dd80b28caf00e',
)


class TestPricepoint(unittest.TestCase):
    def test_new_from_details_has_all_correct_attributes_and_properties(self):
        input_oracle_pubkey = PublicKey('02d3c1de9d4bc77d6c3608cbe44d10138c7488e592dc2b1e10a6cf0e92c2ecb047')
        input_timestamp = ScriptTimestamp(1664427567)
        input_price_oracleUnits_per_bch = ScriptPriceInOracleUnitsPerBch(11556)
        input_message_sequence = 239679
        input_price_sequence = 239012
        input_signature = '9f66be2e0b542325303102afb584cdcee591b84a9ec6aba311e73b0f1cbba8d5d71c701b7b6c3230e4814170d79cafea0d90ea0e78d666d8f50dd80b28caf00e'

        expected_oracleUnit_name = 'USD(e-2)'
        expected_message = '2f2635633fa80300a4a50300242d0000'
        expected_standardUnits_per_bch = 115.56

        p = Pricepoint.new_from_details(
            oracle_pubkey=input_oracle_pubkey,
            timestamp=input_timestamp,
            price_oracleUnits_per_bch=input_price_oracleUnits_per_bch,
            message_sequence=input_message_sequence,
            price_sequence=input_price_sequence,
            signature=input_signature,
        )

        # confirm all the primary attributes and properties
        self.assertEqual(p.oracle_pubkey, input_oracle_pubkey)
        self.assertEqual(p.message, expected_message)
        self.assertEqual(p.signature, input_signature)
        self.assertEqual(p.oracleUnit_name, expected_oracleUnit_name)
        self.assertEqual(p.timestamp, input_timestamp)
        self.assertEqual(p.message_sequence, input_message_sequence)
        self.assertEqual(p.price_sequence, input_price_sequence)
        self.assertEqual(p.price_oracleUnits_per_bch, input_price_oracleUnits_per_bch)
        self.assertEqual(p.price_standardUnits_per_bch, expected_standardUnits_per_bch)

    def test_metadata_message_same_length_as_price_message_raises_value_error(self):
        metadata_message = 'f499936236f60000caffffff55534400'
        self.assertEqual(len(metadata_message), len(known_pricepoint.message))
        with self.assertRaises(ValueError):
            Pricepoint(
                oracle_pubkey=PublicKey('02d3c1de9d4bc77d6c3608cbe44d10138c7488e592dc2b1e10a6cf0e92c2ecb047'),
                message=metadata_message,
                signature='',
            )

    def test_metadata_message_different_length_as_price_message_raises_value_error(self):
        metadata_message = 'f49993622ff60000fcffffff'
        self.assertNotEqual(len(metadata_message), len(known_pricepoint.message))
        with self.assertRaises(ValueError):
            Pricepoint(
                oracle_pubkey=PublicKey('02d3c1de9d4bc77d6c3608cbe44d10138c7488e592dc2b1e10a6cf0e92c2ecb047'),
                message=metadata_message,
                signature='',
            )


if __name__ == '__main__':
    unittest.main()
