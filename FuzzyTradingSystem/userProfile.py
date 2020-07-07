class userProfile:

    def __init__(self):
        self.cash_hold = 100000
        self.posit_num = 0
        self.market_total = 0
        self.profit_curve = []
        self.buy_price = 0
        self.tradInformationList = []
        self.skip_days = 0


    def get_cash_hold(self):
        return self.cash_hold

    def get_skip_days(self):
        return self.skip_days

    def get_posit_num(self):
        return self.posit_num

    def get_market_total(self):
        return self.market_total

    def get_profit_curve(self):
        return self.profit_curve

    def get_buy_price(self):
        return self.buy_price

    def get_tradInformationList(self):
        return self.tradInformationList

    def set_cash_hold(self,cash_hold):
        self.cash_hold = cash_hold

    def set_posit_num(self,posit_num):
        self.posit_num = posit_num

    def set_market_total(self , market_total):
        self.market_total = market_total

    def set_profit_curve(self ,  profit_curve):
        self.profit_curve.append(profit_curve)

    def set_buy_price(self, buy_price):
        self.buy_price = buy_price

    def set_skip_days(self,skip_days):
        self.skip_days = skip_days

    def set_tradInformationList(self,infor):
        self.tradInformationList.append(infor)