

import requests
from pandas.io.json import json_normalize
import pandas as pd
import ftplib
import io

def build_url(ticker, start_date = None, end_date = None):
    
    if end_date is None:  
        end_seconds = int(pd.Timestamp("now").timestamp())
        
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
    '''Downloads historical stock price data into a pandas data frame 
    
       @param: ticker
       @param: start_date = None
       @param: end_date = None
       @param: index_as_date = True
    '''
    
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
    
    temp = pd.json.loads(needed)
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
    '''Downloads list of tickers currently listed in the S&P 500 '''
    # get list of all S&P 500 stocks
    sp500 = pd.read_html("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")[0]
    sp_tickers = sp500[0].tolist()
    sp_tickers = [x for x in sp_tickers if x != "Ticker symbol"]

    return sp_tickers


def tickers_nasdaq():
    
    '''Downloads list of tickers currently listed in the NASDAQ'''
    
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
    '''Downloads list of tickers currently listed in the "otherlisted.txt"
       file on "ftp.nasdaqtrader.com" '''
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
    
    
def tickers_dow():
    
    '''Downloads list of currently traded tickers on the Dow'''

    site = "https://finance.yahoo.com/quote/%5EDJI/components?p=%5EDJI"
    
    table = pd.read_html(site)[0]

    dow_tickers = sorted(table['Symbol'].tolist())
    
    return dow_tickers    
    

def get_quote_table(ticker , dict_result = True): 
    
    '''Scrapes data elements found on Yahoo Finance's quote page 
       of input ticker
    
       @param: ticker
       @param: dict_result = True
    '''

    site = "https://finance.yahoo.com/quote/" + ticker + "?p=" + ticker
    
    tables = pd.read_html(site)

    data = tables[0].append(tables[1])

    data.columns = ["attribute" , "value"]

    price_etc = [elt for elt in tables if elt.iloc[0][0] == "Previous Close"][0]
    price_etc.columns = data.columns.copy()
    
    data = data.append(price_etc)
    
    data = data.sort_values("attribute")
    
    data = data.drop_duplicates().reset_index(drop = True)

    if dict_result:
        
        result = {key : val for key,val in zip(data.attribute , data.value)}
        return result
        
    return data    
    
    

def get_stats(ticker):
    
    '''Scrapes information from the statistics tab on Yahoo Finance 
       for an input ticker 
    
       @param: ticker
    '''

    stats_site = "https://finance.yahoo.com/quote/" + ticker + \
                 "/key-statistics?p=" + ticker
    

    tables = pd.read_html(stats_site)
    
    
    table = tables[0]
    for elt in tables[1:]:
        table = table.append(elt)

    table.columns = ["Attribute" , "Value"]
    
    table = table.reset_index(drop = True)
    
    return table
        

def get_income_statement(ticker):
    
    '''Scrape income statement from Yahoo Finance for a given ticker
    
       @param: ticker
    '''
    
    income_site = "https://finance.yahoo.com/quote/" + ticker + \
            "/financials?p=" + ticker
    

    tables = pd.read_html(income_site , header = 0)
    
    table = [table for table in tables if 'Revenue' in str(table)][0]    
    


    return table
        

def get_balance_sheet(ticker):
    
    '''Scrapes balance sheet from Yahoo Finance for an input ticker 
    
       @param: ticker
    '''    
    
    balance_sheet_site = "https://finance.yahoo.com/quote/" + ticker + \
                         "/balance-sheet?p=" + ticker
    
    
    tables = pd.read_html(balance_sheet_site , header = 0)
    
    table = [table for table in tables if 'Period Ending' in str(table)][0]    
    

    return table
        

def get_cash_flow(ticker):
    
    '''Scrapes the cash flow statement from Yahoo Finance for an input ticker 
    
       @param: ticker
    '''
    
    cash_flow_site = "https://finance.yahoo.com/quote/" + \
            ticker + "/cash-flow?p=" + ticker
    
    

    tables = pd.read_html(cash_flow_site , header = 0)
    
    table = [table for table in tables if 'Period Ending' in str(table)][0]    
    

    return table

def get_holders(ticker):
    
    '''Scrapes the Holders page from Yahoo Finance for an input ticker 
    
       @param: ticker
    '''    
    
    holders_site = "https://finance.yahoo.com/quote/" + \
                    ticker + "/holders?p=" + ticker
    
        
    tables = pd.read_html(holders_site , header = 0)
    
       
    table_names = ["Major Holders" , "Direct Holders (Forms 3 and 4)" ,
                   "Top Institutional Holders" , "Top Mutual Fund Holders"]
     
    
    table_mapper = {key : val for key,val in zip(table_names , tables)}
                   
                   
    return table_mapper       

def get_analysts_info(ticker):
    
    '''Scrapes the Analysts page from Yahoo Finance for an input ticker 
    
       @param: ticker
    '''    
    
    
    analysts_site = "https://finance.yahoo.com/quote/" + ticker + "/analysts?p=" + ticker
    
    tables = pd.read_html(analysts_site , header = 0)
    
    table_names = [table.columns[0] for table in tables]

    table_mapper = {key : val for key , val in zip(table_names , tables)}
    

    return table_mapper
        
        
        
        
        
        
        
