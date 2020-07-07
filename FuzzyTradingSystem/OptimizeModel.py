## Optimiz model:
from FuzzyTradingSystem.Stock import Stock
from FuzzyTradingSystem.FuzzyModel import OurFuzzy
from FuzzyTradingSystem.BackTestModel import BackTest
from FuzzyTradingSystem.Indicator import Indicator
import pandas as pd
from FuzzyTradingSystem.TraditionalTrading import TraditionalTrading as tt
import numpy as np
import datetime

# 1.The user can enter the base information
pd.set_option('display.max_rows', None)

date_InputTimeS = datetime.datetime.strptime("2020-01-01", '%Y-%m-%d')

date_InputTimeE = datetime.datetime.strptime('2020-03-30', '%Y-%m-%d')

price = Stock.GetStockDataApi('FB',date_InputTimeS,date_InputTimeE)

indicators = Indicator(price)
firstInput = indicators.getIndicator("RSI")
secondInput = indicators.getIndicator("RSI")
thirdInput = indicators.getIndicator("RSI")


traditional = tt(price)
ttSignal = traditional.signal("RSI","RSI","RSI")
#print(type(ttSignal))
#print("test the ttSignal ", ttSignal)

profit_list = [[0 for x in range(11)] for y in range(11)]
gposition_list = [[0 for x in range(11)] for y in range(11)]

for gpostion in range (0,11):
    for sigma in range (0,11):
        ourFuzzy = OurFuzzy(gpostion/10,sigma/10)
        fuzzyOutSerics = pd.Series()
        fuzzySignal = pd.Series()

        for i in range(0, firstInput.size):
            fuzzyOutPut = OurFuzzy.fuzzyOut(ourFuzzy, firstInput[i], secondInput[i], thirdInput[i])
            fuzzyOutSerics = fuzzyOutSerics.set_value(i, fuzzyOutPut)

        fuzzyOutSerics = fuzzyOutSerics.set_value(i, fuzzyOutPut)

        for index, value in fuzzyOutSerics.iteritems():
            if (value <= 0.4):
                fuzzySignal = fuzzySignal.set_value(index, 1)
            elif (value >= 0.6):
                fuzzySignal = fuzzySignal.set_value(index, -1)
            else:
                fuzzySignal = fuzzySignal.set_value(index, 0)

        backTest = BackTest()
        print ('gpostion' , gpostion , 'sigma' , sigma)
        profit_list[gpostion][sigma] = backTest.getBTresult(price, fuzzySignal,ttSignal)
        #print(profit_list[gpostion][sigma])

max = np.amax(profit_list)
print(max)

