#!/usr/bin/env python
# coding: utf-8

# In[1]:


import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


class SMABacktester():
    def __init__(self, symbol, SMA_S, SMA_L, start, end):
        self.symbol = symbol
        self.SMA_S = SMA_S  # Corrected here
        self.SMA_L = SMA_L  # Corrected here
        self.start = start
        self.end = end
        self.results = None
        self.get_data()
        
    def get_data(self):  # Added self parameter
        df = yf.download(self.symbol, start=self.start, end=self.end)
        data = df.Close.to_frame()
        data["returns"] = np.log(data.Close.div(data.Close.shift(1)))
        data["SMA_S"] = data.Close.rolling(self.SMA_S).mean()
        data["SMA_L"] = data.Close.rolling(self.SMA_L).mean()
        data.dropna(inplace=True)
        self.data2 = data
    
    def test_results(self):
        data = self.data2.copy().dropna()  # Corrected here
        data["position"] = np.where(data["SMA_S"] > data["SMA_L"], 1, -1)
        data["strategy"] = data["returns"] * data.position.shift(1)
        data.dropna(inplace=True)
        data["returnsbh"] = data["returns"].cumsum().apply(np.exp)
        data["strategyresults"] = data["strategy"].cumsum().apply(np.exp)  # Corrected here
        perf = data["strategyresults"].iloc[-1]  # Corrected here
        outperf = perf - data["returnsbh"].iloc[-1]
        self.results = data
        return round(perf, 6), round(outperf, 6)
        
    def plot_results(self):
        if self.results is None:
            print("Run the test please")
        else:
            title_str = "{} | SMA_S = {} SMA_L = {}".format(self.symbol, self.SMA_S, self.SMA_L)
            self.results[["returnsbh", "strategyresults"]].plot(title=title_str, figsize=(12, 8))  # Corrected here


# In[4]:


class MomentBacktester():
    def __init__(self, symbol, momentum_period, start, end):
        self.symbol = symbol
        self.momentum_period = momentum_period
        self.start = start
        self.end = end
        self.results = None
        self.get_data()
        
    def get_data(self):
        df = yf.download(self.symbol, start=self.start, end=self.end)
        data = df.Close.to_frame()
        data["returns"] = np.log(data.Close.div(data.Close.shift(1)))
        data["momentum"] = data.Close.pct_change(self.momentum_period)
        data.dropna(inplace=True)
        self.data2 = data
    
    def test_results(self):
        data = self.data2.copy().dropna()
        data["position"] = np.where(data["momentum"] > 0, 1, -1)
        data["strategy"] = data["returns"] * data.position.shift(1)
        data.dropna(inplace=True)
        data["returnsbh"] = data["returns"].cumsum().apply(np.exp)
        data["strategyresults"] = data["strategy"].cumsum().apply(np.exp)
        perf = data["strategyresults"].iloc[-1]
        outperf = perf - data["returnsbh"].iloc[-1]
        self.results = data
        return round(perf, 6), round(outperf, 6)
        
    def plot_results(self):
        if self.results is None:
            print("Run the test please")
        else:
            title_str = "{} | Momentum Period = {}".format(self.symbol, self.momentum_period)
            self.results[["returnsbh", "strategyresults"]].plot(title=title_str, figsize=(12, 8))


# In[ ]:




