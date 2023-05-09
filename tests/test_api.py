from hashflow.api import HashflowApi

TEST_AUTH_KEY = "TH4RngQBV8mgjiZpTHJ3"
TEST_WALLET_ADDRESS = "0xb31e5e57dd102fac42f5dc9c7e1ba9851761b9e4"
TEST_CHAIN_ID = 1
TEST_BASE_TOKEN = "0x2260fac5e5542a773aa44fbcfedf7c193bc2c599"
TEST_QUOTE_TOKEN = "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48"
TEST_QUOTE_TOKEN_AMOUNT = "18994364991"
TEST_FEE_BPS = 2
TEST_MARKET_MAKERS_LIST = ["mm4", "mm5"]


def create_response(mocker, json_body):
    response = mocker.MagicMock()
    response.raise_for_status = mocker.MagicMock(return_value=None)
    response.json = mocker.MagicMock(return_value=json_body)

    return response


class TestWallet:
    api = HashflowApi(TEST_AUTH_KEY, TEST_WALLET_ADDRESS, "wallet")

    def test_get_market_makers(self, mocker):
        response = create_response(mocker, {"marketMakers": TEST_MARKET_MAKERS_LIST})
        patched = mocker.patch("requests.get", return_value=response)
        result = self.api.get_market_makers(
            TEST_CHAIN_ID, market_maker=TEST_MARKET_MAKERS_LIST
        )
        assert result == ["mm4", "mm5"]
        assert patched.call_args_list == [
            mocker.call(
                "https://api.hashflow.com/taker/v1/marketMakers",
                headers={"Authorization": TEST_AUTH_KEY},
                params={
                    "source": "api",
                    "networkId": TEST_CHAIN_ID,
                    "marketMaker": TEST_MARKET_MAKERS_LIST,
                },
            )
        ]

    def test_get_price_levels(self, mocker):
        response = create_response(mocker, {"levels": "dummy data"})
        patched = mocker.patch("requests.get", return_value=response)
        result = self.api.get_price_levels(TEST_CHAIN_ID, market_makers=["mm4", "mm5"])
        assert result == "dummy data"
        assert patched.call_args_list == [
            mocker.call(
                "https://api.hashflow.com/taker/v2/price-levels",
                headers={"Authorization": TEST_AUTH_KEY},
                params={
                    "source": "api",
                    "networkId": TEST_CHAIN_ID,
                    "marketMakers": TEST_MARKET_MAKERS_LIST,
                    "wallet": TEST_WALLET_ADDRESS,
                },
            )
        ]

    def test_request_quote(self, mocker):
        response = create_response(mocker, "quote data")
        patched = mocker.patch("requests.post", return_value=response)
        result = self.api.request_quote(
            chain_id=TEST_CHAIN_ID,
            base_token=TEST_BASE_TOKEN,
            quote_token=TEST_QUOTE_TOKEN,
            quote_token_amount=TEST_QUOTE_TOKEN_AMOUNT,
            market_makers=TEST_MARKET_MAKERS_LIST,
            feeBps=TEST_FEE_BPS,
            debug=True,
        )
        assert result == "quote data"
        assert patched.call_args_list == [
            mocker.call(
                "https://api.hashflow.com/taker/v2/rfq",
                json={
                    "rfqType": 0,
                    "source": "api",
                    "trader": TEST_WALLET_ADDRESS,
                    "networkId": TEST_CHAIN_ID,
                    "dstNetworkId": None,
                    "baseToken": TEST_BASE_TOKEN,
                    "quoteToken": TEST_QUOTE_TOKEN,
                    "baseTokenAmount": None,
                    "quoteTokenAmount": TEST_QUOTE_TOKEN_AMOUNT,
                    "effectiveTrader": None,
                    "marketMakers": TEST_MARKET_MAKERS_LIST,
                    "feesBps": TEST_FEE_BPS,
                    "debug": True,
                },
                headers={"Authorization": TEST_AUTH_KEY},
            )
        ]


class TestTaker:
    api = HashflowApi(TEST_AUTH_KEY, "test_taker_client", "taker")

    def test_get_market_makers(self, mocker):
        response = create_response(mocker, {"marketMakers": TEST_MARKET_MAKERS_LIST})
        patched = mocker.patch("requests.get", return_value=response)
        result = self.api.get_market_makers(
            TEST_CHAIN_ID, market_maker=TEST_MARKET_MAKERS_LIST
        )
        assert result == ["mm4", "mm5"]
        assert patched.call_args_list == [
            mocker.call(
                "https://api.hashflow.com/taker/v1/marketMakers",
                headers={"Authorization": TEST_AUTH_KEY},
                params={
                    "source": "test_taker_client",
                    "networkId": TEST_CHAIN_ID,
                    "marketMaker": TEST_MARKET_MAKERS_LIST,
                },
            )
        ]

    def test_get_price_levels(self, mocker):
        response = create_response(mocker, {"levels": "dummy data"})
        patched = mocker.patch("requests.get", return_value=response)
        result = self.api.get_price_levels(TEST_CHAIN_ID, market_makers=["mm4", "mm5"])
        assert result == "dummy data"
        assert patched.call_args_list == [
            mocker.call(
                "https://api.hashflow.com/taker/v2/price-levels",
                headers={"Authorization": TEST_AUTH_KEY},
                params={
                    "source": "test_taker_client",
                    "networkId": TEST_CHAIN_ID,
                    "marketMakers": TEST_MARKET_MAKERS_LIST,
                },
            )
        ]

    def test_request_quote(self, mocker):
        response = create_response(mocker, "quote data")
        patched = mocker.patch("requests.post", return_value=response)
        result = self.api.request_quote(
            chain_id=TEST_CHAIN_ID,
            base_token=TEST_BASE_TOKEN,
            quote_token=TEST_QUOTE_TOKEN,
            quote_token_amount=TEST_QUOTE_TOKEN_AMOUNT,
            market_makers=TEST_MARKET_MAKERS_LIST,
            feeBps=TEST_FEE_BPS,
            debug=True,
            wallet=TEST_WALLET_ADDRESS,
        )
        assert result == "quote data"
        assert patched.call_args_list == [
            mocker.call(
                "https://api.hashflow.com/taker/v2/rfq",
                json={
                    "rfqType": 0,
                    "source": "test_taker_client",
                    "trader": TEST_WALLET_ADDRESS,
                    "networkId": TEST_CHAIN_ID,
                    "dstNetworkId": None,
                    "baseToken": TEST_BASE_TOKEN,
                    "quoteToken": TEST_QUOTE_TOKEN,
                    "baseTokenAmount": None,
                    "quoteTokenAmount": TEST_QUOTE_TOKEN_AMOUNT,
                    "effectiveTrader": None,
                    "marketMakers": TEST_MARKET_MAKERS_LIST,
                    "feesBps": TEST_FEE_BPS,
                    "debug": True,
                },
                headers={"Authorization": TEST_AUTH_KEY},
            )
        ]
