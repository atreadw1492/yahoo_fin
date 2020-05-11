# -*- coding: utf-8 -*-
"""
Created on Sat Jan 12 12:39:03 2019

@author: atrea
"""

import options

dates = options.get_expiration_dates("tgt")


info = {date : options.get_calls("tgt", date, True) for date in dates}


info = {date : options.get_options_chain("tgt", date, True) for date in dates}


d = options.get_options_chain("tgt", raw = True)

c = d["calls"]



def clean_percentage_field(series):
    
    """This is a helper function to clean the percentage-based fields in the
       options chain tables"""
    
    series = series.str.strip("%").str.strip("+").str.strip("-").str.strip()
    series = series.astype("float") / 100
    
    return series



    if not raw:
        calls["% Change"] = clean_percentage_field(calls["% Change"])
        puts["% Change"] = clean_percentage_field(puts["% Change"])
    
        calls["Implied Volatility"] = clean_percentage_field(calls["Implied Volatility"])
        puts["Implied Volatility"] = clean_percentage_field(puts["Implied Volatility"])
    
