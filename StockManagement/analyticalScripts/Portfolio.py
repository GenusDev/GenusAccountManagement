import stockProfile

class Portfolio:

    def __init__(self,TickerArray):
        self.TickerArray = TickerArray
        self.SharpRatio = "notSet"
        self.PortfolioArray = {}

    def buildPortfolio(self):
        for eachTickerName in self.TickerArray:
            print(eachTickerName);
            CompanyProfile = stockProfile(eachTickerName, self.TickerArray[eachTickerName] )
            self.PortfolioArray.update({eachTickerName:CompanyProfile})
            print(self.PortfolioArray)
            time.sleep(30)

    def getSharpRatio(self):
        return self.SharpRatio
