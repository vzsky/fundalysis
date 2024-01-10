# ADD SHEBANG TO MAKE EXECUTABLE /usr/bin/env python3

########################### Block CTRL-C ###########################
import signal

def signal_handler(sig, frame):
    pass # do something to return back to shell, or just do nothing

signal.signal(signal.SIGINT, signal_handler)

####################################################################

from src.cli.main import main

from dotenv import load_dotenv

if __name__ == "__main__" :
    load_dotenv()
    main()
