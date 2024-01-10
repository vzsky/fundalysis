from src.cli import CliTools
from rich.table import Table

cli = CliTools()

import src.cli.fairprice   
import src.cli.show       


def help():
    cli.cons.print("** Help - Fundalysis **", style="bold green")

    command = Table(show_header=False)
    command.add_column("Command")
    command.add_column("Function")
    command.add_row("help", "show this message")
    command.add_row("clear", "clear all cache")
    command.add_row("show [symbol]", "show fundamental analysis of [symbol]")
    command.add_row("fairprice (symbol)", "calculate discounted cashflow")
    cli.cons.print(command)



def main():
    while True:
        try:
            try:
                inp = input("$ ")
                if inp == "":
                    continue
                if inp == "help" or inp == "h":
                    help()
                if inp == "exit" or inp == "quit":
                    break
                if inp == "clear" : 
                    cli.clear()
            except Exception as err:
                break

            args = inp.split(" ")
            command = cli.cmd(args[0])
            if command:
                command(*args[1:])
            else:
                cli.cons.print("no such command", style="bold red")
        except Exception as e:
            cli.cons.print("An error occur", style="bold red")
            cli.cons.print(e)
