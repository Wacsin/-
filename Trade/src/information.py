# encoding : utf8
# 该文件主要用于开户，记录用户交易信息记录，定义买、卖行为类型。
# 融资，融券行为定义在execute_func中
import time


class User():
    Company = "中盛恒生"
    account_Open_time = time.strftime('%Y%b%d %H:%M:%S', time.localtime(time.time()))
    record = []
    long_position = []
    short_position = []
    print(" Account created successfully."
          f"Company = {Company} "
          f"balance = 0")

    def __init__(self, balance, name):
        self.balance = balance
        self.name = name
        self.debt_money = 0
        self.debt_ticks = 0
        self.ticks = 0
        self.trade_money = 0
        self.wait_buy = 0
        self.long = False
        self.short = False
        self.ticker = 0
        self.totle_balance = 0
    def buy_in(self, _row):
        self.ticker = _row["ticker"]
        competitor = _row["P_N"] * _row["Q_N"]

        if self.wait_buy != 0:

            if competitor >= self.wait_buy:
                self.trade_money = self.wait_buy
                self.record.append(["buy", _row["ticker"], time.time(), _row["P_N"], self.trade_money / _row["P_N"], self.trade_money])
                self.ticks += self.trade_money / _row["P_N"]
                self.wait_buy = 0
                # 是否全成交， 成交量， 价格
                return 1, self.trade_money / _row["P_N"], _row["P_N"]

            else:
                self.trade_money = competitor
                self.record.append(["buy", _row["ticker"], time.time(), _row["P_N"], self.trade_money / _row["P_N"], self.trade_money])
                self.ticks += self.trade_money / _row["P_N"]
                self.wait_buy -= competitor
                return 0, _row["Q_N"], _row["P_N"]

        else:

            if self.balance > 0 and competitor >= 0.5 * self.balance:
                self.trade_money = 0.5 * self.balance
                self.record.append(["buy", _row["ticker"], time.time(), _row["P_N"], self.trade_money / _row["P_N"], self.trade_money])
                self.ticks += self.trade_money / _row["P_N"]
                self.balance -= self.trade_money
                return 1, self.trade_money / _row["P_N"], _row["P_N"]

            elif self.balance > 0 and competitor < 0.5 * self.balance:
                self.trade_money = _row["P_N"] * _row["Q_N"]
                # wait_buy 未成交
                self.wait_buy = 0.5 * self.balance - self.trade_money
                self.record.append(["buy", _row["ticker"], time.time(), _row["P_N"], self.trade_money / _row["P_N"], self.trade_money])
                self.ticks += self.trade_money / _row["P_N"]
                self.balance -= self.trade_money
                return 0, self.trade_money / _row["P_N"], _row["P_N"]

    # debt直接融的券，own融资后买的。分开是为了更好的表示多空
    def sell(self, price, debt_or_own="own"):
        if debt_or_own == "own":
            self.balance += self.ticks * price
            self.record.append(["sell", self.ticker, time.time(), price, self.ticks, self.ticks * price])
            self.ticks = 0
            self.long_position = []
        if debt_or_own == "debt":
            self.debt_ticks = 0.5 * self.balance / price
            self.balance += self.debt_ticks * price
            self.short_position.append(["debt_sell", self.ticker, time.time(), price, self.debt_ticks, self.debt_ticks * price])
            self.record.append(["debt_sell", self.ticker, time.time(), price, self.debt_ticks, self.debt_ticks * price])


