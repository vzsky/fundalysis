# Fundalysis 

A free financial platform

---

currently, a simple financial REPL can be run. This is a proof of concept
<img width="1194" alt="Screenshot 2566-12-28 at 02 55 22" src="https://github.com/vzsky/fundalysis/assets/20735983/5a01ce6f-cc05-423b-abb6-0a1488e55a3c">

To make this actually work in practice, more things are needed to be implement. Also, new, better datasource might be handful. 
If this work, it should be easy to also port into a webapp, instead of just CLI.

---
## Installing

The install script is tested on MacOS and should work for linux. I don't think it will work for windows.

Simply clone this repo, and run `sudo ./install.sh` then feel free to delete the cloned repository. The source should be installed 
and usable. 

Run `fundalysis` to open up the terminal.

Also, in case you want to, run `sudo ./uninstall.sh` to removed all installed packages. 

Note that this needs certain version of python3 and will install packages into the global pip. If this is not desirable, create a virtualenv and use it without using the install script. The cli is accessable by running `./cli.py`. 

--- 
Fundalysis was from "Fund" and "Analysis", not from "Fundamental", though it might sound that way.
