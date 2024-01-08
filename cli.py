#!/usr/bin/env python3

from src.fundamental import Fundamental
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.columns import Columns
from math import isnan
import readline                     # Need this unused import   

import signal

def signal_handler(sig, frame):
    pass # do something to return back to shell, or just do nothing

signal.signal(signal.SIGINT, signal_handler)

####################################################################

cons = Console()

history = []
commands = {}
cache = {}

def read (number, unit="", color=True, colrev=0) -> str : 
    def colorize (s) :
        if color == False: return s
        if (number < 0) ^ (colrev) : return '[red]' + s + '[/red]'
        return '[green]' + s + '[/green]'

    def addunit (s) : 
        if isnan(number) : return s
        if unit == "$" : return "$" + s
        return s + unit

    def scale (num) -> str : 
        s = lambda n : "{:.2f}".format(n)
        if isnan(num) : 
            return "[purple]NaN[/purple]"
        if abs(num) > 1000_000_000 : 
            return s(num / 1000_000_000) + "B" 
        if abs(num) > 1000_000 : 
            return s(num / 1000_000) + "M" 
        if abs(num) > 1000 : 
            return s(num / 1000) 
        return s(num) 

    return colorize(addunit(scale(number)))

def command (f):
    commands[f.__name__] = f
    return f

@command
def load(symbol: str):
    if symbol in cache : return
    cache[symbol] = Fundamental(symbol)

@command
def show(symbol: str):
    if symbol not in cache : load(symbol)
    ticker = cache[symbol]

    cons.print()
    cons.print("Fundalysis of", ticker.symbol.upper(), style="bold")

    basic = Table(show_header=False)
    basic.add_column("Metric")
    basic.add_column("Value", justify="right")
    basic.add_row("Current Price", read(ticker.price, "$", color=False))
    basic.add_row("Current P/E", read(ticker.pe, "x"))
    basic.add_row("Current P/FCF", read(ticker.pfcf, "x"))

    cons.print(basic)

    growth = Table(show_header=True, header_style="bold")
    growth.add_column("")
    for c in ticker.years[:-1] : 
        growth.add_column(c, justify="right")
    growth.add_column("3Y average", justify="right")
    growth.add_row("Revenue growth", *[ read(g, "%") for g in ticker.rev_growth ], read(ticker.rev_growth_avg3, "%"))
    growth.add_row("Earning growth", *[ read(g, "%") for g in ticker.net_growth ], read(ticker.net_growth_avg3, "%"))
    growth.add_row("Free Cash Flow growth", *[ read(g, "%") for g in ticker.fcf_growth ], read(ticker.fcf_growth_avg3, "%"))
    growth.add_row("Share Outstanding growth", *[ read(g, "%", colrev=1) for g in ticker.share_growth ], 
                   read(ticker.share_growth_avg3, "%", colrev=1))

    cons.print(growth)

    value = Table(show_header=True, header_style="bold") 
    value.add_column("")
    for c in ticker.years: 
        value.add_column(c, justify="right")

    value.add_row("Revenue", *[ read(g, "$") for g in ticker.revenues ])
    value.add_row("Gross Profit", *[ read(g, "$") for g in ticker.gross ])
    value.add_row("Pretax Income", *[ read(g, "$") for g in ticker.pretax ])
    value.add_row("Net Income", *[ read(g, "$") for g in ticker.net_after_tax])
    value.add_row("Gross Margin", *[ read(g, "%") for g in ticker.gross_margin ])
    value.add_row("Pretax Margin", *[ read(g, "%") for g in ticker.pretax_margin ])
    value.add_row("Net Margin", *[ read(g, "%") for g in ticker.net_margin ])
    value.add_row("Free Cash Flow Margin", *[ read(g, "%") for g in ticker.fcf_margin ])
    value.add_row()
    value.add_row("Operating Cash Flow", *[ read(g, "$") for g in ticker.oper_cashflow ])
    value.add_row("Free Cash Flow", *[ read(g, "$") for g in ticker.free_cashflow ])
    value.add_row()
    value.add_row("Asset", *[ read(g, "$") for g in ticker.assets ])
    value.add_row("Liability", *[ read(g, "$") for g in ticker.liability ])
    value.add_row("Current Liability", *[ read(g, "$") for g in ticker.current_lia ])
    value.add_row("Current Liability Ratio", *[ read(g, "%") for g in ticker.current_lia_ratio ])
    value.add_row("Asset / Liability", *[ read(g, "x") for g in ticker.assets_lia_ratio ]) 
    value.add_row()
    value.add_row("ROIC", *[ read(g, "%") for g in ticker.roic ])
    value.add_row("P/E", *[ read(g, "x") for g in ticker.historic_pe ])
    value.add_row("P/FCF", *[ read(g, "x") for g in ticker.historic_pfcf ])

    cons.print(value)
    
    cons.print("Checklists", style="bold")
    def chcol (n, f, u="") : 
        s = read(n, u, False)
        if (f(n)) : 
            return f"[green]{s}[/green]"
        return f"[red]{s}[/red]"

    cons.print(Columns([
        Panel(f"4 year P/E RATIO \nis at {chcol(ticker.historic_pe_avg4, lambda x: x < 23, 'x')}"),
        Panel(f"4 year P/FCF RATIO \nis at {chcol(ticker.historic_pfcf_avg4, lambda x: x < 23, 'x')}"), 
        Panel(f"4 year ROIC \nis at {chcol(ticker.roic_avg4, lambda x: x > 10, '%')}"), 
        Panel(f"3 year Revenue Growth \nis at {chcol(ticker.rev_growth_avg3, lambda x: x > 1, '%')}"), 
        Panel(f"3 year Net Income Growth \nis at {chcol(ticker.net_growth_avg3, lambda x: x > 1, '%')}"),  
        Panel(f"3 year Share Buyback \nis at {chcol(ticker.share_growth_avg3, lambda x: x < -1, '%')}"), 
        Panel(f"3 year Cash Flow Growth \nis at {chcol(ticker.fcf_growth_avg3, lambda x: x > 1, '%')}"), 
        Panel(f"Liability Per Free Cash Flow \nis at {chcol(ticker.li_per_fcf[0], lambda x: x < 3, 'x')}"), 
    ]))

@command
def fairprice (symbol) : 
    if symbol not in cache : load(symbol)
    ticker = cache[symbol]

    year        = int(  input("year of simulation: "))
    growth      = float(input("expected growth (%): "))
    net_margin  = float(input("expected [net | fcf] margin (%): "))
    pe          = float(input("expected [P/E | P/FCF] after the period: "))
    discount    = float(input("desired annual return (%): "))

    res = ticker.disc_earning(year, growth/100, net_margin, pe, discount/100)

    cons.print(f"The fair price is [b][cyan]${'{:.2f}'.format(res)}[/cyan][/b]")

if __name__ == "__main__":

    while True : 
        try : 
            try : 
                inp = input("$ ")
                if inp == "" : continue
                if inp == "exit" : break
            except Exception as err: 
                break
            history.append(inp)
            args = inp.split(' ')
            if args[0] in commands : 
                commands[args[0]](*args[1:])
            else :
                cons.print("no such command", style="bold red")
        except Exception as e : 
            cons.print("An error occur", style="bold red")
            cons.print(e)
        
