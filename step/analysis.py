# -*- encoding: utf -*-
"""
Create on 2020/12/2 11:20
@author: Xiao Yijia
"""
import matplotlib.pyplot as plt
import matplotlib
import numpy as np

from dao.commondb import CommonDB


def plot_length_width(db_name):
    db_file = CommonDB(db_name)
    db_file.run_sql("""
    SELECT length, width
    FROM china_trajectory_cn
    WHERE load_state = 1 AND 
           input_or_output = 'Input' AND 
           vessel_type_sub = 'Crude Oil Tanker' AND 
           length < 400 AND 
           width < 80
    ORDER BY arrive_Time;
    """)
    x = []
    y = []
    for row in db_file.db_cursor:
        x.append(row[0])
        y.append(row[1])

    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    ax1.scatter(x, y, color='blue')
    # plt.show()
    db_file.run_sql("""
    SELECT length, width
    FROM china_trajectory_cn
    WHERE (arrive_time BETWEEN 20141100000000 AND 20150000000000 OR
            arrive_time BETWEEN 20150500000000 AND 20150700000000) AND
            load_state = 1 AND
            input_or_output = 'Input' AND
            vessel_type_sub = 'Crude Oil Tanker'
     ORDER BY arrive_Time;
    """)
    x = []
    y = []
    for row in db_file.db_cursor:
        x.append(row[0])
        y.append(row[1])

    # fig = plt.figure()
    ax1.scatter(x, y, color='red')
    plt.show()


def test_plot():
    N = 10
    x = np.random.rand(N)
    y = np.random.rand(N)
    x2 = np.random.rand(N)
    y2 = np.random.rand(N)
    area = np.random.rand(N) * 1000
    fig = plt.figure(figsize=(12, 6))

    ax1 = fig.add_subplot(121)
    ax1.scatter(x, y, color='black', s=80, marker='o')
    ax1.scatter(x2, y2, color='green', s=80, marker='o')
    plt.show()


def plot_deadweight(param):
    db_file = CommonDB(param)
    db_file.run_sql("""
        SELECT deadweight/10000 AS weight, count()
        FROM china_trajectory_cn
        WHERE load_state = 1 AND
               input_or_output = 'Input' AND
               vessel_type_sub = 'Crude Oil Tanker'
        GROUP BY weight
        ORDER BY weight;
        """)
    x = []
    y = []
    for row in db_file.db_cursor:
        x.append(row[0])
        y.append(row[1])

    fig = plt.figure()
    # plt.xlim(0, 400000)
    ax1 = fig.add_subplot(111)
    ax1.bar(x, y)

    db_file.run_sql("""
          SELECT deadweight/10000 AS weight, count()
          FROM china_trajectory_cn
          WHERE (arrive_time BETWEEN 20141100000000 AND 20150000000000 OR
                  arrive_time BETWEEN 20150500000000 AND 20150700000000) AND 
                  load_state = 1 AND
                  input_or_output = 'Input' AND
                  vessel_type_sub = 'Crude Oil Tanker'
          GROUP BY weight
          ORDER BY weight;
        """)
    x = []
    y = []
    for row in db_file.db_cursor:
        x.append(row[0])
        y.append(row[1] * 20)

    ax1.bar(x, y, color='red')
    plt.show()


if __name__ == '__main__':
    # plot_length_width(r"D:\graduation\data\step_result\total\step7\trajectory.db")
    # plot_deadweight(r"D:\graduation\data\step_result\total\step7\trajectory.db")
    test_plot()
