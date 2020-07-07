import wx
import wx.adv
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from FuzzyTradingSystem.MainPanel import MainPanel
from FuzzyTradingSystem.MainPanel import BackTestPanel
import datetime
from FuzzyTradingSystem.Stock import Stock
from FuzzyTradingSystem.TraditionalTrading import TraditionalTrading as tt
from FuzzyTradingSystem.Indicator import Indicator
from FuzzyTradingSystem.FuzzyModel import OurFuzzy
import numpy as np
import pandas as pd
from FuzzyTradingSystem.BackTestModel import BackTest

class Panel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent, id=-1)
        self.figure = Figure()
        self.am = self.figure.add_subplot(1,1,1)
        self.FigureCanvas = FigureCanvas(self, -1, self.figure)  #
        self.TopBoxSizer = wx.BoxSizer(wx.VERTICAL)
        self.TopBoxSizer.Add(self.FigureCanvas, proportion=-1, border=1, flag=wx.ALL | wx.EXPAND)
        self.SetSizer(self.TopBoxSizer)

class Frame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, parent=None, title='FUZZY LOGIC TRADING SYSTEM', size=(1000, 600),
                          style=wx.DEFAULT_FRAME_STYLE ^ wx.MAXIMIZE_BOX)
        #1.------------------------------------------------------------------------------------------
        self.DispPanel = MainPanel(self)
        self.BackPanel = BackTestPanel(self)

        self.am = self.DispPanel.am
       #self.vol = self.DispPanel.vol
       #self.devol = self.DispPanel.devol
       #self.macd = self.DispPanel.macd

        #2.------------------------------------------------------------------------------------------
        self.ParaPanel = wx.Panel(self, -1)
        vboxnetA = wx.BoxSizer(wx.VERTICAL)

        # 2.1 create box and sizer
        paraInput_Box = wx.StaticBox(self.ParaPanel, -1, style=2,name= "Parameter Input")
        paraInput_Sizer = wx.StaticBoxSizer(paraInput_Box, wx.VERTICAL)
        #2.1.1 set widgets
        stockCode_Text = wx.StaticText(self.ParaPanel, -1, 'Stock Name')
        self.stockSearch = wx.SearchCtrl(self.ParaPanel, -1, value="Search")
        self.stockName = self.stockSearch.GetValue() # set the default stock name
        if self.stockName == "":
            self.stockName = 'MCD'

        self.dpcEndTime = wx.adv.DatePickerCtrl(self.ParaPanel, -1, style=wx.adv.DP_DROPDOWN | wx.adv.DP_SHOWCENTURY | wx.adv.DP_ALLOWNONE)  # end time
        self.dpcStartTime = wx.adv.DatePickerCtrl(self.ParaPanel, -1,style=wx.adv.DP_DROPDOWN | wx.adv.DP_SHOWCENTURY | wx.adv.DP_ALLOWNONE)  # start time
        DateTimeNow = wx.DateTime.Now()  # the formate of the date
        self.dpcEndTime.SetValue(DateTimeNow)
        self.dpcStartTime.SetValue(DateTimeNow)
        stockData_Text = wx.StaticText(self.ParaPanel, -1, 'Date')

        dateVal = self.dpcStartTime.GetValue()
        self.stockSdate_Val = datetime.datetime(dateVal.year-1, dateVal.month+1, dateVal.day)
        dateVal = self.dpcEndTime.GetValue()
        self.stockEdate_Val = datetime.datetime(dateVal.year, dateVal.month+1, dateVal.day)

        #2.1.2 add into the sizer
        paraInput_Sizer.Add(stockCode_Text, proportion=0, flag=wx.EXPAND | wx.ALL, border=2)
        paraInput_Sizer.Add(self.stockSearch, 0, wx.EXPAND | wx.ALL | wx.CENTER, 2)
        paraInput_Sizer.Add(stockData_Text, proportion=0, flag=wx.EXPAND | wx.ALL, border=2)
        paraInput_Sizer.Add(self.dpcStartTime, 0, wx.EXPAND | wx.ALL | wx.CENTER, 2)
        paraInput_Sizer.Add(self.dpcEndTime, 0, wx.EXPAND | wx.ALL | wx.CENTER, 2)

        #2.2 create the box and sizer
        IndicatorBox = wx.StaticBox(self.ParaPanel, -1, 'Indicators')
        Indicators_Sizer = wx.StaticBoxSizer(IndicatorBox, wx.VERTICAL)
        #2.2.1 craetet the widget
        indicators_list = ['MACD', "RSI", "KDJ"]
        self.indicators_CMBO1 = wx.ComboBox(self.ParaPanel, -1, "MACD", choices = indicators_list, style = wx.CB_READONLY|wx.CB_DROPDOWN)
        self.indicators_CMBO2 = wx.ComboBox(self.ParaPanel, -1, "RSI", choices = indicators_list,  style = wx.CB_READONLY|wx.CB_DROPDOWN)
        self.indicators_CMBO3 = wx.ComboBox(self.ParaPanel, -1, "KDJ", choices = indicators_list,  style = wx.CB_READONLY|wx.CB_DROPDOWN)
        #2.2.2 add into the sizer
        Indicators_Sizer.Add(self.indicators_CMBO1,proportion=0,flag = wx.EXPAND|wx.ALL,border = 2)
        Indicators_Sizer.Add(self.indicators_CMBO2, proportion=0, flag=wx.EXPAND | wx.ALL, border=2)
        Indicators_Sizer.Add(self.indicators_CMBO3, proportion=0, flag=wx.EXPAND | wx.ALL, border=2)

        #2.4
        self.TextAInput = wx.TextCtrl(self.ParaPanel, -1, "Information : \n", style=wx.TE_MULTILINE | wx.TE_READONLY)  #


        #2.5. add widgest into the paramebter panel.

        vboxnetA.Add(paraInput_Sizer, proportion=0, flag=wx.EXPAND | wx.BOTTOM, border=2)
        vboxnetA.Add(Indicators_Sizer, proportion=0, flag=wx.EXPAND | wx.BOTTOM, border=2)
        vboxnetA.Add(self.TextAInput, proportion=1, flag=wx.EXPAND | wx.ALL, border=2)
        self.ParaPanel.SetSizer(vboxnetA)

        #3 Create right plane------------------------------------------------------------------------------------------
        self.CtrlPanel = wx.Panel(self, -1)
        self.FlexGridSizer = wx.FlexGridSizer(rows=2, cols=1, vgap=2, hgap=2)

        #3.1 craete the widgets Events
        self.Firmoffer = wx.Button(self.CtrlPanel, -1, "Real Time")
        self.Firmoffer.Bind(wx.EVT_BUTTON,self.FirmEvent)

       # self.Stockpick = wx.Button(self.CtrlPanel, -1, "Select Stock")

        self.Backtrace = wx.Button(self.CtrlPanel, -1, "Back Test")
        self.Backtrace.Bind(wx.EVT_BUTTON,self.BackPanelEvent)


        #3.2 add into the sizer
        self.FlexGridSizer.Add(self.Firmoffer, proportion=1, border=5, flag=wx.ALL | wx.EXPAND)
        #self.FlexGridSizer.Add(self.Stockpick, proportion=1, border=5, flag=wx.ALL | wx.EXPAND)
        self.FlexGridSizer.Add(self.Backtrace, proportion=1, border=5, flag=wx.ALL | wx.EXPAND)
        self.FlexGridSizer.SetFlexibleDirection(wx.BOTH)
        self.CtrlPanel.SetSizer(self.FlexGridSizer)

        #End add panels into the frame------------------------------------------------------------------------------------------.
        self.HBoxPanel = wx.BoxSizer(wx.HORIZONTAL)
        self.HBoxPanel.Add(self.ParaPanel, proportion=1, border=2, flag=wx.EXPAND | wx.ALL)
        self.HBoxPanel.Add(self.DispPanel, proportion=8, border=2, flag=wx.EXPAND | wx.ALL)
        self.HBoxPanel.Add(self.CtrlPanel, proportion=1, border=2, flag=wx.EXPAND | wx.ALL)
        self.SetSizer(self.HBoxPanel)

    # the real stock price page

    def FirmEvent(self, event):
        self.HBoxPanel.Hide(self.BackPanel) #hide the back test panel

        self.HBoxPanel.Replace(self.BackPanel, self.DispPanel)  # show the main panel

        self.HBoxPanel.Show(self.DispPanel)

       # self.HBoxPanel.Remove(self.BackPanel)

        self.SetSizer(self.HBoxPanel)

        self.HBoxPanel.Layout()

        # get the default stock information
        self.stockName = self.stockSearch.GetValue()

        #self.str_StartTime = self.dpcStartTime.GetValue()

        dateVal = self.dpcStartTime.GetValue()
        #print(dateVal)
        self.stockSdate_Val = datetime.datetime(dateVal.year , dateVal.month + 1, dateVal.day)
        dateVal = self.dpcEndTime.GetValue()
        #print(dateVal)
        self.stockEdate_Val = datetime.datetime(dateVal.year, dateVal.month + 1, dateVal.day)

        self.reFlashFrame()

    def reFlashFrame(self):
        self.DispPanel.clear_subgraph()  #
        self.ProcessStock()
        self.DispPanel.update_subgraph()  #

    def ProcessStock(self):
        #df_stockload = web.DataReader("600797.SS","yahoo", datetime.datetime(2017,1,1), datetime.date.today())


        df_stockload = Stock.GetStockDatPro(self.stockName, self.stockSdate_Val, self.stockEdate_Val)

        """ draw the AM"""
        # self.am.plot(self.numic[0:self.butNum],self.close[0:self.butNum],'#0f0ff0',linewidth=1.0)

        numic = np.arange(0, len(df_stockload.index))
        #butNum = len(df_stockload.index)
        self.DispPanel.xylabel_tick_lim(self.stockName, df_stockload.index)
        self.DispPanel.draw_subgraph(df_stockload)

    # the back test page

    def BackPanelEvent(self, event): #get panel information to stock for futher analysis .
        self.HBoxPanel.Hide(self.DispPanel)  # hide the back test panel

        self.HBoxPanel.Replace(self.DispPanel, self.BackPanel)  # show the main panel

        self.HBoxPanel.Show(self.BackPanel)

        #self.HBoxPanel.Remove(self.DispPanel)

        self.SetSizer(self.HBoxPanel)

        self.HBoxPanel.Layout()

        # Get stockName from UI
        self.stockName = self.stockSearch.GetValue()
        #Get data from UI
        dateVal = self.dpcStartTime.GetValue()
        self.stockSdate_Val = datetime.datetime(dateVal.year, dateVal.month + 1, dateVal.day)
        dateVal = self.dpcEndTime.GetValue()
        self.stockEdate_Val = datetime.datetime(dateVal.year, dateVal.month + 1, dateVal.day)
        #get indicator from UI

        self.reFlashBackPanel()

    def ProcessBackTest(self):

        price = Stock.GetStockDataApi(self.stockName, self.stockSdate_Val, self.stockEdate_Val)
        indicators = Indicator(price)
        firstInput = indicators.getIndicator(self.indicators_CMBO1.GetValue())
        secondInput = indicators.getIndicator(self.indicators_CMBO2.GetValue())
        thirdInput = indicators.getIndicator(self.indicators_CMBO3.GetValue())
        ourFuzzy = OurFuzzy()
        fuzzyOutSerics = pd.Series()
        fuzzySignal = pd.Series()
        for i in range(0, firstInput.size):
            fuzzyOutPut = OurFuzzy.fuzzyOut(ourFuzzy, firstInput[i], secondInput[i], thirdInput[i])
            fuzzyOutSerics = fuzzyOutSerics.set_value(i, fuzzyOutPut)
        fuzzyOutSerics = fuzzyOutSerics.set_value(i, fuzzyOutPut)

        traditional = tt(price)
        ttSignal = traditional.signal(self.indicators_CMBO1.GetValue(), self.indicators_CMBO2.GetValue(), self.indicators_CMBO3.GetValue())
        for index, value in fuzzyOutSerics.iteritems():
            if (value <= 0.4):
                fuzzySignal = fuzzySignal.set_value(index, 1)
            elif (value >= 0.6):
                fuzzySignal = fuzzySignal.set_value(index, -1)
            else:
                fuzzySignal = fuzzySignal.set_value(index, 0)
        backTest = BackTest()
        backTestResult = backTest.getBTresult(price, fuzzySignal, ttSignal)

        self.BackPanel.draw_subgraph(backTestResult)
        self.tradInformationList = backTest.getInfromationList()

        for i in self.tradInformationList: # show the processing information into the text box
            self.TextAInput.AppendText(i)

    def reFlashBackPanel(self):
        self.BackPanel.clear_subgraph()
        self.ProcessBackTest()
        self.BackPanel.update_subgraph()

class App(wx.App):
    def OnInit(self):
        self.frame = Frame()
        self.frame.ProcessStock()
        self.frame.Show()
        self.SetTopWindow(self.frame)
        return True

if __name__ == '__main__':
    app = App()
    app.MainLoop()