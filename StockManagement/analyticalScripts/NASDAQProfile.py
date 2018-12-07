import wikipedia
from bs4 import BeautifulSoup
import pandas as pd
import requests
import io



class NASDAQProfile:

    def __init__(self,companyName):
        pull latest pickle
        if pickle.Date < 1 month of now
            pull all data
        self.name = companyName
        self.wikiProfileInfo = self.searchAndFind(companyName).infoBoxData


    def PullDataSpecificToStock(self):


    def pullAllStockTickers(self):
        nasdaqTickersURL = 'https://www.nasdaq.com/screening/companies-by-name.aspx?letter=0&exchange=nyse&render=download'
        nyseTickersURL = 'https://www.nasdaq.com/screening/companies-by-name.aspx?letter=0&exchange=nasdaq&render=download'
        amexTickersURL = 'https://www.nasdaq.com/screening/companies-by-name.aspx?letter=0&exchange=amex&render=download'

        data = {}

        def pullStockTickers(URL):
            nyseTickersrespose = requests.get(URL).content
            nyseTickersData = pd.read_csv(io.StringIO(nyseTickersrespose.decode('utf-8')))
            return nyseTickersData

        nyseData = pullStockTickers(nyseTickersURL)
        nasdaqData = pullStockTickers(nasdaqTickersURL)
        amexData = pullStockTickers(amexTickersURL)
        verticalStack = pd.concat([nyseData, nasdaqData], axis=0)
        verticalStack = pd.concat([verticalStack, amexData], axis=0)
        verticalStackReindexed = verticalStack.reset_index(drop=True)
        verticalStackReindexed = verticalStackReindexed.set_index('Symbol')

        return verticalStackReindexed



# Merge Dataframes
# Convert data early on into useful data
