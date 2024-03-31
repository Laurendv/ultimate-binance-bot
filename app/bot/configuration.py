from binance import Client
from dotenv import load_dotenv
import os

load_dotenv()

def init():
    if os.getenv('MAINNET') == 1:
        api_key = os.getenv('BINANCE_PUBLIC')
        api_secret = os.getenv('BINANCE_SECRET')
        return Client(api_key, api_secret)    
    else:     
        api_key = os.getenv('BINANCE_PUBLIC_TEST')
        api_secret = os.getenv('BINANCE_SECRET_TEST')
        testnet_url = 'https://testnet.binance.vision/api'
        client = Client(api_key, api_secret)
        client.API_URL = testnet_url
        return client