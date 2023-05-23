from hashflow.api import HashflowApi
import pytest
import aiohttp

TEST_AUTH_KEY = "TH4RngQBV8mgjiZpTHJ3"
TEST_WALLET_ADDRESS = "0xb31e5e57DD102FAC42f5dc9C7E1Ba9851761B9e4"
TEST_CHAIN_ID = 1
TEST_BASE_TOKEN = "0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599"
TEST_QUOTE_TOKEN = "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"
TEST_QUOTE_TOKEN_AMOUNT = "18994364991"
TEST_FEE_BPS = 2
TEST_MARKET_MAKERS_LIST = ["mm4", "mm5"]

    
def create_response(mocker, json_body):
    response = mocker.MagicMock()
    response.raise_for_status = mocker.MagicMock(return_value=None)
    response.json = mocker.AsyncMock(return_value=json_body)
    response.__aenter__.return_value = response
    response.__aexit__.return_value = None
    return response


# TODO(ENG-1141): Replace the async with in every test with a fixture
class TestWallet:
    @pytest.mark.asyncio
    async def test_get_market_makers(self, mocker):
        async with HashflowApi(mode="wallet", name=TEST_WALLET_ADDRESS, auth_key=TEST_AUTH_KEY) as api:
            response = create_response(mocker, {"marketMakers": TEST_MARKET_MAKERS_LIST})
            patched = mocker.patch.object(aiohttp.ClientSession, "get", return_value=response)
            result = await api.get_market_makers(
                TEST_CHAIN_ID, market_maker=TEST_MARKET_MAKERS_LIST
            )
            assert result == TEST_MARKET_MAKERS_LIST
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

    @pytest.mark.asyncio
    async def test_get_price_levels(self, mocker):
        async with HashflowApi(mode="wallet", name=TEST_WALLET_ADDRESS, auth_key=TEST_AUTH_KEY) as api:
            response = create_response(mocker, {"levels": "dummy data"})
            patched = mocker.patch.object(aiohttp.ClientSession, "get", return_value=response)
            result = await api.get_price_levels(TEST_CHAIN_ID, market_makers=["mm4", "mm5"])
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

    @pytest.mark.asyncio
    async def test_request_quote(self, mocker):
        async with HashflowApi(mode="wallet", name=TEST_WALLET_ADDRESS, auth_key=TEST_AUTH_KEY) as api:
            response = create_response(mocker, "quote data")
            patched = mocker.patch.object(aiohttp.ClientSession, "post", return_value=response)
            result = await api.request_quote(
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
    @pytest.mark.asyncio
    async def test_get_market_makers(self, mocker):
        async with HashflowApi(mode="taker", name="test_taker_client", auth_key=TEST_AUTH_KEY) as api:
            response = create_response(mocker, {"marketMakers": TEST_MARKET_MAKERS_LIST})
            patched = mocker.patch.object(aiohttp.ClientSession, "get", return_value=response)
            result = await api.get_market_makers(
                TEST_CHAIN_ID, market_maker=TEST_MARKET_MAKERS_LIST
            )
            assert result == TEST_MARKET_MAKERS_LIST
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

    @pytest.mark.asyncio
    async def test_get_price_levels(self, mocker):
        async with HashflowApi(mode="taker", name="test_taker_client", auth_key=TEST_AUTH_KEY) as api:
            response = create_response(mocker, {"levels": "dummy data"})
            patched = mocker.patch.object(aiohttp.ClientSession, "get", return_value=response)
            result = await api.get_price_levels(TEST_CHAIN_ID, market_makers=["mm4", "mm5"])
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

    @pytest.mark.asyncio
    async def test_request_quote(self, mocker):
        async with HashflowApi(mode="taker", name="test_taker_client", auth_key=TEST_AUTH_KEY) as api:
            response = create_response(mocker, "quote data")
            patched = mocker.patch.object(aiohttp.ClientSession, "post", return_value=response)
            result = await api.request_quote(
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
