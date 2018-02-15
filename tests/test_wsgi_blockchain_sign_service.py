from bexi import Config
from bexi.wsgi.sign_service import implementations

from unittest.case import TestCase


class TestSignService(TestCase):

    def test_wallets(self):
        address = implementations.create_address()

        assert address["privateKey"] == Config.get_config()["bitshares"]["exchange_account_active_key"]
        assert Config.get_config()["bitshares"]["exchange_account_id"] in address["publicAddress"]

    def test_sign(self):
        tx = {
            "ref_block_num": 49506,
            "ref_block_prefix": 2292772274,
            "expiration": "2018-01-25T08:29:00",
            "operations": [
                [
                    2,
                    {
                        "fee": {
                            "amount": 9,
                            "asset_id": "1.3.0"
                        },
                        "fee_paying_account": "1.2.126225",
                        "order": "1.7.49956139",
                        "extensions": []
                    }
                ]
            ],
            "extensions": [],
            "signatures": [],
        }
        stx = implementations.sign(tx, [Config.get_config()["bitshares"]["exchange_account_active_key"]])
        stx = stx["signedTransaction"]
        self.assertIn("signatures", stx)
        self.assertEqual(len(stx["signatures"]), 1)

        stx = implementations.sign(
            tx, ["5JLEjm8zesAHq9fZ52dVTj2Mho15w7esfqWyTULp6WBe9YEJiRA",
                 "5Jm7csbkpF8ghpG9QoyAeWw9Z2uBe93Axe9eoV9BuopUx4r4o6n"]
        )
        stx = stx["signedTransaction"]
        self.assertIn("signatures", stx)
        self.assertEqual(len(stx["signatures"]), 2)