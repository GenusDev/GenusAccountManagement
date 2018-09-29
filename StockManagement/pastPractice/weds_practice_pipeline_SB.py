import math
import talib
import numpy as np
from scipy import stats
import statsmodels.tsa.stattools as ts

from quantopian.pipeline import Pipeline
from quantopian.pipeline.data.morningstar import earnings_ratios
import statsmodels.tsa.stattools as ts
from quantopian.algorithm import attach_pipeline, pipeline_output

##Initialize with pipeline_output
# define Universe
def initialize(context):
    # define Universe
    initUniverse(context)
    context.spy = sid(8554) # The SID 8554 refers to the S&P500 SPYDER fund.
    context.nvs = sid(21536)  # NOVARTIS
    context.nvda = sid(19725) #NVIDIA! 
    #define security number in portfolio. TODO: change, use for test purpose.
    context.num_sec = 3
    #Allocation for each stock
    context.lim_sector = math.floor(context.num_sec * max_alloc_sector)
    try:
        context.init = True
    except:
        # First initialization begins a dict for all sectors.
        context.init = False
        # dictionary of key: sector in portfolio and value: number of stocks
        context.number_sector = dict()
        #init at 0
        for stock in context.securities:
            sector = context.dict_sector[stock.symbol]
            context.number-sector[sector] = 0
        # Initialize at 0
        for stock in context.securities:
            sector = context.dict_secotr[stock.symbol]
            context.number_sector[sector] = 0
        #Initialize the Index
        context.index = dict()
        #First 12 months, activate init of size 100 TODO change later
        for stock in context.securities:
            context.index[stock] = []
            for i in range(12):
                context.index[stock].append(100)
            context.in_aggregate = True
            #Determine if action is required
            context.weekly_action = False
            context.monthly_action = False
        #TODO
## Activation action
#TODO
## Weekly action
#TODO

### Daily Action
pass

# Perform portfolio rebalance / portfolio maanagement.

## Stock Universe Define
def initUniverse(context):
    #to do: replace symbols with actual stocks in our portfolio for future modeling.
    context.securities = symbols('SPY')
