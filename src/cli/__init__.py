from math import isnan
from rich.console import Console
from src.data.polyYahoo import PolyYahooProvider
from src.data.yahoo import YahooProvider
from src.data.polygonio import PolygonProvider
from src.fundamental import Fundamental
import os

class CliTools : 

    def __init__ (self) : 
        self.cons = Console()
        self.commands = {}
        self.cache = {}

    def command (self, f):
        self.commands[f.__name__] = f
        return f

    def cmd (self, name) : 
        if name not in self.commands : 
            return None
        return self.commands[name]

    def cached (self, sym):
        if sym not in self.cache : return None
        else : return self.cache[sym]

    def load(self, symbol: str):
        if symbol in self.cache : return
        try : 
            # self.cache[symbol] = Fundamental(symbol, PolygonProvider, [os.environ["POLYGON_API"]])
            self.cache[symbol] = Fundamental(symbol, PolyYahooProvider, [os.environ["POLYGON_API"]])
        except: 
            self.cache[symbol] = Fundamental(symbol, YahooProvider)

    def clear(self): 
        self.cache = {}

def read (number, unit="", color=True, colrev=0) -> str : 
    def colorize (s) :
        if color == False: return s
        if (number < 0) ^ (colrev) : return '[red]' + s + '[/red]'
        return '[green]' + s + '[/green]'

    def addunit (s) : 
        if isnan(number) : return s
        if unit == "$" : 
            if s[0] == "-" : return "-$" + s[1:]
            else : return "$" + s
        return s + unit

    def scale (num) -> str : 
        s = lambda n : "{:.2f}".format(n)
        if num == None or isnan(num) : 
            return "[purple]NaN[/purple]"
        if abs(num) > 1000_000_000 : 
            return s(num / 1000_000_000) + "B" 
        if abs(num) > 1000_000 : 
            return s(num / 1000_000) + "M" 
        if abs(num) > 1000 : 
            return s(num / 1000) 
        return s(num)
    
    return colorize(addunit(scale(number)))
