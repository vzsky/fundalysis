import numpy as np

avg = lambda x : float(sum(x)) / len(x)
def growth (x) :
    num = (100.0 * (x[:-1] - x[1:])) 
    dem = np.array([a if a != 0 else np.nan for a in x[1:]])
    return num / dem

class Fundamental :
    def __init__(self, symbol, dataProvider, aux=[]):

        self.data = dataProvider(symbol, *aux)
        self.symbol = symbol

        ################################################################
        #                        Copy Into Self                        #
        ################################################################

        self.price = self.data.price
        self.years = self.data.years

        self.revenues = self.data.revenues 
        self.gross = self.data.gross
        self.pretax = self.data.pretax 
        self.net_after_tax = self.data.net_after_tax
        self.oper_cashflow = self.data.oper_cashflow
        self.free_cashflow = self.data.free_cashflow
        self.shares = self.data.shares
        self.income_price = self.data.income_price
        self.invested_cap = self.data.invested_cap
        self.assets = self.data.assets
        self.liability = self.data.liability
        self.current_lia = self.data.current_lia

        ################################################################
        #                     Metrics Calculation                      #
        ################################################################

        self.rev_growth         = growth(self.revenues)
        self.rev_growth_avg3    = avg(self.rev_growth[:3])

        self.net_growth         = growth(self.net_after_tax)
        self.net_growth_avg3    = avg(self.net_growth[:3])
        
        self.fcf_growth         = growth(self.free_cashflow)
        self.fcf_growth_avg3    = avg(self.fcf_growth[:3])

        self.share_growth       = growth(self.shares)
        self.share_growth_avg3  = avg(self.share_growth[:3])

        self.roic               = 100.0 * self.net_after_tax / self.invested_cap
        self.roic_avg4          = avg(self.roic[:4])

        self.pe                 = (self.price * self.shares[0]) / self.net_after_tax[0]
        self.historic_pe        = self.income_price / self.net_after_tax * self.shares 
        self.historic_pe_avg4   = avg(self.historic_pe[:4])

        self.pfcf               = (self.price * self.shares[0]) / self.free_cashflow[0]
        self.historic_pfcf      = self.income_price / self.free_cashflow * self.shares 
        self.historic_pfcf_avg4 = avg(self.historic_pfcf[:4])

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


def disc_earning (sale_per_share, year, growth, net_margin, pe, discount) : 

    # calculate earning per share in each year and add up with annual discount. 
    # at the end of all years, add up the terminal value at given pe multiple. 
    # returns the fair price when the given condition are met.

    # replace net_margin and pe with fcf_margin and pfcf to ge tthe discount free cash flow model.
    r = (1+growth)/(1+discount)
    n = year
    mul = n if r == 1 else (r - r**(n+1)) / (1-r)
    return (0.01 * net_margin * sale_per_share) * ( mul  + (r**n) * pe)


