# encoding:"utf8“
import pandas as pd
from information import User
from execute_func import data_read_func
from execute_func import long, long_throw
from execute_func import point_justify
from execute_func import short, short_throw


def mat_para(User, _row):
    time = int(str(_row["data_time"])[9:15])
    total_balance = User.balance + (User.ticks - User.debt_ticks) * _row["P_N"]
    return [time, total_balance]


def auto_process(User, df_bar):
    df_bar2 = df_bar
    buy_trigger = df_bar2[(df_bar2['close_price'] - df_bar2['P_N'] < (-df_bar2['P_N'] * 0.006)) & (
            ((df_bar2['bid_qty_M'] - df_bar2['ask_qty_M']) - df_bar2['OB_Q_N_3']) > (df_bar2['Q_N'] / 2))]
    sell_trigger = df_bar2[(df_bar2['close_price'] - df_bar2['P_N'] > (df_bar2['P_N'] * 0.006)) & (
            ((df_bar2['ask_qty_M'] - df_bar2['bid_qty_M']) - df_bar2['OB_QQ_N_3']) < (df_bar2['Q_N'] / 2))]

    matplot_param = []

    for _index, _row in df_bar2.iterrows():
        if int(str(_row["data_time"])[9:13]) <= 1450:
            # 如果能买就作多
            if _index in buy_trigger.index:
                ret = long(User, _row)
                matplot_param.append(mat_para(User, _row))
            # 如果 +— 2% 就止盈止损
            try:
                if User.long_position[0] == "BUY_FINISH" and _row["P_N"] >= 1.02 * User.long_position[-1]:
                    long_throw(User, _row["P_N"])
                elif User.long_position[0] == "BUY_FINISH" and _row["P_N"] <= 0.98 * User.long_position[-1]:
                    long_throw(User, _row["P_N"])
                matplot_param.append(mat_para(User, _row))
            except IndexError:
                pass

            # 空点就空
            if _index in sell_trigger.index:
                short(User, _row)
                matplot_param.append(mat_para(User, _row))

            # 平空点就平空
            try:
                if _row["P_N"] >= 1.02 * User.short_position[0][3] or _row["P_N"] < 0.98 * User.short_position[0][3]:
                    short_throw(User, _row)
                matplot_param.append(mat_para(User, _row))
            except IndexError:
                pass
        else:
            short_throw(User, _row)
            matplot_param.append(mat_para(User, _row))
            long_throw(User, _row["P_N"])
            matplot_param.append(mat_para(User, _row))
            break
    return User,matplot_param





