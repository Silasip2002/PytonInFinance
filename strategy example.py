import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pandas_datareader.data as web
import datetime
import talib
import mpl_finance as mpf


class QuantAverBreak:
    def __init__(self):
        self.skip_days = 0
        self.cash_hold = 100000  # 初始资金
        self.posit_num = 0  # 持股数目
        self.market_total = 0  # 持股市值
        self.profit_curve = []

    def run_factor_plot(self, stock_df, mode):
        #trade rule setting
        if mode == 0 :
            # --------------------------60MA break out strategy-------------------------
            stock_df['Ma60'] = stock_df.Close.rolling(window=60).mean()  #
            list_diff = np.sign(stock_df.Close - stock_df.Ma20)
            print(type(list_diff))
            stock_df['signal'] = np.sign(list_diff - list_diff.shift(1))
        elif mode == 1:
             # ------------------------- MACD trategy------------------------------------
             macd_dif, macd_dea, macd_bar = talib.MACD(stock_df['Close'].values, fastperiod=12, slowperiod=26,signalperiod=9)
             list_diff = np.sign(macd_dif - macd_dea)
             shift_differt  =  np.roll(list_diff,1, axis=None)
             stock_df['signal'] = np.sign(list_diff - shift_differt)

        #show the candles
        fig = plt.figure(figsize=(25, 12), dpi=80, facecolor="white")
        candle  = fig.add_subplot(2, 1, 1)
        candle.set_title(u"00254")
        candle.set_xlabel("Date")
        candle.set_ylabel('Price')
        candle.set_xlim(0, len(stock_df.index))
        candle.set_xticks(range(0, len(stock_df.index), len(stock_df.index)))
        candle.grid(True, color='k')
        mpf.candlestick2_ochl(candle, stock_df.Open, stock_df.Close, stock_df.High, stock_df.Low, width=0.5, colorup='r',colordown='g')
        plt.show()

        # the trading conditions
        for kl_index, today in stock_df.iterrows():
            if today.signal > 0:  # Buy
                print("buy", kl_index)
                start = stock_df.index.get_loc(kl_index)
                self.skip_days = -1
                self.posit_num = int(self.cash_hold / today.Close)
                self.cash_hold = 0
            elif today.signal < 0:  # Sell
                if self.skip_days == -1: #make sure
                    print("sell", kl_index)
                    end = stock_df.index.get_loc(kl_index)
                    self.skip_days = 0
                    self.cash_hold = int(self.posit_num * today.Close)
                    self.market_total = 0
                    if stock_df.Close[end] < stock_df.Close[start]:  # if lose money then shows green color
                        plt.fill_between(stock_df.index[start:end], 0, stock_df.Close[start:end], color='green',
                                         alpha=0.38)
                        is_win = False
                    else:  # earn money shows red color
                        plt.fill_between(stock_df.index[start:end], 0, stock_df.Close[start:end], color='red', alpha=0.38)
                        is_win = True
            if self.skip_days == -1:
                self.market_total = int(self.posit_num * today.Close)
                self.profit_curve.append(self.market_total)
            else:
                self.profit_curve.append(self.cash_hold)
        profit = fig.add_subplot(2,1,2)
        stock_df['profit'] = self.profit_curve
        profit.plot( stock_df['profit'])
        profit.legend(loc='best')
        plt.subplots_adjust(left=0.09, bottom=0.20, right=0.94, top=0.95, wspace=0.2, hspace=0)


#...........star running ...........
StockName = "FB" #//enter the code of the tradying product.
StartTime = datetime.datetime(2017, 1, 1)
stock = web.DataReader(StockName, "yahoo", StartTime , datetime.date.today())
examp_trade = QuantAverBreak()
examp_trade.run_factor_plot(stock,1)