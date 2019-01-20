

import pandas as pd

try:
    from requests_html import HTMLSession
except Exception:
    pass

def build_options_url(ticker, date = None):
    
    """Constructs the URL pointing to options chain"""
       
    url = "https://finance.yahoo.com/quote/" + ticker + "/options?p=" + ticker

    if date is not None:
        url = url + "&date=" + str(int(pd.Timestamp(date).timestamp()))

    return url

def get_options_chain(ticker, date = None):
    
    """Extracts put option table for input ticker and expiration date.  If
       no date is input, the default result will be the earliest expiring
       option chain from the current date.
    
       @param: ticker
       @param: date"""    
    
    site = build_options_url(ticker, date)
    
    tables = pd.read_html(site)

    
    calls = tables[0].copy()
    puts = tables[1].copy()
    
    return {"calls": calls, "puts":puts}    
    
    
def get_calls(ticker, date = None):

    """Extracts call option table for input ticker and expiration date
    
       @param: ticker
       @param: date"""
       
    options_chain = get_options_chain(ticker, date)
    
    return options_chain["calls"]
    
    

def get_puts(ticker, date = None):

    """Extracts put option table for input ticker and expiration date
    
       @param: ticker
       @param: date"""
    
    options_chain = get_options_chain(ticker, date)
    
    return options_chain["puts"]    

    
def get_expiration_dates(ticker):

    """Scrapes the expiration dates from each option chain for input ticker
    
       @param: ticker"""
    
    site = build_options_url(ticker)
    
    session = HTMLSession()
    resp = session.get(site)
    resp.html.render()
    
    html = resp.html.raw_html.decode()
    
    splits = html.split("</option>")
    
    dates = [elt[elt.rfind(">"):].strip(">") for elt in splits]
    
    dates = [elt for elt in dates if elt != '']
    
    session.close()
    
    return dates
    



    
    
    
    
    
    
    
    

    
