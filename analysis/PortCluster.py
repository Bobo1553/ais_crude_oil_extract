# -*- encoding: utf -*-
"""
Create on 2021/4/20 11:29
@author: Xiao Yijia
"""

from sklearn.cluster import DBSCAN
import csv
import numpy as np
import matplotlib.pyplot as plt

# const
NAME_INDEX = 3
LATITUDE_INDEX = 5
LONGITUDE_INDEX = 6
WEIGHT_INDEX = 7

# parameter
port_position_file_name = r"D:\graduation\data\analysis\chapter5\port_position.csv"
save_file_name = r"D:\graduation\data\analysis\chapter5\port_area.csv"
eps = 2.3

with open(port_position_file_name) as port_position_file:
    port_position_reader = csv.reader(port_position_file)
    positions = []
    weights = []
    port_name = []
    next(port_position_reader)

    for row in port_position_reader:
        positions.append([float(row[LATITUDE_INDEX]), float(row[LONGITUDE_INDEX])])
        weights.append(float(row[WEIGHT_INDEX]))
        port_name.append(row[NAME_INDEX])

    np_positions = np.array(positions)
    np_weights = np.array(weights)

    clustering = DBSCAN(eps).fit(np_positions, sample_weight=np_weights)
    # clustering = DBSCAN(eps).fit(np_positions)
    print(clustering.labels_)

    with open(save_file_name, "w", newline="") as save_file:
        save_writer = csv.writer(save_file)

        save_writer.writerow(["port_name", "longitude", "latitude", "oil", "area_index"])
        for idx, label in enumerate(clustering.labels_):
            save_writer.writerow([port_name[idx], positions[idx][1], positions[idx][0], weights[idx], label])

    plt.scatter(np_positions[:, 1], np_positions[:, 0], marker='o', c=clustering.labels_)

    plt.show()
