

import pandas as pd
import numpy as np
import requests

try:
    from requests_html import HTMLSession
except Exception:
    pass


def force_float(elt):
    
    try:
        return float(elt)
    except:
        return elt

def build_options_url(ticker, date = None):
    
    """Constructs the URL pointing to options chain"""
       
    url = "https://finance.yahoo.com/quote/" + ticker + "/options?p=" + ticker

    if date is not None:
        url = url + "&date=" + str(int(pd.Timestamp(date).timestamp()))

    return url

def get_options_chain(ticker, date = None, raw = True, headers = {'User-agent': 'Mozilla/5.0'}):
    
    """Extracts call / put option tables for input ticker and expiration date.  If
       no date is input, the default result will be the earliest expiring
       option chain from the current date.
    
       @param: ticker
       @param: date"""    
    
    site = build_options_url(ticker, date)
    
    tables = pd.read_html(requests.get(site, headers=headers).text)
    
    if len(tables) == 1:
        calls = tables[0].copy()
        puts = pd.DataFrame(columns = calls.columns)
    else:
        calls = tables[0].copy()
        puts = tables[1].copy()
    
    if not raw:
        calls["% Change"] = calls["% Change"].str.strip("%").map(force_float)
        calls["% Change"] = calls["% Change"].map(lambda num: num / 100 if isinstance(num, float) else 0)
        calls["Volume"] = calls["Volume"].str.replace("-", "0").map(force_float)
        calls["Open Interest"] = calls["Open Interest"].str.replace("-", "0").map(force_float)
        
        
        puts["% Change"] = puts["% Change"].str.strip("%").map(force_float)
        puts["% Change"] = puts["% Change"].map(lambda num: num / 100 if isinstance(num, float) else 0)
        puts["Volume"] =puts["Volume"].str.replace("-", "0").map(force_float)
        puts["Open Interest"] = puts["Open Interest"].str.replace("-", "0").map(force_float)
        
    
    
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
    
    html = resp.html.raw_html.decode()
    
    splits = html.split("</option>")
    
    dates = [elt[elt.rfind(">"):].strip(">") for elt in splits]
    
    dates = [elt for elt in dates if elt != '']
    
    session.close()
    
    return dates
    



    
    
    
    
    
    
    
    

    
