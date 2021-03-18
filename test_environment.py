# -*- encoding: utf -*-
"""
Create on 2020/12/2 17:32
@author: Xiao Yijia
"""

import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib


def test_plot():
    N = 10
    x = np.random.rand(N)
    y = np.random.rand(N)
    x2 = np.random.rand(N)
    y2 = np.random.rand(N)
    area = np.random.rand(N) * 1000
    # fig = plt.figure(figsize=(6, 6))
    fig = plt.figure()

    ax1 = fig.add_subplot(111)
    ax1.scatter(x, y, color='black', s=area, marker='o', )
    ax1.scatter(x2, y2, color='green', s=area, marker='o', )
    plt.show()


if __name__ == '__main__':
    # print(sys.path)
    test_plot()
