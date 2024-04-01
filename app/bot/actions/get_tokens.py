import random, json, time
from app.bot import configuration
from datetime import datetime
import copy

ONE_MILLION_DOLLARS = 1000000
ONE_HUNDRED_MILLION_DOLLARS = 100000000

def main():
    config = configuration.init()
   
    binance_client = config["binance_client"]
    coin_market_cap_client = config["coin_market_cap_client"]
     
    # Fetch all symbols
    # exchange_info = binance_client.get_exchange_info()
    # symbols = [symbol['symbol'] for symbol in exchange_info['symbols'] if 'USDT' in symbol['symbol']]

    
    tickers = binance_client.get_all_tickers()
    usdt_pairs = [ticker for ticker in tickers if ticker['symbol'].endswith('USDT')][100:110]

    
    tokens_to_trade = select_tokens(usdt_pairs, binance_client, coin_market_cap_client)
    
    
    
    with open('tokens_to_trade.json', 'w') as f:
        json.dump(tokens_to_trade_model(tokens_to_trade, binance_client), f, indent=4)    
    
def token_model(token, binance_client, time_now):
    symbol = token['trading_pair']
    exchange_info = binance_client.get_exchange_info()
    lot_size_info = get_lot_size_info(symbol, exchange_info)
    model_data = {
            "price": binance_client.get_symbol_ticker(symbol=symbol)['price'],
            "time": time_now,
            "weight": calculate_weight(),
            "lot_size": lot_size_info
            }
    return {**token, **model_data}
    
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



def get_market_cap(symbol, coin_market_cap_client):
    
    token_symbol = symbol.split("USDT")[0]
    
    current_data = coin_market_cap_client.cryptocurrency_quotes_latest(symbol=token_symbol)
    market_cap =  current_data.data[token_symbol][0]['quote']['USD']['market_cap']
    percent_change_7d =  current_data.data[token_symbol][0]['quote']['USD']['percent_change_7d']
    return {
        "symbol": token_symbol,
        "trading_pair":symbol,
        "market_cap":market_cap,
        "percent_change_7d": percent_change_7d
        }

def market_cap_within_range(market_cap_min, market_cap_max, tickers, binance_client, coin_market_cap_client):
    tokens_within_range = []
    
    for token in tickers:
        symbol = token['symbol']
        token_data = get_market_cap(symbol, coin_market_cap_client)  # You'll need to implement this function
        market_cap = token_data["market_cap"]
        if market_cap_min <= market_cap <= market_cap_max:
           tokens_within_range.append(token_data)

    return tokens_within_range

def sort_by_biggest_gainers(tokens):
     tokens_data = copy.deepcopy(tokens)
     return sorted(tokens_data, key=lambda x: x['percent_change_7d'])

def select_tokens(tickers, binance_client, coin_market_cap_client):
    market_cap_min = ONE_MILLION_DOLLARS
    market_cap_max = ONE_HUNDRED_MILLION_DOLLARS
    symbols_in_market_cap_range = market_cap_within_range(market_cap_min,
                                                          market_cap_max,
                                                          tickers,
                                                          binance_client,
                                                          coin_market_cap_client)
    
    return sort_by_biggest_gainers(symbols_in_market_cap_range)[:6]
    
def calculate_weight():
    return 0.2 # could be based on percentage increases

if __name__ == '__main__':
    main()
