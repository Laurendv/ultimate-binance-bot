from app.bot import configuration
import json, os
import math

def main():
    binance_client = configuration.init()

    with open("/Users/laurenducvu/Documents/ultimate-binance-bot/allocation.json") as f:
        tokens_to_trade = json.load(f)
    
    for token in tokens_to_trade:
        symbol = token["trading_pair"]
        amount = token["amount_to_invest"]
        price = float(token["price"])
        step_size = float(token["lot_size"]["stepSize"])
        quantity = calculate_quantity(amount, price, step_size)

        print(f"Placing order for {quantity} {symbol} at {price}")

        try:
            order = binance_client.create_order(
                symbol=symbol,
                side='BUY',
                type='LIMIT',
                timeInForce='GTC',  # Good Till Canceled
                quantity=str(quantity), 
                price=str(price)
            )
            print(f"Order placed for {symbol}: {order}")
        except Exception as e:
            print(f"Error placing order for {symbol}: {e}")
            
def gets_binance_precision_standard(quantity):
    return round(quantity, 8)

def calculate_quantity(amount, price, step_size):
    quantity = math.floor((amount / price) / step_size) * step_size
    return gets_binance_precision_standard(quantity)

if __name__ == '__main__':
    main()