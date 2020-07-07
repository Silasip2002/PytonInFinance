import talib as ta

#Indicator library

class Indicator:

    def __init__(self,price):
        self.price = price;

    def getIndicator(self,name):
        if name == 'MACD':
             input = self.getMACD()
        elif name == 'RSI':
             input = self.getRSI()
        elif name == "KDJ":
             input = self.getKDJ()
        return input

    def getMACD(self):
        return ta.MACD(self.price['Adj Close'], fastperiod=6, slowperiod=12, signalperiod=9)[1]

    def getRSI(self):
        return ta.RSI(self.price['Adj Close'], timeperiod=9) / 100

    def getKDJ(self):
        return ta.STOCH(self.price['High'], self.price['Low'],self.price['Adj Close'], fastk_period=5, slowk_period=3, slowk_matype=0, slowd_period=3, slowd_matype=0)[1]



