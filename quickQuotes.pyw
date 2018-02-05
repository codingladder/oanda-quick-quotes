# Noel Caceres
# quickQuotes.py
# get quick quotes from Oanda currency pairs
# uses Oanda API to get prices and displays them 
# tested on python 2.7

from Tkinter import *
import Tkinter as tk
import ttk
import time
from threading import Thread
from credentials import ACCOUNT_NUMBER, TOKEN
from quote import *

instrumentList = ("EUR/USD", "USD/JPY", "USD/CHF", "GBP/USD"
                  ,"AUD/USD", "USD/CAD", "EUR/JPY", "EUR/GBP")
prevTimeStamp = ""

# Function
# starts streaming quotes 
def streamQuotes(prevInstrument):
    symbol = str(instrument.get())
    # new Quote needs account number, symbol, and api token
    pQuote = Quote(ACCOUNT_NUMBER, symbol, TOKEN)
    timeStamp = pQuote.getTimeStamp()

    # only display new quote if there's an updated one
    global prevTimeStamp
    if timeStamp != prevTimeStamp:
        ask = str(pQuote.getAsk())  # quote ASK price
        bid = str(pQuote.getBid())  # quote BID price
        text = "\n\t  "+timeStamp+"\t\t\t"+"ask: "+ask+"\t\t"+"bid: "+bid
        try:
            # check if it's the same
            if symbol != prevInstrument:
                # if not then display new symbol
                consoleText.insert(END, "\n\n  "+symbol)
            consoleText.insert(END, text )
        except TclError:    
            exit()
        prevInstrument = symbol
        
    prevTimeStamp = timeStamp
    time.sleep(1)                # set to 1 sec. quotes
    streamQuotes(prevInstrument) # get next quote


pricesStarted = False       # to keep track if quotes have started
prevInstrument = ""
prevTimeStamp = ""
root = Tk()
root.geometry("550x700")
root.title("Quick Quotes")
console_rows = 0
max_console_rows = 20
inputFrame = Frame(root, width="200")
inputFrame.pack(pady=7, padx=7)

ttk.Label(inputFrame, text="Instrument:").grid(column=1, row=0)
instrument = tk.StringVar()
instrument_chosen = ttk.Combobox(inputFrame, width=12, textvariable=instrument)
instrument_chosen['values'] = instrumentList
instrument_chosen.grid(column=1, row=1)
instrument_chosen.current(0)  # choose first by default

consoleFrame = Frame(root)
consoleFrame.pack(expand=1, pady=15, padx=15, fill= BOTH)
consoleText = Text(consoleFrame, fg="white", bg="black",state=DISABLED)
consoleText.pack(expand=1, fill= BOTH)
consoleText.config(state=NORMAL)
pQuote = Quote(ACCOUNT_NUMBER, str(instrument.get()), TOKEN)

# if the price stream has NOT started
if pricesStarted == False:
    # thread to run prices stream
    t = Thread(target=streamQuotes, args=(prevInstrument,))
    pricesStarted = True
    t.start()

root.mainloop()


