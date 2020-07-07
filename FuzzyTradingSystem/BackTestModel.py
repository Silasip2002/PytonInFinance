import matplotlib.pyplot as plt
from FuzzyTradingSystem.userProfile import userProfile as uProfile


class BackTest:
    def __init__(self):
        plt.figure(figsize=(25, 12), dpi=80, facecolor="white")
        plt.subplot(2, 1, 1)
        self.trdAccount = uProfile()
        self.fuzzyAccount = uProfile()

    def getBTresult(self,stock_df,fuzzySignal,ttSignal):

        #get the trading signal between fuzzy and traditional
        stock_df['fuzzySignal']= fuzzySignal.values
        stock_df['ttSignal'] = ttSignal.values

        #print('Strating the fuzzy trading back test result')
        for kl_index, today in stock_df.iterrows():
            if (today.fuzzySignal > 0 and self.fuzzyAccount.get_skip_days() == 0):
                #print("Buy", kl_index)
                str_buyInfo = "Buy \n"
                self.fuzzyAccount.set_tradInformationList(str_buyInfo)
                start = stock_df.index.get_loc(kl_index)
                self.fuzzyAccount.set_skip_days(-1)
                self.fuzzyAccount.set_posit_num(int(self.fuzzyAccount.get_cash_hold() / today.Close))
                self.fuzzyAccount.set_buy_price ( int(self.fuzzyAccount.get_posit_num() * today.Close))  #get the buy cost
                self.fuzzyAccount.set_cash_hold(0)
            elif (self.fuzzyAccount.get_skip_days() == -1) :
                #print (" **the fuzzySignal is sell**")
                if  today.fuzzySignal < 0: #or ((self.fuzzyAccount.get_market_total() - self.fuzzyAccount.get_buy_price() ) / self.fuzzyAccount.get_buy_price() )* 100 > -5 :  #  the sell condition is -1 or the loss capital is more than 5 %
                   # print("Sell", kl_index)
                    str_sellInfo = "Sell \n"
                    self.fuzzyAccount.set_tradInformationList(str_sellInfo)
                    end = stock_df.index.get_loc(kl_index)
                    self.fuzzyAccount.set_skip_days(0)
                    self.fuzzyAccount.set_cash_hold(int(self.fuzzyAccount.get_posit_num() * today.Close) )
                    self.fuzzyAccount.set_market_total(0)
                    if stock_df.Close[end] < stock_df.Close[start]:
                        plt.fill_between(stock_df.index[start:end], 0, stock_df.Close[start:end], color='green',alpha=0.38)
                        is_win = False
                    else:
                        plt.fill_between(stock_df.index[start:end], 0, stock_df.Close[start:end], color='red',alpha=0.38)
                        is_win = True

            if self.fuzzyAccount.get_skip_days() == -1 : # if  we have stock then the profile will be the  market price
                self.fuzzyAccount.set_market_total( int(self.fuzzyAccount.get_posit_num() * today.Close))
                self.fuzzyAccount.set_profit_curve(self.fuzzyAccount.get_market_total())
            else:
                self.fuzzyAccount.set_profit_curve(self.fuzzyAccount.get_cash_hold()) # else the profit will be cash

       # print('Starting the traditional trading back test result ')
        for kl_index, today in stock_df.iterrows():
            if (today.ttSignal > 0 and self.trdAccount.get_skip_days() == 0):
               # print("Buy", kl_index)
                str_buyInfo = "Buy \n"
                self.trdAccount.set_tradInformationList(str_buyInfo)
                start = stock_df.index.get_loc(kl_index)
                self.trdAccount.set_skip_days(-1)
                self.trdAccount.set_posit_num(int(self.trdAccount.get_cash_hold() / today.Close))
                self.trdAccount.set_buy_price(int(self.fuzzyAccount.get_posit_num() * today.Close) ) # get the buy cost
                self.trdAccount.set_cash_hold(0)
            elif (self.trdAccount.get_skip_days() == -1):
               # print (" the buy stock cost ", self.trdAccount.get_buy_price())
                if today.ttSignal < 0: #or ((self.trdAccount.get_market_total() - self.trdAccount.get_buy_price()) / self.trdAccount.get_buy_price()) * 100 > -5:  # the sell condition is -1 or the loss capital is more than 5 %
                   # print("Sell", kl_index)
                    str_sellInfo = "Sell \n"
                    self.trdAccount.set_tradInformationList(str_sellInfo)
                    end = stock_df.index.get_loc(kl_index)
                    self.trdAccount.set_skip_days(0)
                    self.trdAccount.set_cash_hold(int(self.trdAccount.get_posit_num() * today.Close))
                    self.trdAccount.set_market_total(0)
                    if stock_df.Close[end] < stock_df.Close[start]:
                        plt.fill_between(stock_df.index[start:end], 0, stock_df.Close[start:end], color='green',
                                         alpha=0.38)
                        is_win = False
                    else:
                        plt.fill_between(stock_df.index[start:end], 0, stock_df.Close[start:end], color='red',
                                         alpha=0.38)
                        is_win = True

            if self.trdAccount.get_skip_days() == -1:  # if  we have stock the profile will be the  market price
                self.trdAccount.set_market_total(int(self.trdAccount.get_posit_num() * today.Close))
                self.trdAccount.set_profit_curve(self.trdAccount.get_market_total())
            else:
                self.trdAccount.set_profit_curve(self.trdAccount.get_cash_hold())  # else the profit will be cash



        stock_df['fuzzy_profit'] = self.fuzzyAccount.get_profit_curve()

        #print("fuzzy profit ",  stock_df['fuzzy_profit'] )
        stock_df['traditional_profit'] = self.trdAccount.get_profit_curve()

        #print("stock_df['traditional_profit'] ", stock_df['traditional_profit'])

        stockC =  (stock_df.iloc[len(stock_df) - 1].Close - stock_df.iloc[0].Close) / stock_df.iloc[0].Close * 100
        fuzzy_profitC = (stock_df['fuzzy_profit'][len(stock_df) - 1] - 100000) / 100000 * 100
        trd_profitC = (stock_df['traditional_profit'][len(stock_df) - 1] - 100000) / 100000 * 100

        stockChange = "Price: " + str('%.2f' %stockC  +"%"+ '\n')
        profitChange =  "Profit:"  + str('%.2f' %fuzzy_profitC  +'%'+ '\n')
        self.fuzzyAccount.set_tradInformationList(stockChange)
        self.fuzzyAccount.set_tradInformationList(profitChange)

        print("Stock Price: ", (stock_df.iloc[len(stock_df) - 1].Close - stock_df.iloc[0].Close) / stock_df.iloc[0].Close * 100, " % ")
        print("Fuzzy Profit: ", (stock_df['fuzzy_profit'][len(stock_df) - 1] - 100000) / 100000 * 100, " % ")
        print("Traditional Profit: ", (stock_df['traditional_profit'][len(stock_df) - 1] - 100000) / 100000 * 100, " % ")

        # get set the graph attribute
        plt.title("Stock Name")
        #plt.ylim(np.min(stock_df.Close) - 5, np.max(stock_df.Close) + 5)  # visualize the stock price

        p1 = plt.subplot(2, 1, 1)
        stock_df.fuzzy_profit.plot()
        plt.legend(['Fuzzy Profit'], loc='best')

        p2 = plt.subplot(2, 1, 2)
        stock_df.traditional_profit.plot()
        plt.legend(['Traditional Profit'], loc='best')

        plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0, hspace=0.25)
        plt.subplots_adjust(left=0.09, bottom=0.20, right=0.94, top=0.95, wspace=0.2, hspace=0)
        #plt.show()

        print  ("The fuzzy Profit : ", stock_df['fuzzy_profit'][len(stock_df) - 1] - 100000)
        #return (stock_df['fuzzy_profit'][len(stock_df) - 1] - 100000)
        return stock_df


    def getInfromationList(self):
        return self.fuzzyAccount.get_tradInformationList();


