import pandas as pd
import numpy as np
import time
import matplotlib.pyplot as plt
import matplotlib
from pylab import xticks, yticks
import matplotlib.ticker as ticker


# 输入时间和股票代码，返回指定数据,数据集要存放在datas目录下
def data_read_func(ticker_num=300482, YearMonthDAY=20010502, file_format="excel"):
    path = str(ticker_num) + "_" + str(YearMonthDAY)
    if format == "excel" or "xlsx":
        filename = path + ".xlsx"
        return pd.read_excel(f"../datas/{filename}")
    elif format == "csv":
        filename = path + ".csv"
        return pd.read_csv(f"../datas/{filename}")
    else:
        raise FileExistsError("No such format!")


def point_justify(bar, start_time, stop_time,stock):
    df_bar2 = bar[
        (bar['data_time'] >= start_time) &
        (bar['data_time'] < stop_time) &
        (bar['ticker'] == stock) &
        (bar['period'] == 15000) &
        bar['P_N'] > 0]
    return df_bar2


# 无杠杆，认为单倍作多，传入作多前的账户和作多对应的数据行
def long(User, time_row):
    while User.long is False:
        ret = User.buy_in(time_row)
        User.long_position.append(list(ret[1:]))
        if ret[0] == 1:
            # 买够了,但有可能是陆陆续续买近来的，需要计算下均价
            User.long = True
            avr_price = 0
            sum_Q = 0
            for i in User.long_position:
                sum_Q += i[0]
                avr_price += i[0] * i[1]
                if np.asarray(User.long_position).shape==(1,2):
                    pass
            avr_price = avr_price / sum_Q
            User.long_position = ["BUY_FINISH", sum_Q, avr_price]
            return User.long_position[2]
        if ret == 0:
            return "NotEnough"


def long_throw(User, price):
    if User.long is True:
        User.sell(price=price, debt_or_own="own")
        User.long = False
        return User


def short(User, time_row):
    if User.short is False:
        User.sell(price=time_row["P_N"], debt_or_own="debt")
        User.short = True
        return User.short_position[0][3]


def short_throw(User, time_row):
    if User.short is True:
        User.record.append([["debt_clear",User.ticker, time.time(), time_row["P_N"], User.debt_ticks, User.debt_ticks * time_row["P_N"]]])
        User.balance -= User.debt_ticks * time_row["P_N"]
        User.debt_ticks = 0
        User.short = False
        User.short_position = []


def time_format(timelist):
    time_dealed = []
    for i in timelist:
        i = str(int(i))
        second = i[-2:]
        min = i[-4:-2]
        hour = i[0:-4]
        time_dealed.append(":".join([hour,min,second]))
    return time_dealed




def draw(matplot_param):
    ls = np.asarray(matplot_param)
    ls=ls.transpose(1,0)
    time_para = ls[0]
    time_dealed =time_format(time_para)
    balance_para = list(map(lambda x: x/1000000, ls[1]))
    fig, ax = plt.subplots(1, 1)
    tick_spacing = 250
    ax.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))
    plt.plot(time_dealed, balance_para,"b*--", alpha=0.5, linewidth=0.3, label="rate")
    plt.xlabel("time")
    plt.ylabel("rate")
    plt.show()