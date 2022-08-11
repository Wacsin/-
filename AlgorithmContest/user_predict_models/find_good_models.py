# 在这里我打算用逻辑回归，SVC、随机森林、LightBGM各自预测下，并评价好坏。
import os
import pickle
import time
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression as LR
from sklearn.svm import SVC as SVC
from sklearn.ensemble import RandomForestClassifier as RF
from lightgbm import LGBMClassifier as LGB
from sklearn.metrics import precision_score,recall_score,f1_score,classification_report
from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold


# KFold 交叉验证神器. 由于给了验证集，我就5折交叉吧
import CharacteristicEngineering.train_characteristic

# classifier不是变量是“别名”
def kFold_cv(X, y, classifier, **kwargs):
    kf = KFold(n_splits=5, shuffle=True)
    y_pred = np.zeros(len(y))
    start = time.time()
    for train_index, test_index in kf.split(X):
        X_train = X[train_index]
        X_test = X[test_index]
        y_train = y[train_index]
        clf = classifier(**kwargs)
        clf.fit(X_train, y_train)
        y_pred[test_index] = clf.predict(X_test)
        print("time used is :{}".format(time.time()-start))
        return y_pred


data = pd.read_csv("../src/train_enhanced.csv")
data = CharacteristicEngineering.train_characteristic.wash_cols_index(data)
X = data.iloc[:, 1:-1]
Y = data.iloc[:, -1]
x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=1)
lr_model = LR(penalty="l2", C=1.0).fit(x_train, y_train)
# 用values就不用asarray了，Dataframe取消索引秒变array,熊猫牌果然方便实惠～
# lr_prediction = kFold_cv(x_train.values, y_train.values, LR, penalty="l2", C=1.0)
# svc_prediction = kFold_cv(x_train.values, y_train.values, SVC, C=1.0)
# rf_prediction = kFold_cv(x_train.values, y_train.values, RF, n_estimators=100, max_depth=100)
# lgb_prediction = kFold_cv(x_train.values, y_train.values, LGB, learning_rate=0.1, n_estimators=500, max_depth=10)
# print(lr_prediction)
# # support mechain 最慢了
# # 做个表格看，弄个空表先
# scoreDf = pd.DataFrame(columns=['LR', 'SVC', 'RandomForest', 'LGB'])
# pred = [lr_prediction, svc_prediction, rf_prediction, lgb_prediction]
# # print(scoreDf)
# for i in range(len(pred)):
#     precision_rate = precision_score(y_train.values, pred[i])
#     recall_rate = recall_score(y_train.values, pred[i])
#     f1 = f1_score(y_train, pred[i])
#     scoreDf.iloc[:, i] = pd.Series([precision_rate, recall_rate, f1])
# scoreDf.index = ["precision_rate", "recall_rate", "f1"]


"""
笑死我了，费老大劲发现最后结果几乎一样。
找个跑得快的模型保存了吧。
                 LR  SVC  RandomForest  LGB
precision_rate 0.99 0.99          0.99 0.99
recall_rate    0.20 0.20          0.20 0.20
f1             0.33 0.33          0.33 0.33
"""

pickle.dump(lr_model, open("lr_pre_model.dat", "wb"))
