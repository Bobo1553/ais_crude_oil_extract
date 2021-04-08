# -*- encoding: utf -*-
"""
Create on 2020/10/15 10:36
@author: Xiao Yijia
"""
import pandas as pd

if __name__ == '__main__':
    s1 = pd.Series([6, 7, 15, 36, 39, 40, 41, 42, 43, 47, 49])
    print s1.describe()
