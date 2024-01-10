import numpy as np
from polygon import ReferenceClient
from typing import Any
import functools
from datetime import timedelta
import yfinance as yf
from src.data.base import DataProvider

TENDAYS = timedelta(days=10)
NaN = float('nan')

##########################################################################################

foldl = lambda func, acc, xs: functools.reduce(func, xs, acc)

def optionalGet(dict, *args) : 
    try: 
        return foldl (lambda dict, arg: dict.get(arg), dict, args)
    except AttributeError: 
        return NaN

g = lambda s, *xs : optionalGet(s, *xs)
def gusd (s, *xs) : 
    unit = g(s, *xs, "unit")
    assert(isinstance(unit, str) and unit.lower() == "usd")
    return g(s, *xs, "value")

def text_to_date (text) : # YYYY-MM-DD 
    return np.datetime64(text, 'D')

def expand (l, n) : # Expand list l to length n
    if (len(l) >= n) : return l[:n]
    return np.append(l, np.zeros(n-len(l)) + np.nan)



##########################################################################################

class PolyYahooProvider (DataProvider):
    def __init__ (self, symbol, API_KEY) : 
        self.symbol = symbol

        reference_client = ReferenceClient(API_KEY, connect_timeout=5, read_timeout=5)
        fin: Any = reference_client.get_stock_financials_vx(symbol.upper(), time_frame="annual", limit=10, order="desc") 
        assert(fin['status'] == 'OK')
        statements = fin['results']
        n = len(statements)

        self._ticker = yf.Ticker(symbol)
        self._balance    = self._ticker.balance_sheet
        self._cashflow   = self._ticker.cashflow

        self.revenues           = np.array([gusd(s, "financials", "income_statement", "revenues") for s in statements]) 
        self.invested_cap       = expand(self._balance.loc["Invested Capital"].to_numpy(), n)
        self.gross              = np.array([gusd(s, "financials", "income_statement", "gross_profit") for s in statements])
        self.pretax             = np.array([gusd(s, "financials", "income_statement", "income_loss_from_continuing_operations_before_tax") for s in statements])
        self.net_after_tax      = np.array([gusd(s, "financials", "income_statement", "net_income_loss") for s in statements])
        self._net_per_share     = np.array([g(s, "financials", "income_statement", "basic_earnings_per_share", "value") for s in statements])
        self.shares             = self.net_after_tax / self._net_per_share
        self.income_date        = np.array([text_to_date(g(s, "filing_date")) for s in statements])
        self.oper_cashflow      = np.array([gusd(s, "financials", "cash_flow_statement", "net_cash_flow_from_operating_activities") for s in statements])
        self.free_cashflow      = expand(self._cashflow.loc["Free Cash Flow"].to_numpy(), n)
        self.assets             = np.array([gusd(s, "financials", "balance_sheet", "assets") for s in statements])
        self.current_lia        = np.array([gusd(s, "financials", "balance_sheet", "current_liabilities") for s in statements])
        self.liability          = np.array([gusd(s, "financials", "balance_sheet", "liabilities") for s in statements])

        self.years              = np.array([np.datetime_as_string(d, "Y") for d in self.income_date])

        def get_hist(day):
            try: return self._ticker.history(start=day, end=day+TENDAYS, interval="1d").iloc[0, 3] # Close Price
            except: return NaN

        self.income_price       = np.array([ get_hist(day) for day in self.income_date.astype('datetime64[s]').tolist() ])
        self.price = self._ticker.info["currentPrice"]
