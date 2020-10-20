import numpy as np

# 数据集
data_all = np.array([[1, 1, 1],  # 色泽， 根蒂， 敲声， 好瓜
                     [2, 1, 1],  # 青绿1  蜷缩1  浊响1  是1
                     [2, 1, 2],  # 乌黑2  稍蜷2  沉闷2  否2
                     [1, 1, 2],  # 浅白3  硬挺3  清脆3
                     [3, 1, 1],
                     [1, 2, 1],
                     [2, 2, 1],
                     [2, 2, 1],
                     [2, 2, 2],
                     [1, 3, 3],
                     [3, 3, 3],
                     [3, 1, 1],
                     [1, 2, 1],
                     [3, 2, 2],
                     [2, 2, 1],
                     [3, 2, 1],
                     [1, 3, 1],
                     [1, 2, 3],
                     [2, 2, 3],
                     [2, 2, 1],
                     [3, 2, 3],
                     [1, 1, 3],
                     [3, 3, 2],
                     [2, 3, 1],
                     [1, 3, 3],
                     [3, 1, 2],
                     [1, 2, 1],
                     [3, 3, 3],
                     [1, 1, 2]])
# 条件参数初始
condition_data_Y = np.array([[0.3, 0.4, 0.3],  # p(青绿1|是) p(乌黑2|是) p(浅白3|是)  色泽
                             [0.2, 0.35, 0.45],  # p(蜷缩1|是) p(稍蜷2|是) p(硬挺3|是)  根蒂
                             [0.5, 0.2, 0.3]])  # p(浊响1|是) p(沉闷2|是) p(清脆3|是)  敲声

condition_data_N = np.array([[0.3, 0.3, 0.4],  # p(青绿1|否) p(乌黑2|否) p(浅白3|否)  色泽
                             [0.33, 0.33, 0.34],  # p(蜷缩1|否) p(稍蜷2|否) p(硬挺3|否)  根蒂
                             [0.25, 0.5, 0.25]])  # p(浊响1|否) p(沉闷2|否) p(清脆3|否)  敲声


# 计算隐藏变量好瓜值
def hide():
    whether_good = []
    whether_data_b = []
    whether_data_g = []
    for i in range(0, data_all.shape[0]):
        result_g = condition_data_Y[0, data_all[i, 0] - 1] * condition_data_Y[1, data_all[i, 1] - 1] * condition_data_Y[
            2, data_all[i, 2] - 1]
        result_b = condition_data_N[0, data_all[i, 0] - 1] * condition_data_N[1, data_all[i, 1] - 1] * condition_data_N[
            2, data_all[i, 2] - 1]
        whether_data_b.append(result_b)
        whether_data_g.append(result_g)
        if result_g < result_b:
            whether_good.append(1)
        else:
            whether_good.append(0)
    print('whether_data_g', whether_data_g)
    print('whether_data_b', whether_data_b)
    print(whether_good)
    whether_good = np.array(whether_good)
    return whether_good


# 计算条件参数
def canshu(whether_good):
    for j in range(0, 3):
        a = 0
        b = 0
        c = 0
        for i in range(len(whether_good)):  # 父结点为好瓜
            if whether_good[i] == 0:
                if data_all[i, j] == 1:
                    a = a + 1
                if data_all[i, j] == 2:
                    b = b + 1
                if data_all[i, j] == 3:
                    c = c + 1
        print(a, b, c)
        condition_data_Y[j, 0] = round(a / np.sum(whether_good == 0), 2)
        condition_data_Y[j, 1] = round(b / np.sum(whether_good == 0), 2)
        condition_data_Y[j, 2] = round(c / np.sum(whether_good == 0), 2)
        print(condition_data_Y[j, 0], condition_data_Y[j, 1], condition_data_Y[j, 2])

    for j in range(0, 3):
        a = 0
        b = 0
        c = 0
        for i in range(len(whether_good)):  # 父结点为坏瓜
            if whether_good[i] == 1:
                if data_all[i, j] == 1:
                    a = a + 1
                if data_all[i, j] == 2:
                    b = b + 1
                if data_all[i, j] == 3:
                    c = c + 1
        print(a, b, c)
        condition_data_N[j, 0] = round(a / np.sum(whether_good == 1), 2)
        condition_data_N[j, 1] = round(b / np.sum(whether_good == 1), 2)
        condition_data_N[j, 2] = round(c / np.sum(whether_good == 1), 2)
        print(condition_data_N[j, 0], condition_data_N[j, 1], condition_data_N[j, 2])


for i in range(0, 5):
    a = hide()
    canshu(a)
    print('condition_data_Y', condition_data_Y)
    print('condition_data_N', condition_data_N)