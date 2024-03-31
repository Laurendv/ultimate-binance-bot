from binance import Client
import os

def init():
    api_key = os.getenv('BINANCE_PUBLIC')
    api_secret = os.getenv('BINANCE_SECRET')
    return Client(api_key, api_secret)