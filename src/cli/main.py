from src.cli import CliTools

cli = CliTools()

import src.cli.show
import src.cli.fairprice

def main () : 
    while True : 
        try : 

            try : 
                inp = input("$ ")
                if inp == "" : continue
                if inp == "exit" or inp == "quit" : break
            except Exception as err: 
                break

            args = inp.split(' ')
            command = cli.cmd(args[0])
            if command : 
                command(*args[1:])
            else :
                cli.cons.print("no such command", style="bold red")
        except Exception as e : 
            cli.cons.print("An error occur", style="bold red")
            cli.cons.print(e)
        
