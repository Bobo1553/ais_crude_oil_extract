# -*- encoding: utf -*-
"""
Create on 2021/4/9 11:27
@author: Xiao Yijia
"""
import csv

import statsmodels.api as sm
import matplotlib.pyplot as plt
import pandas as pd


class TimeSequence(object):

    def __init__(self, source_file_name, value_col, index_col):
        self.data = pd.read_csv(source_file_name, usecols=[index_col, value_col], index_col=index_col)

    def decompose(self, value_col, freq, save_file):
        rd = sm.tsa.seasonal_decompose(self.data[value_col].values, period=freq)

        with open(save_file, 'w', newline='') as save:
            save_writer = csv.writer(save)
            save_writer.writerow(['ID', 'Cycle', 'Trend', 'Residuals'])
            for i, trend_value in enumerate(rd.trend):
                if trend_value is not None:
                    save_writer.writerow([i, rd.seasonal[i]/10000, trend_value/10000, rd.resid[i]/10000, ])
                else:
                    save_writer.writerow([i, rd.seasonal[i]/10000, '', ''])

        rd.plot()
        plt.show()


if __name__ == '__main__':
    source_file_name = r"D:\graduation\data\analysis\chapter4\correct\china-daily.csv"
    month_file_name = r"D:\graduation\data\analysis\chapter4\correct\china-month.csv"
    season_file_name = r"D:\graduation\data\analysis\chapter4\correct\china-season.csv"

    value_col = "dailyW"
    index_col = "day"
    month_freq = 30
    season_freq = 91

    china_daily = TimeSequence(source_file_name, value_col, index_col)
    china_daily.decompose(value_col, month_freq, month_file_name)
    china_daily.decompose(value_col, season_freq, season_file_name)
