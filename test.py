# # -*- encoding: utf -*-
# """
# Create on 2020/10/15 10:36
# @author: Xiao Yijia
# """
#
# # import pandas as pd
# import math
#
# import numpy as np
#
#
# def analysis(arr):
#     arr = [math.log10(item) for item in arr]
#     # 求均值
#     arr_mean = np.mean(arr)
#     # 求方差
#     arr_var = np.var(arr)
#     # 求标准差
#     arr_std = np.std(arr, ddof=1)
#     print("平均值为：%f" % arr_mean)
#     print("方差为：%f" % arr_var)
#     print("标准差为:%f" % arr_std)
#
#
# def aaa(b, c):
#     if b is None and c is None:
#         return
#     elif c is None:
#         return b
#     elif b is None:
#         return -c
#     else:
#         return b - c
#
#
# if __name__ == '__main__':
#     huabei_arr = [16063, 12946, 9230, 4780, 4709, 3757, 2957, 1335, 1064, 663, 317, 89, 82, 60, 36, ]
#     huazhong_arr = [12275, 11028, 4732, 1145, 599, 64, 59, 30, 26, 16, 14, 10, 1, 1, ]
#     huanan_arr = [5732, 3148, 383, 314, 244, 200, 189, 172, 101, 34, 27, 18, 15, 1, ]
#     south_arr = [5782, 3011, 2745, 2226, 704, 346, 185, 68, 32, 20, ]
#     print("huabei")
#     analysis(huabei_arr)
#     print("huazhong")
#     analysis(huazhong_arr)
#     print("huanan")
#
#     analysis(huanan_arr)
#     print("south")
#     analysis(south_arr)

print(30125745/12232263)