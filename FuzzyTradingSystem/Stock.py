import numpy as np
import pandas as pd
import pandas_datareader.data as web
import datetime
import csv,os
import codecs
import talib

class Stock:

    def GetStockDataApi(stockName=None,inputTimeS=None,inputTimeE=None):


        path = '/Users/silasip/PycharmProjects/PytonInFinance/FuzzyTradingSystem/Stock_History'

        str_InputTimeS =  inputTimeS.strftime('%Y-%m-%d')
        date_InputTimeS = datetime.datetime.strptime(str_InputTimeS,'%Y-%m-%d')
        str_IntPutTimeE = inputTimeE.strftime('%Y-%m-%d')
        date_InputTimeE = datetime.datetime.strptime(str_IntPutTimeE,'%Y-%m-%d')
        #print('GetStockDataApi', stockName)
        stockFileName = stockName + '+' + str_InputTimeS + '+' + str_IntPutTimeE + '.csv'
        #print(stockFileName)
        newFilePath = os.path.join(path,stockFileName)

        #print("Current:%s" % os.getcwd())  # current directory
        os.chdir(path)
        #print("After:%s" % os.getcwd())  # modified directory

        for filename in os.listdir(path): # assume there are file name already.
            if stockName in filename:
                if filename.count('+') == 2: #save the csv file
                    str_fileTimeS = filename.split('+')[1]
                    str_fileTimeE = filename.split('+')[2].split('.')[0]

                    #change the Date formate frome Str to Date
                    date_fileTimeS  = datetime.datetime.strptime(str_fileTimeS,'%Y-%m-%d')
                    date_fileTimeE = datetime.datetime.strptime(str_fileTimeE,'%Y-%m-%d')

                    if((date_fileTimeS - date_InputTimeS).days <= 0) and ((date_fileTimeE - date_InputTimeE).days >= 0): #the inputdate has already in the files then read the date directly.
                        stockData = pd.read_csv(os.path.join(path,filename),parse_dates=True,index_col=0)
                       # print(stockData.head(), stockData.tail())

                        stockData = stockData.loc[date_InputTimeS:date_InputTimeE] #select the data within the input peroid.
                        #print(stockData.head(),stockData.tail)
                    else: # if the input date is not included in the exiting data, then need to download.
                        print('else ', stockName)
                        stockData = web.DataReader(stockName,'yahoo',date_InputTimeS,date_InputTimeE)
                        os.rename(filename,newFilePath) # replace the old name with new file path name
                        stockData.to_csv(newFilePath,columns=stockData.columns,index=True) #replace the content in existing file.

                   # print(stockData.head(), stockData.tail())
                    return stockData
                else:
                    break

        stockData = web.DataReader(stockName,'yahoo',date_InputTimeS,date_InputTimeE)
        #print('stocData ' , stockData)
        stockData.to_csv(newFilePath,columns = stockData.columns,index=True)

        return stockData


    def GetStockDatPro(stockName=None, stockTimeS=None, stockTimeE=None):
        #print ('GetStockDatPro', stockName )
        stockPro = Stock.GetStockDataApi(stockName, stockTimeS, stockTimeE)
        #print('the stockPro data type : ' , type(stockPro))



        '''
        #stockPro['Ma20'] = pd.rolling_mean(stockPro.Close, window=20)
        #stockPro['Ma60'] = pd.rolling_mean(stockPro.Close, window=60)
        #stockPro['Ma120'] = pd.rolling_mean(stockPro.Close, window=120)
        stockPro['Ma20'] = stockPro.Close.rolling(12).mean()
        stockPro['Ma60'] = stockPro.Close.rolling(60).mean()
        stockPro['Ma120'] = stockPro.Close.rolling(120).mean()

        # MACD
       # stockPro['macd_dif'], stockPro['macd_dea'], stockPro['macd_bar'] = talib.MACD(stockPro['Close'].values,fastperiod=12, slowperiod=26,signalperiod=9)

        # KDJ
        
        xd = 9 - 1
        date = stockPro.index.to_series()
        RSV = pd.Series(np.zeros(len(date) - xd), index=date.index[xd:])
        Kvalue = pd.Series(0.0, index=RSV.index)
        Dvalue = pd.Series(0.0, index=RSV.index)
        Kvalue[0], Dvalue[0] = 50, 50

        for day_ind in range(xd, len(date)):
            RSV[date[day_ind]] = (stockPro.Close[day_ind] - stockPro.Low[day_ind - xd:day_ind + 1].min()) / (
                        stockPro.High[day_ind - xd:day_ind + 1].max() - stockPro.Low[
                                                                        day_ind - xd:day_ind + 1].min()) * 100
            if day_ind > xd:
                index = day_ind - xd
                Kvalue[index] = 2.0 / 3 * Kvalue[index - 1] + RSV[date[day_ind]] / 3
                Dvalue[index] = 2.0 / 3 * Dvalue[index - 1] + Kvalue[index] / 3
        stockPro['RSV'] = RSV
        stockPro['K'] = Kvalue
        stockPro['D'] = Dvalue
        stockPro['J'] = 3 * Kvalue - 2 * Dvalue
        '''
        return stockPro


