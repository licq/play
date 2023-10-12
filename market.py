import akshare as ak
import pandas as pd
from store import Store
from logger import logger
from utils import retry
import sys

class Market:
    def __init__(self, store=None):
        self.store = Store() if store is None else store
        
    def download_symbols(self):
        sh_symbols = retry(ak.stock_info_sh_name_code)
        sz_symbols = retry(ak.stock_info_sz_name_code)
        if sh_symbols is None or sz_symbols is None:
            logger.error("Failed to download symbols")
            return
        sh_symbols.rename(columns={'证券代码':'code', "证券简称": "name"}, inplace=True)
        sz_symbols.rename(columns={'A股代码':'code', "A股简称": "name"}, inplace=True)
        all_symbols = pd.concat([sh_symbols[['code','name']], sz_symbols[['code','name']]], ignore_index=True)
        self.store.save_symbols(all_symbols)
    
    def history(self, code):
        data = retry(ak.stock_zh_a_hist, symbol=code, period='daily', adjust="qfq")
        data.rename(columns={"日期": "date","开盘": "open","收盘": "close","最高":"high","最低":"low","成交量":"volume", "换手率": "trading_rate"}, inplace=True)
        return data[['date','open','close','high','low','volume', "trading_rate"]]
    
    def histories(self):
        symbols = self.store.read_symbols()
        count = len(symbols['code'])
        for i, code in enumerate(symbols['code']):
            logger.info(f"Downloading histories for {code}..., {i+1}/{count}")
            data = self.history(code)
            if data is None:
                logger.error(f"Failed to download histories for {code}")
                sys.exit(1)
            self.store.save_stock_prices(code, data)
        logger.info("Downloading histories Done")
        


if __name__ == "__main__":
    market = Market()
    market.histories()
    # data = market.history("sh600000", "2020-01-01", "2020-12-31")
    # print(data)



