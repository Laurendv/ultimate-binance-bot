from binance import Client
from coinmarketcapapi import CoinMarketCapAPI
from dotenv import load_dotenv
import os

load_dotenv()

def init():
    config = {
        "coin_market_cap_client": CoinMarketCapAPI(os.getenv('COIN_MARKET_CAP'))
    }
    if os.getenv('MAINNET') == 1:
        api_key = os.getenv('BINANCE_PUBLIC')
        api_secret = os.getenv('BINANCE_SECRET')
        config["binance_client"] = Client(api_key, api_secret)    
    else:     
        api_key = os.getenv('BINANCE_PUBLIC_TEST')
        api_secret = os.getenv('BINANCE_SECRET_TEST')
        testnet_url = 'https://testnet.binance.vision/api'
        client = Client(api_key, api_secret)
        client.API_URL = testnet_url
        config["binance_client"] = client
    return config
