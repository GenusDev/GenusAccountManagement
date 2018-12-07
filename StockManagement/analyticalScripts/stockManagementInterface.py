from pullEndogenInvestments import EndogenAccountDataPull
from CompanyWikiProfile import CompanyWikiProfile
from Universe import Universe

import pprint
import datetime as dt
import time
import matplotlib.pyplot as plt
from matplotlib import style
from matplotlib.finance import candlestick_ohlc
import matplotlib.dates as mdates
import numpy as np
import pandas as pd
import pandas_datareader.data as web
from alpha_vantage.timeseries import TimeSeries
import matplotlib.pyplot as plt
import sys
import json
import urllib.request
import pickle
import requests


def applyAnalysis(portfolio,whichAnalysis):

    if whichAnalysis == "example":
        doThisThing = "yeah"


def setUpPortfolio():

    ExistingPortfolio = EndogenAccountDataPull()








def Main(): #buildPortfolio

    def higherLogic():
        universeInstance = Universe()

        options = [
            "( b )uild Portfolio",
        ]

        choice = input("What do you want to do? :")

        if choice == "b":
            universeInstance.setUpPortfolio()


        portfolioTickersandHoldings = EndogenAccountDataPull()



        #set up universe




    higherLogic()



if __name__ == '__main__':
    Main()
