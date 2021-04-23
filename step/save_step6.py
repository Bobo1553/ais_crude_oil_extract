# -*- encoding: utf -*-
"""
Create on 2020/11/6 22:40
@author: Xiao Yijia
"""
import csv
import os

from const.const import Const
from service.deadweightdb import DeadweightDB
from service.portservice import PortService
from util.Utils import Utils


def get_for_analysis(deadweight_db, deadweight_table, source_csv_file, static_info_file_for_analysis, ):
    Utils.check_file_path(static_info_file_for_analysis)

    # get trajectory _info
    deadweights = DeadweightDB(deadweight_db)
    deadweights.init_ships_deadweight(deadweight_table)

    Utils.get_trajectory_static_info_file(source_csv_file, deadweights, static_info_file_for_analysis,
                                          static_info_file_header, Const.LINE_NO_SPLIT_DEGREE)

    return


def split_source_csv_file(source_csv_file, target_path, split_csv_file_name, line_cover=100000):
    with open(source_csv_file) as source_csv:
        source_csv_reader = csv.reader(source_csv)
        header = source_csv_reader.next()

        target_index = 0
        Utils.check_path(os.path.join(target_path, str(target_index)))
        print(os.path.join(target_path, str(target_index)))
        os.chdir(os.path.join(target_path, str(target_index)))

        split_csv_file = open(split_csv_file_name, 'wb')
        split_csv_writer = csv.writer(split_csv_file)
        split_csv_writer.writerow(header)

        for row in source_csv_reader:
            if int(row[15]) / line_cover != target_index:
                split_csv_file.close()
                target_index += 1

                os.chdir(os.path.join(target_path, str(target_index)))
                split_csv_file = open(split_csv_file_name, 'wb')
                split_csv_writer = csv.writer(split_csv_file)
                split_csv_writer.writerow(header)
                split_csv_writer.writerow(row)
            else:
                split_csv_writer.writerow(row)

        split_csv_file.close()
        return target_index + 1


def create_shp_with_info(port_shp_file, deadweight_db, deadweight_table, source_csv_file, target_path, split_csv_file,
                         format_txt_file, static_info_file_for_shp, shp_file, split_trajectory_degree):
    split_count = split_source_csv_file(source_csv_file, target_path, split_csv_file)

    port_service = PortService(port_shp_file)

    deadweights = DeadweightDB(deadweight_db)
    deadweights.init_ships_deadweight(deadweight_table)

    for i in range(split_count):
        os.chdir(os.path.join(target_path, str(i)))

        Utils.convert_csv_to_format_txt(split_csv_file, format_txt_file, port_service, split_trajectory_degree)

        Utils.get_trajectory_static_info_file(split_csv_file, deadweights, static_info_file_for_shp,
                                              static_info_file_header, split_trajectory_degree)

    Utils.create_shp(format_txt_file, shp_file)
    return


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
    port_shp_file = r"D:\GeoData\Port\WPI.shp"
    deadweight_db = r"D:\graduation\data\OilTankerWithDeadWeight.db"
    deadweight_table = "OilTankerFiles"
    # source_csv_file = r"D:\graduation\data\step_result\check\step4\trajectory_{}.csv".format(215153000)
    source_csv_file = r"D:\graduation\data\step_result\total\step5\china_trajectory_all.csv"
    # source_csv_path = r"D:\graduation\data\step_result\total\step6\split_china_trajectory"
    target_path = r"D:\graduation\data\step_result\check\step6\trajectory"
    split_csv_file = "trajectory_{}.csv".format(215153000)
    format_txt_file = r"trajectory_{}.txt".format(215153000)
    shp_file = r"trajectory_{}.shp".format(215153000)
    static_info_file_for_shp = r"trajectory_{}_for_shp.csv".format(215153000)
    # static_info_file_for_analysis = r"D:\graduation\data\step_result\check\step6\trajectory_{}_for_analysis.csv".format(215153000)
    static_info_file_for_analysis = r"D:\graduation\data\step_result\total\step6\china_trajectory_all_for_analysis.csv"
    static_info_file_header = ['line_index', 'mmsi', 'mark', 'imo', 'vessel_name', 'vessel_type', 'length', 'width',
                               'deadweight', 'start_time', 'arrive_time', 'source_port', 'target_port', 'load_state',
                               'input_or_output']
    split_trajectory_degree = 300

    get_for_analysis(deadweight_db, deadweight_table, source_csv_file, static_info_file_for_analysis, )

    # create_shp_with_info(port_shp_file, deadweight_db, deadweight_table, source_csv_file, target_path, split_csv_file,
    #                      format_txt_file, static_info_file_for_shp, shp_file, split_trajectory_degree)

    # format_txt_file_list = [
    #     r"D:\graduation\data\step_result\total\step6\split_china_trajectory\0\china_trajectory_cn.txt",
    #     r"D:\graduation\data\step_result\total\step6\split_china_trajectory\1\china_trajectory_cn.txt",
    #     r"D:\graduation\data\step_result\total\step6\split_china_trajectory\2\china_trajectory_cn.txt",
    #     r"D:\graduation\data\step_result\total\step6\split_china_trajectory\3\china_trajectory_cn.txt",
    #     r"D:\graduation\data\step_result\total\step6\split_china_trajectory\4\china_trajectory_cn.txt",
    #     r"D:\graduation\data\step_result\total\step6\split_china_trajectory\5\china_trajectory_cn.txt",
    #     r"D:\graduation\data\step_result\total\step6\split_china_trajectory\6\china_trajectory_cn.txt",
    #     r"D:\graduation\data\step_result\total\step6\split_china_trajectory\7\china_trajectory_cn.txt",
    #     r"D:\graduation\data\step_result\total\step6\split_china_trajectory\8\china_trajectory_cn.txt",
    #     r"D:\graduation\data\step_result\total\step6\split_china_trajectory\9\china_trajectory_cn.txt",
    #     r"D:\graduation\data\step_result\total\step6\split_china_trajectory\10\china_trajectory_cn.txt",
    # ]
    #
    # for format_txt_file_item in format_txt_file_list:
    #     Utils.create_shp(format_txt_file_item, format_txt_file_item.replace(".csv", ".shp"))
