import numpy as np
from polygon import StocksClient, ReferenceClient
from typing import Any
import functools
from datetime import datetime, timedelta

FIVEYEARS = timedelta(days=5*356)
NaN = float('nan')

##########################################################################################

foldl = lambda func, acc, xs: functools.reduce(func, xs, acc)

def optionalGet(dict, *args) : 
    try: 
        return foldl (lambda dict, arg: dict.get(arg), dict, args)
    except AttributeError: 
        return None

g = lambda s, *xs : optionalGet(s, *xs)
def gusd (s, *xs) : 
    unit = g(s, *xs, "unit")
    assert(isinstance(unit, str) and unit.lower() == "usd")
    return g(s, *xs, "value")

def text_to_date (text) : # YYYY-MM-DD 
    return np.datetime64(text, 'D')

##########################################################################################

class PolygonProvider :
    def __init__ (self, symbol, API_KEY) : 
        self.symbol = symbol

        stocks_client = StocksClient(API_KEY, connect_timeout=5, read_timeout=5)
        reference_client = ReferenceClient(API_KEY, connect_timeout=5, read_timeout=5)
        fin: Any = reference_client.get_stock_financials_vx("AMD", time_frame="annual", limit=10, order="desc") 
        assert(fin['status'] == 'OK')
        statements = fin['results']

        self.revenues           = np.array([gusd(s, "financials", "income_statement", "revenues") for s in statements]) 
        self.invested_cap       = np.array([NaN for _ in statements])
        self.gross              = np.array([gusd(s, "financials", "income_statement", "gross_profit") for s in statements])
        self.pretax             = np.array([gusd(s, "financials", "income_statement", "income_loss_from_continuing_operations_before_tax") for s in statements])
        self.net_after_tax      = np.array([gusd(s, "financials", "income_statement", "net_income_loss") for s in statements])
        self._net_per_share     = np.array([g(s, "financials", "income_statement", "basic_earnings_per_share", "value") for s in statements])
        self.shares             = self.net_after_tax / self._net_per_share
        self.income_date        = np.array([text_to_date(g(s, "filing_date")) for s in statements])
        self.oper_cashflow      = np.array([gusd(s, "financials", "cash_flow_statement", "net_cash_flow_from_operating_activities") for s in statements])
        self.free_cashflow      = np.array([NaN for _ in statements])
        self.assets             = np.array([gusd(s, "financials", "balance_sheet", "assets") for s in statements])
        self.current_lia        = np.array([gusd(s, "financials", "balance_sheet", "current_liabilities") for s in statements])
        self.liability          = np.array([gusd(s, "financials", "balance_sheet", "liabilities") for s in statements])

        self.years              = np.array([np.datetime_as_string(d, "Y") for d in self.income_date])
        now = datetime.now()
        allprices: Any = stocks_client.get_aggregate_bars(symbol, now-FIVEYEARS, now)

        self.price = allprices["results"][-1]["c"]
        dates = self.income_date.astype('datetime64[s]').tolist()
        self.income_price = np.array([ next((price["vw"] for price in allprices["results"] if datetime.fromtimestamp(price["t"]/1000) - date < timedelta(weeks=2)), NaN) for date in dates ])

    def showAll (self) :
        print("revenues", self.revenues)
        print("invested_cap", self.invested_cap)
        print("gross", self.gross)
        print("pretax", self.pretax)
        print("net_after_tax", self.net_after_tax)
        print("shares", self.shares)
        print("income_date", self.income_date)
        print("oper_cashflow", self.oper_cashflow)
        print("free_cashflow", self.free_cashflow)
        print("assets", self.assets)
        print("current_lia", self.current_lia)
        print("liability", self.liability)
        print("years", self.years)
        print("income_price", self.income_price)
        print("price", self.price)

if __name__ == "__main__" : 
    api = input("API_KEY: ")
    data = PolygonProvider("aapl", api)
    data.showAll()
