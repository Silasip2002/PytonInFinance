import numpy as np
import talib as ta
import pandas as pd

class TraditionalTrading:

    def __init__(self,stock):
        self.stock = stock
        self.stock['rsi'] = ta.RSI(self.stock['Adj Close'], timeperiod=14)
        self.stock['macd'], self.stock['macdsignal'],self.stock['macdSlow'] = ta.MACD(self.stock['Adj Close'],
                                                                fastperiod=12, slowperiod=26,signalperiod=9)
        self.stock['k'], self.stock['d'] = ta.STOCH(self.stock['High'], self.stock['Low'], self.stock['Adj Close'],
                                        fastk_period=5,slowk_period=3, slowk_matype=0, slowd_period=3, slowd_matype=0)
        self.signalResult = pd.Series()

    def signal (self,input1,input2,input3):
        ttSignal = pd.DataFrame()
        inputsignal1  = self.selectIndicators(input1)
        inputsignal2 = self.selectIndicators(input2)
        inputsignal3 = self.selectIndicators(input3)

        for index in self.stock.index:
            if inputsignal1['input'].loc[index] == 1 and inputsignal2['input'].loc[index] == 1  and inputsignal3['input'].loc[index] == 1:
                ttSignal.loc[index, 'input'] = 1
            elif inputsignal1['input'].loc[index] == -1 and inputsignal2['input'].loc[index] == -1 and inputsignal3['input'].loc[index] == -1:
                ttSignal.loc[index, 'input'] = -1
            elif inputsignal1['input'].loc[index] == 0 and inputsignal2['input'].loc[index] == 0  and inputsignal3['input'].loc[index] == 0:
                ttSignal.loc[index, 'input'] = 0
            elif inputsignal1['input'].loc[index] == 1  and inputsignal2['input'].loc[index] == -1 and inputsignal3['input'].loc[index] == 1:
                ttSignal.loc[index, 'input'] = 0
            elif inputsignal1['input'].loc[index] == -1  and inputsignal2['input'].loc[index] == -1 and inputsignal3['input'].loc[index] == 1:
                ttSignal.loc[index, 'input'] = 0
            elif inputsignal1['input'].loc[index] == 1  and inputsignal2['input'].loc[index] == 1 and inputsignal3['input'].loc[index] == 0:
                ttSignal.loc[index, 'input'] = 0
            elif inputsignal1['input'].loc[index] == 1  and inputsignal2['input'].loc[index] == 1 and inputsignal3['input'].loc[index] == 0:
                ttSignal.loc[index, 'input'] = 1
            elif inputsignal1['input'].loc[index] == -1  and inputsignal2['input'].loc[index] == -1 and inputsignal3['input'].loc[index] == 0:
                ttSignal.loc[index, 'input'] = -1
            elif inputsignal1['input'].loc[index] == 1  and inputsignal2['input'].loc[index] == 1 and inputsignal3['input'].loc[index] == -1:
                ttSignal.loc[index, 'input'] = 0
            elif inputsignal1['input'].loc[index] == 1  and inputsignal2['input'].loc[index] == 0 and inputsignal3['input'].loc[index] == 1:
                ttSignal.loc[index, 'input'] = 1
            elif inputsignal1['input'].loc[index] == -1  and inputsignal2['input'].loc[index] == 0 and inputsignal3['input'].loc[index] == -1:
                ttSignal.loc[index, 'input'] = -1
            elif inputsignal1['input'].loc[index] == 0  and inputsignal2['input'].loc[index] == -1 and inputsignal3['input'].loc[index] == -1:
                ttSignal.loc[index, 'input'] = 0
            else:
                ttSignal.loc[index, 'input'] = 0
        return ttSignal

    def selectIndicators(self,input):
        signal = pd.DataFrame()
        if (input == 'MACD'):
            for index in self.stock.index:
                if self.stock['macd'].loc[index] - self.stock['macdsignal'].loc[index] > 0:
                    signal.loc[index, 'input'] = 1
                else:
                    signal.loc[index, 'input'] = -1
            return signal

        elif (input == 'RSI'):
            for index in self.stock.index:
                if self.stock['rsi'].loc[index] < 30:
                    signal.loc[index, 'input'] = 1
                elif self.stock['rsi'].loc[index] > 70:
                    signal.loc[index, 'input'] = -1
                else:
                    signal.loc[index, 'input'] = 0
            return signal

        elif (input == 'KDJ'):
            for index in self.stock.index:
                if self.stock['k'].loc[index]  < 30 and self.stock['d'].loc[index] < 30:
                    signal.loc[index, 'input'] = 1
                elif self.stock['k'].loc[index] > 70 and self.stock['d'].loc[index] > 70:
                    signal.loc[index, 'input'] = -1
                else:
                    signal.loc[index, 'input'] = 0
            return signal
















