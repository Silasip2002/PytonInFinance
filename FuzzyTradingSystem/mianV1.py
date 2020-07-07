from FuzzyTradingSystem.Stock import Stock
from FuzzyTradingSystem.FuzzyModel import OurFuzzy
from FuzzyTradingSystem.BackTestModel import BackTest
from FuzzyTradingSystem.Indicator import Indicator
from FuzzyTradingSystem.TraditionalTrading import TraditionalTrading as tt
import pandas as pd
import datetime

# 1.The user can enter the base information
pd.set_option('display.max_rows', None)

date_InputTimeS = datetime.datetime.strptime("2020-01-01", '%Y-%m-%d')

date_InputTimeE = datetime.datetime.strptime('2020-03-30', '%Y-%m-%d')

price = Stock.GetStockDataApi("FB",date_InputTimeS,date_InputTimeE)

print(price)

# traidtional indicators setting
traditional = tt(price)
ttSignal = traditional.signal("RSI","RSI","RSI")
print("test the ttSignal ", ttSignal)


# fuzzy indicators setting
indicators = Indicator(price)
firstInput = indicators.getIndicator("RSI")
secondInput = indicators.getIndicator("RSI")
thirdInput = indicators.getIndicator("RSI")

ourFuzzy = OurFuzzy()
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
backTestResult = backTest.getBTresult(price,fuzzySignal,ttSignal)
#print('BackTest Result ', type(backTestResult))


