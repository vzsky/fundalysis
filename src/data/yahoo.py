import yfinance as yf
import numpy as np
from datetime import datetime, timedelta

TWOWEEKS = timedelta(days=14)

class YahooProvider :
    def __init__ (self, symbol) : 
        self.symbol = symbol
        self.ticker = yf.Ticker(symbol)

        self.income     = self.ticker.income_stmt
        self.balance    = self.ticker.balance_sheet
        self.cashflow   = self.ticker.cashflow

        self.revenues           = self.income.loc["Total Revenue"]                              .to_numpy()
        self.invested_cap       = self.balance.loc["Invested Capital"]                          .to_numpy()
        self.gross              = self.income.loc["Gross Profit"]                               .to_numpy()
        self.pretax             = self.income.loc["Pretax Income"]                              .to_numpy()
        self.net_after_tax      = self.income.loc["Net Income"]                                 .to_numpy()
        self.shares             = self.balance.loc["Ordinary Shares Number"]                    .to_numpy()
        self.income_date        = self.income.columns                                           .to_numpy()
        self.oper_cashflow      = self.cashflow.loc["Operating Cash Flow"]                      .to_numpy()
        self.free_cashflow      = self.cashflow.loc["Free Cash Flow"]                           .to_numpy()
        self.assets             = self.balance.loc["Total Assets"]                              .to_numpy()
        self.current_lia        = self.balance.loc["Current Liabilities"]                       .to_numpy()
        self.liability          = self.balance.loc["Total Liabilities Net Minority Interest"]   .to_numpy()

        self.years              = np.array([np.datetime_as_string(d, "Y") for d in self.income_date])

        def get_hist(day):
            try: return self.ticker.history(start=day, end=day+TWOWEEKS, interval="1d").iloc[0, 3] # Close Price
            except: return float('nan')

        self.income_price       = np.array([ get_hist(day) for day in self.income_date.astype('datetime64[s]').tolist() ])

        self.price = self.ticker.info["currentPrice"]
