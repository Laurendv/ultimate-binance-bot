binance-trading-bot/
│
├── bot/
│   ├── __init__.py
│   ├── main.py            # Main bot logic
│   ├── trading_strategy.py# Trading strategies implementations
│   ├── config.py          # Configuration settings
│   └── exchange.py        # Interface to Binance API
│
│
├── logs/
│   └── trading.log        # Log file for trading operations
│
├── requirements.txt       # Project dependencies
└── README.md              # Project documentation

Steps:
1. Get the data
2. Compute allocation
3. Back test allocation
4. Order set up
5. Execution
6. Post execution validation