# -*- encoding: utf -*-
"""
Create on 2020/11/6 22:38
@author: Xiao Yijia
"""
import csv

from const.const import Const
from service.portservice import PortService
from util.Utils import Utils


def extract_country_relation_trajectory(port_shp_file, source_trajectory_file, country_trajectory_file,
                                        trajectory_header, country_name):
    Utils.check_file_path(country_trajectory_file)

    # 1. 获取港口
    port_service = PortService(port_shp_file)

    Utils.extract_country_trajectories(port_service, source_trajectory_file, country_trajectory_file,
                                       trajectory_header, country_name)


def check_file(filename):
    with open(filename) as trajectory_file:
        file_reader = csv.reader(trajectory_file)
        print(next(file_reader))
        print(next(file_reader))
        print(next(file_reader))
        print(next(file_reader))
        print(next(file_reader))
        print(next(file_reader))


if __name__ == '__main__':
    port_shp_file = "D:\GeoData\Port\WPI.shp"
    source_trajectory_file = r"D:\graduation\data\step_result\total\step4\trajectory.csv"
    country_trajectory_file = r"D:\graduation\data\step_result\total\step5\china_trajectory_all.csv"
    trajectory_header = ["mmsi", "mark", "imo", "vessel_name", "vessel_type", "length", "width", "longitude",
                         "latitude", "draft", "speed", "utc", "source_port", "target_port",
                         "load_state", "line_index", "inputOrOutput"]
    country_name = Const.CHINA_NAME

    extract_country_relation_trajectory(port_shp_file, source_trajectory_file, country_trajectory_file,
                                        trajectory_header, country_name)
    #
    # check_file(country_trajectory_file)
