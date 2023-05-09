from enum import Enum

chains = {
    "ETHEREUM": {"chainId": 1},
    "GOERLI": {"chainId": 2},
    "OPTIMISM": {"chainId": 3},
    "POLYGON": {"chainId": 4},
    "MUMBAI": {"chainId": 5},
    "BNB": {"chainId": 6},
    "BNB_TESTNET": {"chainId": 7},
    "ARBITRUM": {"chainId": 8},
    "AVALANCHE": {"chainId": 9},
}

CHAIN_IDS = [chain["chainId"] for chain in chains.values()]

class RfqType(Enum):
    RFQT = 0
    RFQM = 1

ETHEREUM = {
    "chainId": 1,
    "name": "ethereum",
    "nativeTokenSymbol": "ETH",
    "nativeTokenName": "Ether",
    "nativeTokenDecimals": 18,
    "hashflowChainId": 1,
    "testTokens": False,
    "weth": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
    "layerZeroEndpoint": "0x66A71Dcef29A0fFBDBE3c6a460a3B5BC225Cd675",
    "layerZeroChainId": 101,
    "layerZeroNonceContract": "0x5B905fE05F81F3a8ad8B28C6E17779CFAbf76068",
    "wormholeChainId": 2,
    "wormholeEndpoint": "0x98f3c9e6E3fAce36bAAd05FE09d375Ef1464288B",
    "wormholeConsistency": 1,
    "zksync": False
}

ARBITRUM = {
    "chainId": 42161,
    "name": "arbitrum",
    "nativeTokenSymbol": "ETH",
    "nativeTokenName": "Ether",
    "nativeTokenDecimals": 18,
    "hashflowChainId": 2,
    "testTokens": False,
    "weth": "0x82af49447d8a07e3bd95bd0d56f35241523fbab1",
    "layerZeroEndpoint": "0x3c2269811836af69497E5F486A85D7316753cf62",
    "layerZeroChainId": 110,
    "layerZeroNonceContract": "0x5B905fE05F81F3a8ad8B28C6E17779CFAbf76068",
    "wormholeChainId": 23,
    "wormholeEndpoint": "0xa5f208e072434bC67592E4C49C1B991BA79BCA46",
    "wormholeConsistency": 1,
    "zksync": False
}

OPTIMISM = {
    "chainId": 10,
    "name": "optimism",
    "nativeTokenSymbol": "ETH",
    "nativeTokenName": "Ether",
    "nativeTokenDecimals": 18,
    "hashflowChainId": 3,
    "testTokens": False,
    "weth": "0x4200000000000000000000000000000000000006",
    "layerZeroEndpoint": "0x3c2269811836af69497E5F486A85D7316753cf62",
    "layerZeroChainId": 111,
    "layerZeroNonceContract": "0x5B905fE05F81F3a8ad8B28C6E17779CFAbf76068",
    "zksync": False
}


