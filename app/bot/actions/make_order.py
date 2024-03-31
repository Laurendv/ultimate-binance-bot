from binance.client import Client
import random

api_key = 'YOUR_API_KEY'
api_secret = 'YOUR_API_SECRET'

# Initialize the client
client = Client(api_key, api_secret)

# Fetch all symbols
exchange_info = client.get_exchange_info()
symbols = [symbol['symbol'] for symbol in exchange_info['symbols'] if 'USDT' in symbol['symbol']]

# Select 5 random symbols
selected_symbols = random.sample(symbols, 5)

# Fetch current prices and place orders
for symbol in selected_symbols:
    # Get the latest price
    price = client.get_symbol_ticker(symbol=symbol)
    
    # Determine the quantity to buy - this is just a placeholder
    # Replace this with your logic to determine the quantity based on price and your budget/strategy
    quantity = 0.01  # Example fixed quantity, adjust based on your strategy

    # Place a test order (this won't create an actual order)
    # For a real order, use client.order_market_buy instead
    order = client.create_test_order(
        symbol=symbol,
        side=Client.SIDE_BUY,
        type=Client.ORDER_TYPE_MARKET,
        quantity=quantity
    )

    print(f"Test order placed for {symbol}: {order}")
