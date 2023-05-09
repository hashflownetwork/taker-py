from requests import Session
from exceptions import InvalidUsage
import os
from validation import *

class HashflowApi:
    session = Session()

    def __init__(self, auth_key, name, mode, environment='production'):
        self.headers = {'Authorization': auth_key}
        if environment == 'production':
            self.host = 'https://api.hashflow.com'
        elif environment == 'staging':
            self.host = 'https://api-staging.hashflow.com'
        else: 
            raise InvalidUsage(f"Invalid value {environment} for environment") 
        
        if mode == 'wallet':
            self.source = 'api'
            self.wallet = name
        elif mode == 'taker':
            self.source = name
            self.wallet = None
        else:
            raise InvalidUsage(f"Invalid value {mode} for mode")

    def get_market_makers(self, chain_id, wallet=None, market_maker=None):
        validate_chain_id(chain_id)
        params = {
            'source': self.source,
            'networkId': chain_id,
        }
        if wallet is not None:
            params['wallet'] = wallet
        if market_maker is not None:
            params['marketMaker'] = market_maker

        r = self.session.get(f"{self.host}/taker/v1/marketMakers", headers=self.headers, params=params)
        r.raise_for_status()
        return r.json()['marketMakers']

    def get_price_levels(self, chain_id, market_makers):
        validate_chain_id(chain_id)
        params = {
            'source': self.source,
            'networkId': chain_id,
            'marketMakers': market_makers
        }
        if self.wallet is not None:
            params['wallet'] = self.wallet

        r = self.session.get(f"{self.host}/taker/v2/price-levels", headers=self.headers, params=params)
        r.raise_for_status()
        return r.json()['levels']
    
    def request_quote(self, chain_id, base_token, quote_token, dst_chain_id=None, base_token_amount=None, quote_token_amount=None, wallet=None, effective_trader=None, market_makers=None, feeBps=None, debug=False):
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
            'rfqType': '3', # fix
            'source': self.source,
            'trader': trader,
            'networkId': chain_id,
            'dstNetworkId': dst_chain_id,
            'baseToken': base_token,
            'quoteToken': quote_token,
            'baseTokenAmount': base_token_amount,
            'quoteTokenAmount': quote_token_amount,
            'effectiveTrader': effective_trader,
            'marketMakers': market_makers,
            'feesBps': feeBps,
            'debug': debug,
        }

        r = self.session.post(f"{self.host}/taker/v2/rfq", data=data)
        r.raise_for_status()
        return r.json()



if __name__ == "__main__":
    api = HashflowApi(os.environ['HASHFLOW_AUTHORIZATION_KEY'], 'qa', 'taker', 'production')
    makers = api.get_market_makers(1)
    print(makers)
    levels = api.get_price_levels(1, ['mm4', 'mm5'])
    print(levels)





