from . import read
from .main import cli

from rich.table import Table
from rich.panel import Panel
from rich.columns import Columns

def show_basic (ticker) : 
    basic = Table(show_header=False)
    basic.add_column("Metric")
    basic.add_column("Value", justify="right")
    basic.add_row("Current Price", read(ticker.price, "$", color=False))
    basic.add_row("Current P/E", read(ticker.pe, "x"))
    basic.add_row("Current P/FCF", read(ticker.pfcf, "x"))

    cli.cons.print(basic)

def show_growth (ticker) : 
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

    cli.cons.print(growth)

def show_value (ticker) :
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
    value.add_row("Shares Outstanding", *[ read(g, "") for g in ticker.shares ])
    value.add_row()
    value.add_row("Price", *[ read(g, "$") for g in ticker.income_price ])
    value.add_row("P/E", *[ read(g, "x") for g in ticker.historic_pe ])
    value.add_row("P/FCF", *[ read(g, "x") for g in ticker.historic_pfcf ])

    cli.cons.print(value)

def show_checklist (ticker) :  
    cli.cons.print("Checklists", style="bold")
    def chcol (n, f, u="") : 
        s = read(n, u, False)
        if (f(n)) : 
            return f"[green]{s}[/green]"
        return f"[red]{s}[/red]"

    cli.cons.print(Columns([
        Panel(f"3 year P/E RATIO \nis at {chcol(ticker.historic_pe_avg3, lambda x: x < 23, 'x')}"),
        Panel(f"3 year P/FCF RATIO \nis at {chcol(ticker.historic_pfcf_avg3, lambda x: x < 23, 'x')}"), 
        Panel(f"3 year ROIC \nis at {chcol(ticker.roic_avg3, lambda x: x > 10, '%')}"), 
        Panel(f"3 year Revenue Growth \nis at {chcol(ticker.rev_growth_avg3, lambda x: x > 1, '%')}"), 
        Panel(f"3 year Net Income Growth \nis at {chcol(ticker.net_growth_avg3, lambda x: x > 1, '%')}"),  
        Panel(f"3 year Share Buyback \nis at {chcol(ticker.share_growth_avg3, lambda x: x < -1, '%')}"), 
        Panel(f"3 year Cash Flow Growth \nis at {chcol(ticker.fcf_growth_avg3, lambda x: x > 1, '%')}"), 
        Panel(f"Liability Per Free Cash Flow \nis at {chcol(ticker.li_per_fcf[0], lambda x: x < 3, 'x')}"), 
    ]))

@cli.command
def show(symbol: str):
    if not cli.cached(symbol) : cli.load(symbol)
    ticker = cli.cached(symbol)
    if not ticker : return

    cli.cons.print()
    cli.cons.print("Fundalysis of", ticker.symbol.upper(), style="bold")

    show_basic(ticker)
    show_growth(ticker)
    show_value(ticker)
    show_checklist(ticker)    
