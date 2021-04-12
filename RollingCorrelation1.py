# -*- coding: utf-8 -*-
"""
Created on Wed Mar 31 11:32:27 2021

@author: Joris Dreesen
"""

import datetime
import pandas as pd
import numpy as np
from pandas_datareader import data as wb
import seaborn as sn
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.io as pio

#pd.options.plotting.backend = "plotly"
pio.renderers.default='browser'
start = '2000-01-01'
end = '2021-12-29'
#['CL=F','ES=F','^VIX','SPY','^TNX','NQ=F','GC=F']
#['XLK','XLY','XLV','XLF','XLI','XLP','XLU','XLB','XLE','XLC']
#['XLK','^TNX','^TYX','AAPL','MSFT']
tickers = ['SPY','BB','TLT']
period = 30
price_data = []
Compare = 'SPY'

for ticker in tickers:
    try:
        prices = wb.DataReader(ticker, start = start, end = end, data_source='yahoo')[['Adj Close']]
        price_data.append(prices.assign(ticker=ticker)[['ticker', 'Adj Close']])
    except:
        pass

names = pd.concat(price_data)
names.reset_index()
names

df = pd.concat(price_data)

pd.set_option('display.max_columns', 525)

df = df.reset_index()
df = df.set_index('Date')
table = df.pivot(columns='ticker')

table1 =table.sum(level=1,axis=1)
table1 = table1.pct_change()
#Correlation matrix for curiousity 
corrMatrix = table1.corr()
sn.heatmap(corrMatrix, annot=True)
plt.title("Correlation from "+str(start))
plt.show()

#Loop comes here
rollingcorrs=[]

for x in tickers:
    if x == Compare:
        pass
    else:
        CorVar1= Compare
        CorVar2 = x
        rollingcorr = pd.Series(table1[CorVar1].rolling(period).corr(table1[CorVar2]),name ='Correlation '+ str(CorVar1) + ' & '+str(CorVar2))
        rollingcorrs.append(rollingcorr)
        next
        
#Clean RollingCorss
CleanRollingCorrs = pd.concat(rollingcorrs, axis=1)
CleanRollingCorrs.reset_index()
CleanRollingCorrs=CleanRollingCorrs.dropna()

fig = px.line(CleanRollingCorrs)
fig.add_hline(y=0.0, line_dash="dot", fillcolor ='red')
fig.show()




