
class AnalyzedCompany(stockProfile):

    def __init__(self,ticker):
        stockProfile.__init__(self,ticker)
        CurrentPrice = self.CurrentPrice
        RecentStats = self.RecentStats
        HistoricalStats = self.HistoricalStats
        zScore = self.zScore

        RiskScore = "notset"
        ProfitabilityScore = "notset"
        SellPrice = "notset"
        BuyPrice = "notset"

    def identifyRiskScore():
        print(zScore)
        CurrentPrice - RecentStats['std']

    def identifyProfitabilityScore():
        print(zScore)
        CurrentPrice - RecentStats['std']

    def setSellPrice():
        SellPrice = CurrentPrice+(HistoricalStats['std']*-zScore)
        print(SellPrice)

    def setBuyPrice():
        BuyPrice = CurrentPrice-RecentStats['std']
        print(BuyPrice)
