from .helpers.exceptions import InvalidUsage
import os
from .helpers.validation import *
from .helpers.common import RfqType
import aiohttp


class HashflowApi:
    def __init__(self, mode, name, auth_key, environment="production"):
        self.headers = {"Authorization": auth_key}
        if environment == "production":
            self.host = "https://api.hashflow.com"
        elif environment == "staging":
            self.host = "https://api-staging.hashflow.com"
        else:
            raise InvalidUsage(f"Invalid value {environment} for environment")

        if mode == "wallet":
            self.source = "api"
            self.wallet = name
        elif mode == "taker":
            self.source = name
            self.wallet = None
        else:
            raise InvalidUsage(f"Invalid value {mode} for mode")
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.session.close()

    async def get_market_makers(self, chain_id, wallet=None, market_maker=None):
        validate_chain_id(chain_id)
        params = {
            "source": self.source,
            "networkId": chain_id,
        }
        if wallet is not None:
            params["wallet"] = wallet
        if market_maker is not None:
            params["marketMaker"] = market_maker


        async with self.session.get(f"{self.host}/taker/v1/marketMakers", headers=self.headers, params=params) as r:
            r.raise_for_status()
            json = await r.json()
            return json["marketMakers"]

    async def get_price_levels(self, chain_id, market_makers):
        validate_chain_id(chain_id)
        params = {
            "source": self.source,
            "networkId": chain_id,
            "marketMakers[]": market_makers,
        }
        if self.wallet is not None:
            params["wallet"] = self.wallet

        async with self.session.get(f"{self.host}/taker/v2/price-levels", headers=self.headers, params=params) as r:
            r.raise_for_status()
            json = await r.json()
            return json["levels"]

    async def request_quote(
        self,
        chain_id,
        base_token,
        quote_token,
        dst_chain_id=None,
        base_token_amount=None,
        quote_token_amount=None,
        wallet=None,
        effective_trader=None,
        market_makers=None,
        feeBps=None,
        debug=False,
    ):
        validate_chain_id(chain_id)
        if dst_chain_id is not None:
            validate_chain_id(dst_chain_id)

        validate_evm_address(base_token)
        validate_evm_address(quote_token)
        if base_token_amount is not None:
            validate_number_string(base_token_amount)
        if quote_token_amount is not None:
            validate_number_string(quote_token_amount)

        trader = wallet if wallet is not None else self.wallet
        if trader is None:
            raise InvalidUsage("Must specify wallet")

        validate_evm_address(trader)
        if effective_trader is not None:
            validate_evm_address(effective_trader)

        data = {
            "rfqType": RfqType.RFQT.value,
            "source": self.source,
            "trader": trader,
            "networkId": chain_id,
            "dstNetworkId": dst_chain_id,
            "baseToken": base_token,
            "quoteToken": quote_token,
            "baseTokenAmount": base_token_amount,
            "quoteTokenAmount": quote_token_amount,
            "effectiveTrader": effective_trader,
            "marketMakers": market_makers,
            "feesBps": feeBps,
            "debug": debug,
        }
        async with self.session.post(f"{self.host}/taker/v2/rfq", json=data, headers=self.headers) as r:
            r.raise_for_status()
            return await r.json()


if __name__ == "__main__":
    import asyncio

    async def main():
        async with HashflowApi(
            mode="taker",
            name="qa",
            auth_key=os.environ["HASHFLOW_AUTHORIZATION_KEY"],
            environment="production",
        ) as api:
            makers = await api.get_market_makers(1, market_maker="mm5")
            print(makers)
            levels = await api.get_price_levels(1, ["mm4", "mm5"])
            print(levels)
            wallet = os.environ["HASHFLOW_TEST_WALLET"]
            quote = await api.request_quote(
                chain_id=1,
                base_token="0x2260fac5e5542a773aa44fbcfedf7c193bc2c599",
                quote_token="0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48",
                quote_token_amount="18364991",
                wallet=wallet,
                market_makers=["mm5", "mm4"],
                feeBps=2,
                debug=True,
            )
            print(quote)
    asyncio.run(main())