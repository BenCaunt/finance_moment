import string
from time import time
from turtle import pd
import yfinance as yf   
from datetime import date
from datetime import timedelta
from enum import Enum, auto
import queue

# Get today's date
today = date.today()
yesterday = today - timedelta(days = 1)

SIM_DATE_START = '2021-01-06' 
SIM_DATE_END = str(yesterday)

class asset:
    def __init__(self,asset_ticker: str):
        self.data = yf.download(asset_ticker,SIM_DATE_START,SIM_DATE_END,interval='1d') 
        self.name = asset_ticker
        self.is_owned = False 
        self.shares_owned = 0.0
    def get_day_data(self, date: str):
        return self.data.loc[date]
    def get_day_close(self, date: str):
        return float(self.get_day_data(date)["Adj Close"])
    def get_day_open(self, date: str):
        return float(self.get_day_data(date)["Open"])
    def get_day_high(self, date: str):
        return float(self.get_day_data(date)["High"])
    def get_day_low(self, date: str):
        return float(self.get_day_data(date)["Low"])
    def get_day_volume(self, date: str):
        return float(self.get_day_data(date)["Volume"])
    def __str__(self) -> str:
        return self.name


class PurchaseMethods(Enum):
    BUY_NUM_SHARES = auto()
    BUY_DOLLARS = auto()



class BuyOrder:
    def __init__(self, share_price: float, balance: float, ticker:str, shares=None, purchase_amount=None):

        self.shares = shares
        self.purchase_amount = purchase_amount
        self.share_price = share_price
        self.ticker = ticker 

        if shares is None and purchase_amount is None:
            raise Exception("No amount provided")

        if not shares is None and not purchase_amount is None:
            raise Exception("Too many arguments specified, Overconstrained purchase.  Only Shares or cash amount should be specified") 

        self.method = None 

        if not shares is None:
            self.method = PurchaseMethods.BUY_NUM_SHARES
            projected_cost = share_price * shares
            if balance < projected_cost:
                self.shares = balance / share_price
        else:
            self.method = PurchaseMethods.BUY_DOLLARS
            if balance < purchase_amount:
                self.purchase_amount = balance

        
    def runOrder(self):
        issued_cost = 0
        issued_shares = 0 
        if self.method == PurchaseMethods.BUY_NUM_SHARES:
            issued_shares = self.shares
            issued_cost = issued_shares * self.share_price

        if self.method == PurchaseMethods.BUY_DOLLARS:
            issued_cost = self.purchase_amount
            issued_shares = issued_cost / self.share_price # we have fractional shares enabled

        return (self.ticker, -issued_cost, -issued_shares) # returns the balance delta aka amount subtracted from balance and the issued shares 


class SellOrder:
    def __init__(self, share_price: float, shares_owned: float, ticker:str, shares_sold=None, sell_amount=None):
        self.shares = shares_sold
        self.sell_amount = sell_amount
        self.share_price = share_price
        self.ticker = ticker 
        self.shares_sold = shares_sold

        if shares_sold is None and sell_amount is None:
            raise Exception("No amount provided")

        if not shares_sold is None and not sell_amount is None:
            raise Exception("Too many arguments specified, Overconstrained purchase.  Only Shares or cash amount should be specified") 

        self.method = None 

        if not shares_sold is None:
            self.method = PurchaseMethods.BUY_NUM_SHARES
            if shares_sold > shares_owned:
                self.shares_sold = shares_owned
        else:
            self.method = PurchaseMethods.BUY_DOLLARS
            projected_shares = sell_amount / share_price # number of shares to sell 
            if projected_shares > shares_owned:
                self.shares_sold = shares_owned
            else: 
                self.shares_sold = projected_shares

        
    def runOrder(self):
        cost = self.share_price * self.shares_sold 
        return (self.ticker, cost, self.shares_sold) # shares gained from this trade 

class TradingStrategy:
    def __init__(self):
        self.order_queue = None
        self.initial_balance = None
        self.asset_names = None
        self.assets = None
    def run_strategy(self):
        pass # create your trading strategy here


class buy_once_strat(TradingStrategy):
    def __init__(self):
        super().__init__()
        self.elapsed_days = 0 



    def run_strategy(self):
        self.elapsed_days += 1 
        if self.elapsed_days == 5: 
            order = BuyOrder(self.assets["TQQQ"].get_)



class backtest_engine:
    def __init__(self, asset_names: list[str], strategy: TradingStrategy):
        self.asset_names = asset_names
        self.assets = {}
        self.cash_balance = 10_000
        self.net_worth = self.cash_balance
        self.internal_date = SIM_DATE_START
        self.orderQueue = queue.Queue()
        self.trading_strategy = strategy
        self.trading_strategy.order_queue = self.orderQueue
        self.trading_strategy.initial_balance = self.assets
        self.trading_strategy.asset_names = self.asset_names
        self.trading_strategy.assets = self.assets



        for a in asset_names:
            self.assets[a] = asset(a)

    
    def calculate_networth(self):
        networth_total = self.cash_balance

        for a in self.assets.values():
            networth_total += a.get_day_close(self.internal_date)

        self.net_worth = networth_total
    def run_sim(self):
        while self.internal_date < SIM_DATE_END:
            # iterate the date forward by 1 day 
            self.trading_strategy.run_strategy()


            # calculate net worth at the end of the day 
            self.calculate_networth()
            date = 
            self.internal_date += timedelta(days=1) 
             
if __name__ == "__main__":
    stategy = buy_once_strat()
    engine = backtest_engine(["SQQQ","TQQQ","FNGU"],stategy)
    engine.run_sim()
    TQQQ = engine.assets["TQQQ"]

    # print(TQQQ.get_day_data("2021-01-01"))
    # print(TQQQ.get_day_close("2021-01-01"))
    # print(TQQQ.get_day_volume("2021-01-01"))