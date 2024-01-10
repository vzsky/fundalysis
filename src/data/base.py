import numpy as np

class DataProvider : 

    revenues = np.array([])
    invested_cap = np.array([])
    gross = np.array([])
    pretax = np.array([])
    net_after_tax = np.array([])
    shares = np.array([])
    income_date = np.array([]) # Date on income statement
    oper_cashflow = np.array([])
    free_cashflow = np.array([])
    assets = np.array([])
    current_lia = np.array([])
    liability = np.array([])
    years = np.array([])
    income_price = np.array([]) # Price on income_date
    price = 0 # Current price

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
