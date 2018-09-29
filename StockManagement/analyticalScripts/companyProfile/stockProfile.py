class stockProfile(CompanyWikiProfile):

    #possibly integrate a twitter profile, and a finviz profile of key data

    def __init__(self, ticker):
        CompanyWikiProfile.__init__(self,ticker)
        self.ticker = ticker
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
        self.RecentData = self.pullData('recent')
        self.HistoricalData = self.pullData('historic') #load from pickle if failed


    def showHistoricalData(self,data):  # move this to another function
        style.use('ggplot')
        df = data

        label = "4. close"
        volLabel = '5. volume'
        if "5. adjusted close" in list(df):
            label = "5. adjusted close"
            volLabel = '6. volume'


        df['100ma'] = df[label].rolling(window=100, min_periods=0).mean()

        data.index = pd.to_datetime(data.index)

        df_ohlc = df[label].resample('10D').ohlc()
        df_volume = df[volLabel].resample('10D').sum()
        df_ohlc = df_ohlc.reset_index()
        df_ohlc['date'] = df_ohlc['date'].map(mdates.date2num)

        ax1 = plt.subplot2grid((6,1), (0,0), rowspan=5, colspan=1)
        ax2 = plt.subplot2grid((6,1), (5,0), rowspan=1, colspan=1, sharex=ax1)
        ax1.plot(df.index, df[label])
        ax1.plot(df.index, df['100ma'])
        ax2.bar(df.index, df[volLabel])
        ax1.xaxis_date()
        candlestick_ohlc(ax1, df_ohlc.values, width=2, colorup='g')
        ax2.fill_between(df_volume.index.map(mdates.date2num), df_volume.values, 0)
        plt.show()


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
            self.RecentStats = _findStats(data)
            #self.showHistoricalData(data)
            self.zScore = (self.CurrentPrice - self.RecentStats['mean'] )/self.RecentStats['std']
            return data

        def pullHistoricalData(self):
            data, meta_data = ts.get_weekly_adjusted(symbol=symbol)
            self.HistoricalStats = _findStats(data)

            return data

        def _findStats(data):
            df = data
            label = "4. close"
            if "5. adjusted close" in list(df):
                label = "5. adjusted close"

            std = np.std(df[label])
            max = np.max(data[label])
            min = np.min(data[label])
            mean = np.mean(df[label])
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


    
