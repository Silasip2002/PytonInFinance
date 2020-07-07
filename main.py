
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.gridspec as gridspec
import mpl_finance as mpf #import matplotlib.finance as mpf
import pandas as pd
import datetime
import talib
import tushare as ts


#******************* step 0 initalnization *********************
#download a stock price
df_stockload = ts.get_hist_data('002547',start='2019-01-01',end=datetime.datetime.now().strftime('%Y-%m-%d'))
df_stockload.sort_index(ascending=True,inplace=True)
plt.rcParams['axes.unicode_minus'] = False

#create a fig object
fig = plt.figure(figsize=(10,8),dpi=100,facecolor='white')
#subplot setting.
gs = gridspec.GridSpec(5,1,hspace=0,height_ratios=[3.5,1,1,1,1])
# allocate indicators position 將Dslop放入grid入面
graph_KAV = fig.add_subplot(gs[0,:]) #將個棒形圖放入個row「0」既index度
graph_VOL = fig.add_subplot(gs[1,:]) #將個vlaue放係row 1既index度
graph_MACD = fig.add_subplot(gs[2,:])
graph_KDJ = fig.add_subplot(gs[3,:])
graph_backTest = fig.add_subplot(gs[4,:])


#******************* step 1 create a stock price candel *********************
#開始設計個suplot既內容
mpf.candlestick2_ochl(graph_KAV,df_stockload.open, df_stockload.close, df_stockload.high, df_stockload.low, width=0.5, colorup='r', colordown='g')
graph_KAV.set_title(u"Stock Name")
graph_KAV.set_xlabel("Date")
graph_KAV.set_ylabel('Price')
graph_KAV.set_xlim(0,len(df_stockload.index))
graph_KAV.set_xticks(range(0,len(df_stockload.index),len(df_stockload.index)))
graph_KAV.grid(True,color='k')

'''for label in graph_KAV.xaxis.get_ticklabels():
    label.set_rotation(45)
    label.set_fontsize(10)'''
#*********************** step 2 create indicators in window *******************
# create a average moving line
#create a data in data frame
df_stockload['ma30']  = df_stockload.close.rolling(window=30).mean() #增加左column係個stock入面
df_stockload['ma60'] = df_stockload.close.rolling(window = 60).mean()
xaxis_range  = np.arange(0,len(df_stockload.index))
#graph_KAV.plot()
graph_KAV.plot(xaxis_range,df_stockload['ma30'],'black',label='M30')
graph_KAV.plot(xaxis_range,df_stockload['ma60'],'green',label='M60')
graph_KAV.legend(loc='best')

#********************* STEP 3 CREATE VOLUMN  *****************************

graph_VOL.bar(xaxis_range,df_stockload['volume'],color=['g' if df_stockload.open[x] > df_stockload.close[x] else 'r' for x in range(0,len(df_stockload.index))])
graph_VOL.set_ylabel('Volume')
graph_VOL.set_xlabel('Date')
graph_VOL.set_xlim(0,len(df_stockload.index))
graph_VOL.set_xticklabels(df_stockload.index)
graph_VOL.set_xticks(range(0,len(df_stockload.index)))

'''for label in graph_KAV.xaxis.get_ticklabels(): #因為個hspaec係零所以本第都睇唔到，所以hide左佢都冇所謂
    label.set_visible(False)

for label in graph_VOL.xaxis.get_ticklabels():
     label.set_rotation(45)
     label.set_fontsize(10)'''

#********************* STEP 4 CREATE MACD  *****************************
macd_dif,macd_dea,macd_bar = talib.MACD(df_stockload['close'].values,fastperiod=12,slowperiod=26,signalperiod=9)
graph_MACD.plot(xaxis_range,macd_dif,'red',label='macd dif') #當用plot時就只係晝左D線出黎。
graph_MACD.plot(xaxis_range,macd_dea,'blue',label='macd dea')

bar_red = np.where(macd_bar > 0, 2*macd_bar,0)
bar_green = np.where(macd_bar <0 , 2*macd_bar,0)
graph_MACD.bar(xaxis_range,bar_red,facecolor='red')
graph_MACD.bar(xaxis_range,bar_green,facecolor='green')
graph_MACD.legend(loc='best',shadow=True,fontsize='10')
graph_MACD.set_ylabel('MACD')
graph_MACD.set_xlabel('Date')
graph_MACD.set_xlim(0,len(df_stockload.index))
graph_MACD.set_xticks(range(0,len(df_stockload.index),10))
'''
graph_MACD.set_xticklabels([df_stockload.index[index] for index in graph_MACD.get_xticks()])


for label in graph_VOL.xaxis.get_ticklabels():
    label.set_visible(False)

for label in graph_MACD.xaxis.get_ticklabels():
        label.set_rotation(45)
        label.set_fontsize(10)
'''
#********************* STEP 5 CREATE KDJ  *****************************
xd = 9-1

date = df_stockload.index.to_series()

RSV = pd.Series(np.zeros(len(date)-xd),index=date.index[xd:])

Kvalue = pd.Series(0.0,index=RSV.index)

Dvalue = pd.Series(0.0,index=RSV.index)

Kvalue[0],Dvalue[0] = 50,50

for day_ind in range(xd, len(df_stockload.index)):

    RSV[date[day_ind]] = (df_stockload.close[day_ind] - df_stockload.low[day_ind-xd:day_ind+1].min())/(df_stockload.high[day_ind-xd:day_ind+1].max()-df_stockload.low[day_ind-xd:day_ind+1].min())*100

    if day_ind > xd:

        index = day_ind-xd

        Kvalue[index] = 2.0/3*Kvalue[index-1]+RSV[date[day_ind]]/3

        Dvalue[index] = 2.0/3*Dvalue[index-1]+Kvalue[index]/3

df_stockload['RSV'] = RSV

df_stockload['K'] = Kvalue

df_stockload['D'] = Dvalue

df_stockload['J'] = 3*Kvalue-2*Dvalue

graph_KDJ.plot(np.arange(0, len(df_stockload.index)), df_stockload['K'], 'blue', label='K')

graph_KDJ.plot(np.arange(0, len(df_stockload.index)), df_stockload['D'], 'g--', label='D')

graph_KDJ.plot(np.arange(0, len(df_stockload.index)), df_stockload['J'], 'r-', label='J')

graph_KDJ.legend(loc='best',shadow=True, fontsize ='10')


graph_KDJ.set_ylabel('KDJ')
graph_KDJ.set_xlabel('Date')
#graph_KDJ.set_xlim(0,len(df_stockload.index))
graph_KDJ.set_xticks(range(0,len(df_stockload.index),10)) #利用range去set左個tick

graph_KDJ.set_xticklabels([df_stockload.index[index] for index in graph_KDJ.get_xticks()])


for label in graph_MACD.xaxis.get_ticklabels():
    label.set_visible(False)

for label in graph_KDJ.xaxis.get_ticklabels():
        label.set_rotation(45)
        label.set_fontsize(10)

plt.show()




