import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import matplotlib
import time
import random
from sklearn.neighbors import NearestNeighbors
# 字体和精度的基本设置
np.set_printoptions(precision=3, suppress=False)
pd.set_option("display.float_format", lambda x: '%.2f' % x)
pd.set_option("display.max_columns", None)


# 判断样本是否均衡
def unbalance_judge(judge_data):
    # 进入的样本可能是被选过特征的，所以要重置索引
    # col_lis = list(range(0, data_frame.shape[1]))
    # if not columns:
    #     columns = col_lis
    # data_frame.columns = col_lis
    # for i in columns:
    # p = data_frame.iloc[:, 1].value_counts()
    p = judge_data.value_counts()
    plt.figure(figsize=(10, 6))
    patches, l_text, p_text = plt.pie(p, labels=["label=0", "label=1"], autopct='%1.2f%%', explode=(0, 0.1))
    for t in l_text:
        t.set_size(15)
    for t in p_text:
        t.set_size(15)
    plt.show()


# smote升采样
class Smote:
    def __init__(self, samples, N, k):
        self.n_samples, self.n_attrs = samples.shape
        self.n_samples = samples
        self.N = N
        self.k = k
        self.samples = samples
        self.newindex = 0

    def over_sampling(self):
        N = int(self.N)
        # 空的样本表
        # print(self.n_samples.shape[0])
        self.synthetic = np.zeros((list(self.n_samples.shape)[0] *N, self.n_attrs))
        neighbors = NearestNeighbors(n_neighbors=self.k).fit(self.samples)
        for i in range(len(self.samples)):
            nnarrny = neighbors.kneighbors(self.samples[i].reshape(-1, 6), return_distance=False)[0]
            self._populate(N, i, nnarrny)
        return self.synthetic

    # 2.为每个少数类样本选择k个最近邻中的N个；3.并生成N个合成样本
    def _populate(self, N, i, nnarrny):
        for j in range(N):
            nn = random.randint(0, self.k-1)
            dif = self.samples[nnarrny[nn]] - self.samples[i]
            gap = random.random()
            self.synthetic[self.newindex] = self.samples[i] + gap*dif
            self.newindex += 1


def wash_cols_index(data_will_wash):
    col_lis = list(range(0, data_will_wash.shape[1]))
    data_will_wash.columns = col_lis
    return data_will_wash







