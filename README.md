# yahoo_fin
Scrape stock price history from new (Spring 2017) Yahoo Finance layout

If you're familiar with the "get_data_yahoo" method in pandas.io.data, this package's main purpose is to serve as an updated replacement
based off Yahoo Finance's recent change in layout and its API (Spring 2017).  Also, yahoo_fin provides functionality to scrape the current stocks comprising the S&P 500, as well as well as the NASDAQ. 

Download using pip:

```batch
pip install yahoo_fin
```

yahoo_fin contains one module, "stock_info."  The main function within stock_info is "get_data."  This function takes a ticker symbol as input (e.g. "nflx"), and outputs a data frame containing open, close, high, low, adjusted close, and volume information.  


Examples:

```python
from yahoo_fin.stock_info import get_data, tickers_sp500, tickers_nasdaq, tickers_other

""" pull historical data for Netflix (NFLX) """
nflx = get_data("NFLX")

""" pull data for Apple (AAPL) """
"""case sensitivity does not matter"""
aapl = get_data("aapl")

""" get list of all stocks currently traded
    on NASDAQ exchange """
nasdaq_ticker_list = tickers_nasdaq()

""" get list of all stocks currently in the S&P 500 """
sp500_ticker_list = tickers_sp500()

""" get other tickers not in NASDAQ (based off nasdaq.com)"""
other_tickers = tickers_other()


```
