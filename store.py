import pandas as pd

class Store:
    def __init__(self):
        self.market_data_file = "data/market_data.csv"
        self.prices_data_folder = "data/prices"

    def save_symbols(self, symbols):
        symbols.to_csv(self.market_data_file, index=False)

    def read_symbols(self):
        data_types = {'code': 'str'}
        symbols = pd.read_csv(self.market_data_file, dtype=data_types)
        return symbols
    
    def save_stock_prices(self, symbol, prices):
        prices.to_csv(f"{self.prices_data_folder}/{symbol}.csv", index=False)