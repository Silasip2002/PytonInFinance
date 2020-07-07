import wx
import numpy as np
from matplotlib.figure import Figure
import matplotlib.dates as mdates
import mpl_finance as mpf
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
import matplotlib.gridspec as gridspec
from FuzzyTradingSystem.Indicator import Indicator


class MainPanel(wx.Panel): #stock price display the panel.
    def __init__(self,parent):
        wx.Panel.__init__(self,parent=parent, id=-1)

        self.figure = Figure()
        #gs = gridspec.GridSpec(1, 1, left=0., bottom=0.09, right=0.96, top=0.1, wspace=None, hspace=0.1)
        self.am = self.figure.add_subplot(111)
        #self.vol = self.figure.add_subplot(gs[1,:])
        #self.macd = self.figure.add_subplot(gs[2,:]
        #self.devol = self.figure.add_subplot(gs[3,:])

        self.FigureCanvas = FigureCanvas(self, -1, self.figure)
        self.TopBoxSizer = wx.BoxSizer(wx.VERTICAL)
        self.TopBoxSizer.Add(self.FigureCanvas,proportion = -1, border = 2,flag = wx.ALL | wx.EXPAND)
        self.SetSizer(self.TopBoxSizer)

    def draw_subgraph(self,stockData):
        #ohlc = list(zip(np.arange(0, len(stockData.index)), stockData.Open, stockData.Close, stockData.High, stockData.Low))
        #mpf.candlestick2_ochl(, ohlc, width=0.5, colorup='r', colordown='g')
        mpf.candlestick2_ochl(self.am, stockData.Open, stockData.Close, stockData.High, stockData.Low,width=0.5,colorup='g', colordown='r')

    def update_subgraph(self):
        self.FigureCanvas.draw()

    def clear_subgraph(self): # should clear the graph before drawing .
        self.am.clear()
        #self.vol.clear()
        #self.devol.clear()
        #self.macd.clear()
        # self.figure.set_canvas(self.FigureCanvas)
        # self.updatePlot()

    def xylabel_tick_lim(self, title, dates):

        self.am.set_ylabel('Price')
        self.am.set_xlabel('Date')
        self.am.set_title(title)
        dir(self.figure)

        major_tick = len(dates)
        self.am.set_xlim(0, major_tick)

        self.am.set_xticks(range(0, major_tick, 15))

        self.am.set_xticklabels([dates.strftime('%Y-%m-%d')[index] for index in self.am.get_xticks()])

        for label in self.am.xaxis.get_ticklabels():
            label.set_rotation(45)
            label.set_fontsize(8)

        self.am.grid(True,color='k')

class BackTestPanel(wx.Panel): # create the back test panel
    def __init__(self,parent):
        wx.Panel.__init__(self, parent=parent, id=-1)
        self.figure = Figure()

        gs = gridspec.GridSpec(2, 1, left=0.05, bottom=0.10, right=0.96, top=0.96, wspace=None, hspace=0.1,
                               height_ratios=[1,1])

        self.trdResult = self.figure.add_subplot(gs[0, :])
        self.fuzzyResult = self.figure.add_subplot(gs[1, :])
        self.trdResult.legend(['Traditional Profit'], loc='best')
        self.fuzzyResult.legend(['Fuzzy Profit'], loc='best')

        self.FigureCanvas = FigureCanvas(self, -1, self.figure)
        self.TopBoxSizer = wx.BoxSizer(wx.VERTICAL)
        self.TopBoxSizer.Add(self.FigureCanvas, proportion=1, border=1, flag=wx.ALL | wx.EXPAND)
        self.SetSizer(self.TopBoxSizer)

    def lable_tick_limt(self,title):
        self.trdResult.set_ylabel('$')
        self.fuzzyResult.set_ylabel('$')
        self.fuzzyResult.set_xlabel('Date')

    def update_subgraph(self):
        self.FigureCanvas.draw()

    def clear_subgraph(self):
        self.trdResult.clear()
        self.fuzzyResult.clear()

    def draw_subgraph(self, backTestResult):
        self.fuzzyResult.plot(backTestResult['fuzzy_profit'])
        self.trdResult.plot(backTestResult['traditional_profit'])

















