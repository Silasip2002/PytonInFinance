
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.gridspec as gridspec
import mpl_finance as mpf #import matplotlib.finance as mpf
import pandas as pd
import datetime
import talib
import tushare as ts
import pandas_datareader.data as web


class QuantAverBreak():
    def __init__(self):
        self.skip_days = 0
        self.cash_hold = 100000  # 初始资金
        self.posit_num = 0  # 持股数目
        self.market_total = 0  # 持股市值
        self.profit_curve = []
        self.df_stockload = stock

    def run_factor_plot(self, mode):
        # trade rule setting
        if mode == "kdj":
            # --------------------------60MA break out strategy-------------------------
            self.df_stockload['Ma60'] = self.df_stockload.Close.rolling(window=60).mean()  #
            list_diff = np.sign(self.df_stockload.Close - self.df_stockload.Ma60)  # 如果個close price升穿60就會大過1
            self.df_stockload['Signal'] = np.sign(list_diff - list_diff.shift(1))  # 將依家既difference同之前前一日既比較睇下有冇穿過，從而去決定買定唔買。
        elif mode == "macd":
            # ------------------------- MACD trategy------------------------------------
            macd_dif, macd_dea, macd_bar = talib.MACD(self.df_stockload['Close'].values, fastperiod=12, slowperiod=26,signalperiod=9)
            list_diff = np.sign(macd_dif - macd_dea)
            shift_differt = np.roll(list_diff, 1, axis=None) #previous point
            self.df_stockload['Signal'] = np.sign(list_diff - shift_differt)  # if the value > 10 then return 1, else return 0
           # print("Debug=>macd making decision:",self.df_stockload['Signal'])
        elif mode == 'rsi':
             rsi1 = talib.RSI(self.df_stockload['Close'].values, timeperiod=9)
             rsi2 = talib.RSI(self.df_stockload['Close'].values, timeperiod=14)
             rsi3 = talib.RSI(self.df_stockload['Close'].values, timeperiod=21)

        else:
            print("The indicator mode is invalid. ")
            return 0;

        # the trading conditions
        for kl_index, today in self.df_stockload.iterrows():  # check返每一日既data
            if today.Signal > 0  :  # IF個Signal係大過0咁就係買入
                start = self.df_stockload.index.get_loc(kl_index)  # 拎住個日搵得返個買入時間
                self.skip_days = -1  # 睇下佢有冇貨係手，以免有貨係手仲不斷買入
                self.posit_num = int(self.cash_hold / today.Close)  # 計下曬所有錢可以買到幾多貨
                self.cash_hold = 0  # 買曬貨所以係零
            elif today.Signal < 0:  # IF個sinal係細過零，咁就會sell
                if self.skip_days == -1:  # -1姐係有貨係手，所以可以賣
                    end = self.df_stockload.index.get_loc(kl_index)  # 拎住個人既index去搵返賣既data
                    self.skip_days = 0  # 將個skip-day轉返0 因為已經賣左D貨。
                    self.cash_hold = int(self.posit_num * today.Close)
                    self.market_total = 0
                    if self.df_stockload.Close[end] < self.df_stockload.Close[start]:  # 如果最近個收盤價低過之前買入既收盤價，咁姐係輸錢。
                        plt.fill_between(self.df_stockload.index[start:end], 0, self.df_stockload.Close[start:end], color='green',
                                         alpha=0.38)
                        is_win = False
                    else:  # earn money shows red color
                        plt.fill_between(self.df_stockload.index[start:end], 0, self.df_stockload.Close[start:end], color='red',
                                         alpha=0.38)
                        is_win = True
            if self.skip_days == -1:  # 如果佢賣左D貨
                self.market_total = int(self.posit_num * today.Close)  # 就將依家個價同數量乘埋
                self.profit_curve.append(self.market_total)  # 之後就將D錢返入去個curve度
            else:
                self.profit_curve.append(self.cash_hold)  # 如果冇賣就保持咁多錢。

        #print("Debug => it is the user profit:",self.profit_curve)
        return self.profit_curve

    def showGraph(self,userProfit,stock_name):
        # ******************* step 0 initalnization *********************
        # download a stock price
        #self.df_stockload = ts.get_hist_data('002547', start='2019-01-01', end=datetime.datetime.now().strftime('%Y-%m-%d'))
        #self.df_stockload.sort_index(ascending=True, inplace=True)
        #plt.rcParams['axes.unicode_minus'] = False

        # create a fig object
        fig = plt.figure(figsize=(12, 10), dpi=100, facecolor='white')
        # subplot setting.
        gs = gridspec.GridSpec(5, 1, hspace=0, height_ratios=[3.5, 1, 1, 1, 2])
        # allocate indicators position 將Dslop放入grid入面
        graph_KAV = fig.add_subplot(gs[0, :])  # 將個棒形圖放入個row「0」既index度
        graph_VOL = fig.add_subplot(gs[1, :])  # 將個vlaue放係row 1既index度
        graph_MACD = fig.add_subplot(gs[2, :])
        graph_KDJ = fig.add_subplot(gs[3, :])
        graph_profit = fig.add_subplot(gs[4, :])

        # ******************* step 1 create a stock price candel *********************
        # 開始設計個suplot既內容
        print('Dubug = > df_stockload head /n: ', self.df_stockload.head())
        mpf.candlestick2_ochl(graph_KAV, self.df_stockload.Open, self.df_stockload.Close, self.df_stockload.High, self.df_stockload.Low,
                              width=0.5, colorup='r', colordown='g')

        graph_KAV.set_title(stock_name) # show the name of stock in the graph
        graph_KAV.set_xlabel("Date")
        graph_KAV.set_ylabel('Price')
        graph_KAV.set_xlim(0, len(self.df_stockload.index))
        graph_KAV.set_xticks(range(0, len(self.df_stockload.index), len(self.df_stockload.index)))
        graph_KAV.grid(True, color='k')

        '''for label in graph_KAV.xaxis.get_ticklabels():
            label.set_rotation(45)
            label.set_fontsize(10)'''
        # *********************** step 2 create indicators in window *******************
        # create a average moving line
        # create a data in data frame
        #self.df_stockload['Ma30'] = self.df_stockload.Close.rolling(window=30).mean()  # 增加左column係個stock入面
        self.df_stockload['ma60'] = self.df_stockload.Close.rolling(window=60).mean()
        xaxis_range = np.arange(0, len(self.df_stockload.index))
        # graph_KAV.plot()
        #graph_KAV.plot(xaxis_range, self.df_stockload['ma30'], 'black', label='M30')
        graph_KAV.plot(xaxis_range, self.df_stockload['ma60'], 'green', label='M60')
        graph_KAV.legend(loc='best')

        # ********************* STEP 3 CREATE VOLUMN  *****************************

        graph_VOL.bar(xaxis_range, self.df_stockload['Volume'],
                      color=['g' if self.df_stockload.Open[x] > self.df_stockload.Close[x] else 'r' for x in
                             range(0, len(self.df_stockload.index))])
        graph_VOL.set_ylabel('Volume')
        graph_VOL.set_xlabel('Date')
        graph_VOL.set_xlim(0, len(self.df_stockload.index))
        graph_VOL.set_xticklabels(self.df_stockload.index)
        graph_VOL.set_xticks(range(0, len(self.df_stockload.index)))

        for label in graph_KAV.xaxis.get_ticklabels(): #因為個hspaec係零所以本第都睇唔到，所以hide左佢都冇所謂
            label.set_visible(False)

        for label in graph_VOL.xaxis.get_ticklabels():
             label.set_rotation(45)
             label.set_fontsize(10)

        # ********************* STEP 4 CREATE MACD  *****************************
        macd_dif, macd_dea, macd_bar = talib.MACD(self.df_stockload['Close'].values, fastperiod=12, slowperiod=26,
                                                  signalperiod=9)
        graph_MACD.plot(xaxis_range, macd_dif, 'red', label='macd dif')  # 當用plot時就只係晝左D線出黎。
        graph_MACD.plot(xaxis_range, macd_dea, 'blue', label='macd dea')

        bar_red = np.where(macd_bar > 0, 2 * macd_bar, 0)
        bar_green = np.where(macd_bar < 0, 2 * macd_bar, 0)
        graph_MACD.bar(xaxis_range, bar_red, facecolor='red')
        graph_MACD.bar(xaxis_range, bar_green, facecolor='green')
        graph_MACD.legend(loc='best', shadow=True, fontsize='10')
        graph_MACD.set_ylabel('MACD')
        graph_MACD.set_xlabel('Date')
        graph_MACD.set_xlim(0, len(self.df_stockload.index))
        graph_MACD.set_xticks(range(0, len(self.df_stockload.index), 10))

        graph_MACD.set_xticklabels([self.df_stockload.index[index] for index in graph_MACD.get_xticks()])


        for label in graph_VOL.xaxis.get_ticklabels():
            label.set_visible(False)

        for label in graph_MACD.xaxis.get_ticklabels():
                label.set_rotation(45)
                label.set_fontsize(10)


        # ********************* STEP 5 CREATE KDJ  *****************************
        xd = 9 - 1

        date = self.df_stockload.index.to_series()

        RSV = pd.Series(np.zeros(len(date) - xd), index=date.index[xd:])

        Kvalue = pd.Series(0.0, index=RSV.index)

        Dvalue = pd.Series(0.0, index=RSV.index)

        Kvalue[0], Dvalue[0] = 50, 50

        for day_ind in range(xd, len(self.df_stockload.index)):

            RSV[date[day_ind]] = (self.df_stockload.Close[day_ind] - self.df_stockload.Low[day_ind - xd:day_ind + 1].min()) / (
                    self.df_stockload.High[day_ind - xd:day_ind + 1].max() - self.df_stockload.Low[
                                                                            day_ind - xd:day_ind + 1].min()) * 100

            if day_ind > xd:
                index = day_ind - xd

                Kvalue[index] = 2.0 / 3 * Kvalue[index - 1] + RSV[date[day_ind]] / 3

                Dvalue[index] = 2.0 / 3 * Dvalue[index - 1] + Kvalue[index] / 3


        self.df_stockload['RSV'] = RSV

        self.df_stockload['K'] = Kvalue

        self.df_stockload['D'] = Dvalue

        self.df_stockload['J'] = 3 * Kvalue - 2 * Dvalue

        graph_KDJ.plot(np.arange(0, len(self.df_stockload.index)), self.df_stockload['K'], 'blue', label='K')

        graph_KDJ.plot(np.arange(0, len(self.df_stockload.index)), self.df_stockload['D'], 'g--', label='D')

        graph_KDJ.plot(np.arange(0, len(self.df_stockload.index)), self.df_stockload['J'], 'r-', label='J')

        graph_KDJ.legend(loc='best', shadow=True, fontsize='10')

        graph_KDJ.set_ylabel('KDJ')
        graph_KDJ.set_xlabel('Date')
        # graph_KDJ.set_xlim(0,len(df_stockload.index))
        graph_KDJ.set_xticks(range(0, len(self.df_stockload.index), 10))  # 利用range去set左個tick

        graph_KDJ.set_xticklabels([self.df_stockload.index[index] for index in graph_KDJ.get_xticks()])

        for label in graph_MACD.xaxis.get_ticklabels():
            label.set_visible(False)

        for label in graph_KDJ.xaxis.get_ticklabels():
            label.set_rotation(45)
            label.set_fontsize(10)

        lengthOfDF = self.df_stockload.count
        #print("the length of userprofit",len(userporfit))
        #print('the length of df_sotck DF',lengthOfDF )
        self.df_stockload['profit'] = userProfit

        graph_profit.plot(self.df_stockload['profit'])
        graph_profit.legend(loc='best')
        plt.show()



#...........star running ...........
StockName = "FB" #//user input stock name

StartTime = datetime.datetime(2017, 1, 1)
stock = web.DataReader(StockName, "yahoo", StartTime , datetime.date.today())
examp_trade = QuantAverBreak() #new the class object
QuantAverBreak.df_stockload = stock
userporfit = examp_trade.run_factor_plot("macd") #base on the stock information to output the user information and select a mode
examp_trade.showGraph(userporfit,StockName) #base on the user information then plot the graph.









