# Fundalysis 

A free financial platform

---

currently, a simple financial REPL can be run. This is a proof of concept
<img width="1194" alt="Screenshot 2566-12-28 at 02 55 22" src="https://github.com/vzsky/fundalysis/assets/20735983/5a01ce6f-cc05-423b-abb6-0a1488e55a3c">

If this work, it should be easy to also port into a webapp, instead of just CLI.

---
## Installing

Auto install script was remove. You are adviced to create virtual environment and run the `cli.py` in the environment for the REPL.
This package needs (although relaxable, mention more below) [polygon](https://polygon.io/) free API key, which should be put in the 
`.env` file.

### Relaxing the API key
One can use this with no API key via yfinance, by editting the `cli/__init__.py` to use yfinance instead. 
However, only 2-4 years of data will be shown and the API is less reliable than the polygon.

--- 
Fundalysis was from "Fund" and "Analysis", not from "Fundamental", though it might sound that way.
