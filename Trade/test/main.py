# encoding:"utf8“
import pandas as pd
from information import User
from execute_func import data_read_func
from execute_func import point_justify
from execute_process import auto_process
from execute_func import draw

# 抑制科学技术法
pd.set_option('display.float_format', lambda x: '%.3f' % x)



# 无杠杆
if __name__ == "__main__":
    User = User(1000000, "Taro")
    User.ticker = 300482
    # 数据库文件读取
    bar = data_read_func(ticker_num=300482, YearMonthDAY=20210121, file_format="excel")
    # para_choice_help = bar.describe()
    #  数据筛选
    df_bar2 = point_justify(bar, start_time=20210121092500000, stop_time=20210121150000000, stock=300482)
    #  预测过程（该过程中并非镜像计算，而是由实例主体进行交易。）
    _,matplot_param = auto_process(User, df_bar2)
    # 绘图函数
    draw(matplot_param)