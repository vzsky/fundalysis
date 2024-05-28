import yfinance as yf
import numpy as np
from datetime import timedelta

from src.data.base import DataProvider

TENDAYS = timedelta(days=10)

class YahooProvider (DataProvider) :
    def __init__ (self, symbol) :
        self.symbol = symbol
        self._ticker = yf.Ticker(symbol)

        self._income     = self._ticker.income_stmt
        self._balance    = self._ticker.balance_sheet
        self._cashflow   = self._ticker.cashflow

        self.revenues           = self._income.loc["Total Revenue"]                              .to_numpy()
        self.invested_cap       = self._balance.loc["Invested Capital"]                          .to_numpy()
        self.gross              = self._income.loc["Gross Profit"]                               .to_numpy()
        self.pretax             = self._income.loc["Pretax Income"]                              .to_numpy()
        self.net_after_tax      = self._income.loc["Net Income"]                                 .to_numpy()
        self.shares             = self._balance.loc["Ordinary Shares Number"]                    .to_numpy()
        self.income_date        = self._income.columns                                           .to_numpy()
        self.oper_cashflow      = self._cashflow.loc["Operating Cash Flow"]                      .to_numpy()
        self.free_cashflow      = self._cashflow.loc["Free Cash Flow"]                           .to_numpy()
        self.assets             = self._balance.loc["Total Assets"]                              .to_numpy()
        self.current_lia        = self._balance.loc["Current Liabilities"]                       .to_numpy()
        self.liability          = self._balance.loc["Total Liabilities Net Minority Interest"]   .to_numpy()

        try : 
            income_years              = np.array([np.datetime_as_string(d, "Y") for d in self.income_date])
            balance_years              = np.array([np.datetime_as_string(d, "Y") for d in self._balance.columns])
            cashflow_years              = np.array([np.datetime_as_string(d, "Y") for d in self._cashflow.columns])

            assert(income_years == cashflow_years and balance_years == cashflow_years)
            self.years = income_years
        except: 
            raise Exception("Yahoo Financial Statements conflict")

        def get_hist(day):
            try: return self._ticker.history(start=day, end=day+TENDAYS, interval="1d").iloc[0, 3] # Close Price
            except: return float('nan')

        self.income_price       = np.array([ get_hist(day) for day in self.income_date.astype('datetime64[s]').tolist() ])

        self.price = self._ticker.info["currentPrice"]
