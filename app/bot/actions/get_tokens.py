import random, json, time
from app.bot import configuration
from datetime import datetime


def main():
    binance_client = configuration.init()
    # Fetch all symbols
    exchange_info = binance_client.get_exchange_info()
    symbols = [symbol['symbol'] for symbol in exchange_info['symbols'] if 'USDT' in symbol['symbol']]
    # Select 5 random symbols
    tokens_to_trade = select_tokens(symbols)
        
    with open('tokens_to_trade.json', 'w') as f:
        json.dump(tokens_to_trade_model(tokens_to_trade, binance_client), f, indent=4)    
    
def token_model(token, binance_client, time_now):
    exchange_info = binance_client.get_exchange_info()
    lot_size_info = get_lot_size_info(token, exchange_info)
    return {
            "trading_pair": token, 
            "symbol": token.split('USDT')[0],
            "price": binance_client.get_symbol_ticker(symbol=token)['price'],
            "time": time_now,
            "weight": calculate_weight(),
            "lot_size": lot_size_info
            }
    
def tokens_to_trade_model(tokens, binance_client):
    model = []
    time_now = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    for token in tokens:
        model.append(token_model(token, binance_client, time_now))
    return model

def get_lot_size_info(token, exchange_info):
    for symbol_info in exchange_info['symbols']:
        if symbol_info['symbol'] == token:
            for filter in symbol_info['filters']:
                if filter['filterType'] == 'LOT_SIZE':
                    return filter
    return None

def select_tokens(symbols):
    return random.sample(symbols, 5)

def calculate_weight():
    return 0.2

if __name__ == '__main__':
    main()