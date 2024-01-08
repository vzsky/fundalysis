import yfinance as yf
import numpy as np
from datetime import datetime, timedelta

avg = lambda x : float(sum(x)) / len(x)
growth = lambda x : 100.0 * (x[:-1] - x[1:]) / x[1:]

TWOWEEKS = timedelta(days=14)

class Fundamental :
    def __init__(self, symbol):

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

        ################################################################
        #                     Metrics Calculation                      #
        ################################################################

        self.rev_growth         = growth(self.revenues)
        self.rev_growth_avg3    = avg(self.rev_growth)

        self.net_growth         = growth(self.net_after_tax)
        self.net_growth_avg3    = avg(self.net_growth)
        
        self.fcf_growth         = growth(self.free_cashflow)
        self.fcf_growth_avg3    = avg(self.fcf_growth)

        self.share_growth       = growth(self.shares)
        self.share_growth_avg3  = avg(self.share_growth)

        self.roic               = 100.0 * self.net_after_tax / self.invested_cap
        self.roic_avg4          = avg(self.roic)

        self.pe                 = (self.price * self.shares[0]) / self.net_after_tax[0]
        self.historic_pe        = self.income_price / self.net_after_tax * self.shares 
        self.historic_pe_avg4   = avg(self.historic_pe)

        self.pfcf               = (self.price * self.shares[0]) / self.free_cashflow[0]
        self.historic_pfcf      = self.income_price / self.free_cashflow * self.shares 
        self.historic_pfcf_avg4 = avg(self.historic_pfcf)

        self.li_per_fcf         = self.liability / self.free_cashflow

        self.gross_margin       = 100.0 * self.gross / self.revenues
        self.pretax_margin      = 100.0 * self.pretax / self.revenues
        self.net_margin         = 100.0 * self.net_after_tax / self.revenues
        self.fcf_margin         = 100.0 * self.free_cashflow / self.revenues

        self.current_lia_ratio  = 100.0 * self.current_lia / self.liability
        self.assets_lia_ratio   = self.assets / self.liability


    ################################################################
    #       Discount Earning Model / Discount Free Cash Flow       #
    ################################################################

    def disc_earning (self, year, growth, net_margin, pe, discount) : 

        # calculate earning per share in each year and add up with annual discount. 
        # at the end of all years, add up the terminal value at given pe multiple. 
        # returns the fair price when the given condition are met.

        # replace net_margin and pe with fcf_margin and pfcf to ge tthe discount free cash flow model.
        shares = self.shares[0]
        revenue = self.revenues[0]

        r = (1+growth)/(1+discount)
        n = year
        mul = n if r == 1 else (r - r**(n+1)) / (1-r)
        return ((0.01 * net_margin * revenue) / shares) * ( mul  + (r**n) * pe)


