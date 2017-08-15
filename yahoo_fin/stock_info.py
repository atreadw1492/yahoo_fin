import requests
import json
from pandas.io.json import json_normalize
import pandas as pd
import time
import ftplib
import io

def build_url(ticker, start_date = None, end_date = None):
    
    if end_date is None:
        end_seconds = round(time.time())    
        
    else:
        end_seconds = int(pd.Timestamp(end_date).timestamp())
        
    if start_date is None:
        start_seconds = 7223400    
        
    else:
        start_seconds = int(pd.Timestamp(start_date).timestamp())
        
        
    site = "https://finance.yahoo.com/quote/" + ticker + "/history?period1=" + str(int(start_seconds)) + "&period2=" + \
            str(end_seconds) + "&interval=1d&filter=history&frequency=1d"
    return site


def get_data(ticker, start_date = None, end_date = None, index_as_date = True):

    
    site = build_url(ticker , start_date , end_date)
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
    result = result[["date","open","high","low","close","adjclose","volume"]]
    
    # fix date field
    result['date'] = result['date'].map(lambda x: pd.datetime.fromtimestamp(x).date())
    
    result['ticker'] = ticker.upper()

    result = result.dropna()
    result = result.reset_index(drop = True)
    
    if index_as_date:
        result.index = result.date.copy()
        result = result.sort_values("date")
        del result["date"]

    

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
    

def get_quote_table(ticker , dict_result = True): 

    site = "https://finance.yahoo.com/quote/" + ticker + "?p=" + ticker
    
    tables = pd.read_html(site)

    data = tables[1].append(tables[2])

    data.columns = ["attribute" , "value"]

    price_etc = [elt for elt in tables if elt.iloc[0][0] == "Previous Close"][0]
    price_etc.columns = data.columns.copy()
    
    data = data.append(price_etc)
    
    data = data.sort_values("attribute")

    if dict_result:
        
        result = {key : val for key,val in zip(data.attribute , data.value)}
        return result
        
    return data    
    
    
    
    
    


