import os
import pickle
import numpy as np
import pandas as pd
import CharacteristicEngineering.train_characteristic
from CharacteristicEngineering.train_characteristic import Smote
import copy



if __name__ == "__main__":
    # train_data = pd.read_csv(r"../src/train.csv")
    # train_data = pd.DataFrame(train_data)
    # test_1 = CharacteristicEngineering.train_characteristic.train_data
    # test_info = test_1.info()
    # test_null = test_1.isnull().any()
    # print(test_null)

    # 由于linux下dataprep包出现GUI图形界面问题，故此处代码删掉了dataprep观察特征协方差矩阵的部分
    # 根据结果，选取六个特征
    # x = train_data.iloc[:, [8, 9, 10, 18, 20, 21]]
    # label = train_data["label"]
    # data = train_data.iloc[:, [8, 9, 10, 18, 20, 21, 24]]
    #CharacteristicEngineering.train_characteristic.unbalance_judge(label)
    # 样本分布不均衡,正例只有3.14%。过于失衡，升采样效果比降采样明显许多
    # 这里使用smote算法，经百度，是一种在路径上添加样本的算法。
    # posDf = data[data["label"] == 1].drop(["label"], axis=1)
    # smote需要输入array，取消dataframe索引
    # posArray = posDf.values
    # posArray = np.asarray(posArray)
    # newPosArray = Smote(posArray, 20, 10).over_sampling()
    # newPosDf = pd.DataFrame(newPosArray)
    # newPosDf[6] = 1
    # label = 1 的数据变双倍，加回 label = 0的，再看看分布
    # data_col_washed = CharacteristicEngineering.train_characteristic.wash_cols_index(data)
    # data_oversampled = pd.concat([data_col_washed, newPosDf], axis=0)
    # label_more = data_oversampled.iloc[:, -1]
    # CharacteristicEngineering.train_characteristic.unbalance_judge(label_more)
    # data_oversampled.to_csv(r"../src/train_enhanced.csv")

    # 升采样后的数据集为变量data_more,我命名为train_enhanced保存在src目录里了。
    # 前面的部分都特征工程的，就此告一段落。
    test_data_whole = pd.read_csv("../src/test.csv")
    test_data = test_data_whole.iloc[:, [8, 9, 10, 18, 20, 21]]
    loaded_model = pickle.load(open("../user_predict_models/lr_pre_model.dat", "rb"))
    test_y_pre = loaded_model.predict(test_data.values)
    uid = test_data_whole.iloc[:, 0]
    result = pd.DataFrame(columns=["uid", "label"])
    result["uid"] = uid
    result["label"] = test_y_pre
    result.to_csv("../src/result.csv", index=True)
