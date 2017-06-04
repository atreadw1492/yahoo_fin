# -*- coding: utf-8 -*-
"""
Created on Sat Jun  3 15:58:56 2017

@author: atrea
"""

import requests
import json
from pandas.io.json import json_normalize
import pandas as pd
import time
import ftplib
import io

def build_url(ticker):
    
    current_seconds = round(time.time())    
    site = "https://finance.yahoo.com/quote/" + ticker + "/history?period1=7223400&period2=" + \
            str(current_seconds) + "&interval=1d&filter=history&frequency=1d"
    return site


def get_data(ticker):

    
    site = build_url(ticker)
    resp = requests.get(site)
    html = resp.content
    html = html.decode()
    
    start = html.index('"HistoricalPriceStore"')
    end = html.index("firstTradeDate")
    
    needed = html[start:end]
    needed = needed.strip('"HistoricalPriceStore":')
    needed = needed.strip(""","isPending":false,'""")
    needed = needed + "}"
    
    temp = json.loads(needed)
    result = json_normalize(temp['prices'])
    result = result[["date","open","high","low","close","unadjclose","volume"]]
    
    # fix date field
    result['date'] = result['date'].map(lambda x: pd.datetime.fromtimestamp(x).date())
    
    result['ticker'] = ticker

    return result



def tickers_sp500():
    # get list of all S&P 500 stocks
    sp500 = pd.read_html("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")[0]
    sp_tickers = sp500[0].tolist()
    sp_tickers = [x for x in sp_tickers if x != "Ticker symbol"]

    return sp_tickers


def tickers_nasdaq():
    
    ftp = ftplib.FTP("ftp.nasdaqtrader.com")
    ftp.login()
    ftp.cwd("SymbolDirectory")
    
    r = io.BytesIO()
    ftp.retrbinary('RETR nasdaqlisted.txt', r.write)
    
    info = r.getvalue().decode()
    splits = info.split("|")
    
    tickers = [x for x in splits if "N\r\n" in x]
    tickers = [x.strip("N\r\n") for x in tickers]
    
    ftp.close()    

    return tickers
    
    

def tickers_other():
    
    ftp = ftplib.FTP("ftp.nasdaqtrader.com")
    ftp.login()
    ftp.cwd("SymbolDirectory")
    
    r = io.BytesIO()
    ftp.retrbinary('RETR otherlisted.txt', r.write)
    
    info = r.getvalue().decode()
    splits = info.split("|")
    
    tickers = [x for x in splits if "N\r\n" in x]
    tickers = [x.strip("N\r\n") for x in tickers]
    tickers = [x.split("\r\n") for x in tickers]
    tickers = [sublist for outerlist in tickers for sublist in outerlist]
    
    ftp.close()    

    return tickers
    

    
    
    
    
    
    


