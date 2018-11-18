import requests
import CompanyWikiProfile
from CompanyWikiProfile import CompanyWikiProfile

class stockProfile(CompanyWikiProfile):

    #possibly integrate a twitter profile, and a finviz profile of key data

    def __init__(self, ticker,QuantityHeld=5):

        ## create separate functions that tries to build profiles - create tests or comments when they fail.

        try:
            CompanyWikiProfile.__init__(self,self.name)
        except:
            try:
                self.name = self.get_symbol_name(ticker)
                CompanyWikiProfile.__init__(self,self.name)
            except:
                self.wikiProfileInfo = "no info found"

        self.ticker = ticker
        self.QuantityHeld = QuantityHeld

        self.SellPrice = "notSet"
        self.BuyPrice = "notSet"
        self.Stats = "notSet"
        self.RiskScore = "notSet"
        self.zScore = "notSet"
        self.ReturnScore = "notSet"

        self.CurrentStats = {}
        self.RecentStats = {}
        self.HistoricalStats = {}

        self.CurrentPrice = "notSet"
        self.CurrentData = self.pullData('current')
        time.sleep(10)
        #print(float(self.CurrentPrice) ,float(QuantityHeld))
        self.value = float(self.CurrentPrice) * float(QuantityHeld)
        print("value: ",self.value)

        self.RecentData = self.pullData('recent')

        time.sleep(10)

        self.HistoricalData = self.pullData('historic') #load from pickle if failed


    def showHistoricalData(self,data):  # move this to another class - data visualizations - include bounds

        closeLabel,volLabel = self.findTheRightLabels(data)

        style.use('ggplot')
        df = data

        df['100ma'] = df[closeLabel].rolling(window=100, min_periods=0).mean()

        data.index = pd.to_datetime(data.index)

        df_ohlc = df[closeLabel].resample('10D').ohlc()
        df_volume = df[volLabel].resample('10D').sum()
        df_ohlc = df_ohlc.reset_index()
        df_ohlc['date'] = df_ohlc['date'].map(mdates.date2num)

        ax1 = plt.subplot2grid((6,1), (0,0), rowspan=5, colspan=1)
        ax2 = plt.subplot2grid((6,1), (5,0), rowspan=1, colspan=1, sharex=ax1)
        ax1.plot(df.index, df[closeLabel])
        ax1.plot(df.index, df['100ma'])
        ax2.bar(df.index, df[volLabel])
        ax1.xaxis_date()
        candlestick_ohlc(ax1, df_ohlc.values, width=2, colorup='g')
        ax2.fill_between(df_volume.index.map(mdates.date2num), df_volume.values, 0)
        plt.show()

    def get_symbol_name(self,symbol):
        url = "http://d.yimg.com/autoc.finance.yahoo.com/autoc?query={}&region=1&lang=en".format(symbol)

        result = requests.get(url).json()

        for x in result['ResultSet']['Result']:
            if x['symbol'] == symbol:
                return x['name']


    def findTheRightLabels(self,tradingData):
        closeLabel = "4. close"
        volLabel = '5. volume'

        if "5. adjusted close" in list(tradingData):
            closeLabel = "5. adjusted close"
            volLabel = '6. volume'

        return closeLabel,volLabel


    def pullData(self,period):
        symbol = self.ticker
        API_KEY = "Z9MF1RI84UA8DQUP"
        symbol = self.ticker
        ts = TimeSeries(key=API_KEY, output_format='pandas', indexing_type='date')
        priceData = "null"


        def pullTodaysData(self):
            data, meta_data = ts.get_intraday(symbol=symbol,interval='15min', outputsize="full")
            self.CurrentStats = _findStats(data)
            self.CurrentPrice = self.CurrentStats["mean"]
            #self.showHistoricalData(data,"4. close")
            return data

        def pullLast4MonthsData(self):
            data, meta_data = ts.get_daily_adjusted(symbol=symbol, outputsize="compact")
            adjCloseName, volumeName = self.findTheRightLabels(data)
            self.Last4MonthsAdjustedClose = data[adjCloseName]
            self.Last4MonthsVolume = data[volumeName]

            self.RecentStats = _findStats(data)
            #self.showHistoricalData(data)
            self.zScore = (self.CurrentPrice - self.RecentStats['mean'] )/self.RecentStats['std']
            return data

        def pullHistoricalData(self):
            data, meta_data = ts.get_weekly_adjusted(symbol=symbol)
            adjCloseName, volumeName = self.findTheRightLabels(data)
            self.HistoricAdjustedClose = data[adjCloseName]
            self.HistoricVolume = data[volumeName]
            self.HistoricalStats = _findStats(data)

            return data


        def _findStats(data):
            df = data

            closeLabel,volLabel = self.findTheRightLabels(data)


            std = np.std(df[closeLabel])
            max = np.max(data[closeLabel])
            min = np.min(data[closeLabel])
            mean = np.mean(df[closeLabel])
            volititility = (std - mean)/mean
            stats = {
                "std" : std,
                "mean" : mean,
                "min" : min,
                "max" : max,
                "volitility" : volititility,
            }
            return stats

        if period == "current":
            priceData = pullTodaysData(self)
        elif period == "recent":
            priceData = pullLast4MonthsData(self)
        elif period == 'historic':
            priceData = pullHistoricalData(self)

        return priceData




    def findSellPrice(self):
        self.CurrentPrice
