from app.bot import configuration
import json, os

strategy = {
    "name": "HILOW57",
    "description": "This strategy is based on the HILOW57 indicator. It buys when the indicator is below 0.5 and sells when it is above 0.5.",
    "position_sizing": 0.1, # 10% of the total balance will be allocated to each trade
}

def main():
    binance_client = configuration.init()
    with open("/Users/laurenducvu/Documents/ultimate-binance-bot/tokens_to_trade.json") as f:
        tokens_to_trade = json.load(f)
    account_info = binance_client.get_account()
    allocation = calculate_allocation(tokens_to_trade, account_info["balances"])
    with open("/Users/laurenducvu/Documents/ultimate-binance-bot/allocation.json", "w") as f:
        json.dump(allocation, f, indent=4)
    

def calculate_allocation(tokens_to_trade, balance):
    usdt_balance = next((item for item in balance if item["asset"] == "USDT"), None)
    if usdt_balance is None:
        print("No USDT balance found")
        return
    allocation = []
    for index, token in enumerate(tokens_to_trade):
        amount_to_invest = calculate_amount_to_invest(float(usdt_balance["free"]), strategy["position_sizing"], token["weight"])
        data = token
        data["amount_to_invest"] = amount_to_invest
        allocation.append(data)
    return allocation

def calculate_amount_to_invest(balance, position_size, weight):
    return balance * position_size * weight

if __name__ == '__main__':
    main()