from .main import cli

from src.fundamental import disc_earning

@cli.command
def fairprice (symbol = None) : 
    if symbol != None and not cli.cached(symbol) : cli.load(symbol)
    ticker = cli.cached(symbol)

    year        = int(  input("year of simulation: "))
    growth      = float(input("expected growth (%): "))
    net_margin  = float(input("expected [net | fcf] margin (%): "))
    pe          = float(input("expected [P/E | P/FCF] after the period: "))
    discount    = float(input("desired annual return (%): "))

    if ticker : 
        res = ticker.disc_earning(year, growth/100, net_margin, pe, discount/100)
    else :
        sale_ps     = float(input("current sales per share: "))
        res = disc_earning(sale_ps, year, growth/100, net_margin, pe, discount/100)

    cli.cons.print(f"The fair price is [b][cyan]${'{:.2f}'.format(res)}[/cyan][/b]")
