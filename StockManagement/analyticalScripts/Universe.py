from Portfolio import Portfolio
from pullEndogenInvestments import EndogenAccountDataPull

class Universe:

    def __init__(self):
        self.allStockData = {}

    def setUpPortfolio(self):
        self.portfolioHoldings = EndogenAccountDataPull() # TODO build in optionality to choose latest or specific date
        print(self.portfolioHoldings )
        PortfolioInstance = Portfolio(self.portfolioHoldings)
        PortfolioInstance.buildPortfolio()
        #savePortfolioInstance(portfolioInstance)
        self.PortfolioInstance = portfolioInstance
