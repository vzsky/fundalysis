from polygon import StocksClient, ReferenceClient
import os
from dotenv import load_dotenv
from typing import Any
import functools
from datetime import datetime, timedelta

load_dotenv()

API_KEY = os.getenv('API_KEY')
if not API_KEY : raise Exception("NO API")

print(API_KEY)

##########################################################################################

foldl = lambda func, acc, xs: functools.reduce(func, xs, acc)

def optionalGet(dict, *args) : 
    try: 
        return foldl (lambda dict, arg: dict.get(arg), dict, args)
    except AttributeError: 
        return None

##########################################################################################

stocks_client = StocksClient(API_KEY, connect_timeout=5, read_timeout=5)
reference_client = ReferenceClient(API_KEY, connect_timeout=5, read_timeout=5)

# current_price = stocks_client.get_previous_close('AMD')
# print(f'Current price for AMD is {current_price}')

fin: Any = reference_client.get_stock_financials_vx("AMD", time_frame="annual", limit=10) 
assert(fin['status'] == 'OK')

statement = fin['results'][0]

def readStatement (stt) : 
    g = lambda *xs : optionalGet(stt, *xs)
    def gusd (*xs) : 
        unit = g(*xs, "unit")
        assert(isinstance(unit, str) and unit.lower() == "usd")
        return g(*xs, "value")
    return {
        "year":                 g("fiscal_year"), 
        "period":               g("fiscal_period"),
        "bal_assets":           gusd("financials", "balance_sheet", "assets"),
        "bal_liabilities":      gusd("financials", "balance_sheet", "liabilities"),
        "bal_curAssets":        gusd("financials", "balance_sheet", "current_assets"),
        "bal_curLiabilities":   gusd("financials", "balance_sheet", "current_liabilities"),
        "bal_equity":           gusd("financials", "balance_sheet", "equity"),
        "cf_operating":         gusd("financials", "cash_flow_statement", "net_cash_flow_from_operating_activities"),
        "cf_operatingCon":      gusd("financials", "cash_flow_statement", "net_cash_flow_from_operating_activities_continuing"),
        "cf_investing":         gusd("financials", "cash_flow_statement", "net_cash_flow_from_investing_activities"),
        "cf_investingCon":      gusd("financials", "cash_flow_statement", "net_cash_flow_from_investing_activities_continuing"),
        "cf_financing":         gusd("financials", "cash_flow_statement", "net_cash_flow_from_financing_activities"),
        "cf_financingCon":      gusd("financials", "cash_flow_statement", "net_cash_flow_from_financing_activities_continuing"),
        "inc_revenues":         gusd("financials", "income_statement", "revenues"),
        "inc_gross":            gusd("financials", "income_statement", "gross_profit"),
        "inc_pretax":           gusd("financials", "income_statement", "income_loss_from_continuing_operations_before_tax"),
        "inc_net":              gusd("financials", "income_statement", "net_income_loss"),
    }

print(readStatement(statement))
