# -*- encoding: utf -*-
"""
Create on 2020/10/15 10:36
@author: Xiao Yijia
"""
import csv

from config.config import Config
from const.const import Const
from service.aisservice import AISService
from service.deadweightdb import DeadweightDB
from service.draftdb import DraftDB
from service.portservice import PortService
from util.Utils import Utils


def step1_get_oil_tanker():
    ais = AISService(Config.target_db)
    ais.import_data_from_path(Config.source_path, Config.source_table, Config.ais_table, Config.ais_rol_list)
    if Config.is_need_cleaning:
        ais.clean_dirty_data(Config.ais_table, Config.speed_threshold, Config.draft_threshold)


def step2_same_mmsi_identify():
    ais = AISService(Config.target_db)

    result_writer = open(Config.target_ais_csv, 'w')

    ais.start_fetch_data_transaction(Config.ais_table)
    while ais.has_next_ais_ship():
        ais.same_mmsi_identify(result_writer)

    return


def step2_get_draft_count_and_load_identify():
    draft = DraftDB(Config.target_db)
    draft.import_data(Config.ais_table, Config.draft_table, Config.draft_rol_list)
    draft.ships_draft_state_identify(Config.draft_table, Config.draft_state_table, Config.draft_state_rol_list)

    return


def step3_format_line():
    # 1. 读取数据库
    draft = DraftDB(Config.target_db)

    ais = AISService(Config.target_db)

    trajectory_file = open(Config.trajectory_output_file, 'wb')
    trajectory_writer = csv.writer(trajectory_file)
    trajectory_writer.writerow(Config.trajectory_output_header)

    port_service = PortService(Config.port_name)
    # port_service = ''

    # 2. 开始读取
    draft_state_dict = draft.start_fetch_transaction(Config.draft_state_table)
    ais.start_fetch_data_transaction(Config.ais_table)
    line_index = 0

    while draft.has_next_draft_state() and ais.has_next_ais_ship():
        compare_result = Utils.compare_mmsi(ais.ais_point, draft_state_dict)
        if compare_result < 0:
            ais.skip_useless_trajectory()
        elif compare_result > 0:
            draft_state_dict = draft.fetch_draft_state()
        else:
            line_index = ais.form_trajectory(draft_state_dict, trajectory_writer, line_index, port_service,
                                             Config.search_distance, Config.trajectory_distance_threshold,
                                             Config.trajectory_speed_threshold)

    # 3. 关闭
    trajectory_file.close()
    draft.close()
    ais.close()


def step4_extract_china_line():
    # 1. 获取港口
    port_service = PortService(Config.port_name)

    Utils.extract_country_trajectories(port_service, Config.trajectory_output_file, Config.china_trajectory_output_file,
                                       Config.trajectory_output_header + ['inputOrOutput'], Const.CHINA_NAME)


def step5_convert_csv_to_format_txt(file_name, degree_threshold):
    port_service = PortService(Config.port_name)

    Utils.convert_csv_to_format_txt(file_name, file_name.replace('.csv', '.txt'), port_service, degree_threshold)


def step6_get_static_info_file(file_name, static_info_file, degree_threshold):
    deadweights = DeadweightDB(Config.deadweight_db)
    deadweights.init_ships_deadweight(Config.deadweight_table)

    Utils.get_trajectory_static_info_file(file_name, deadweights, static_info_file, degree_threshold)


def step7_create_shp_file(file_name):
    Utils.create_shp(file_name.replace('.csv', '.txt'), file_name.replace('.csv', '.shp'))


if __name__ == '__main__':
    Config.parse_from_file("config/config.yml")

    # step1_get_oil_tanker()
    # ais = AISDB(Config.target_db)
    # ais.clean_dirty_data(Config.ais_table, Config.speed_threshold, Config.draft_threshold)
    #
    # step2_get_draft_count_and_load_identify()
    #
    # step3_format_line()
    #
    # step4_extract_china_line()
    # source_file_name = r"D:\graduation\data\result\china_trajectory\china_trajectory.csv"
    # start_line_num = 0
    # end_line_num = 100000 + start_line_num
    # output_file_name = source_file_name.replace(".csv", "_{}_{}.csv".format(start_line_num, end_line_num))
    #
    # Utils.split_china_trajectory_file(source_file_name, start_line_num, end_line_num)
    # print("split trajectory file finished")
    #
    # step5_convert_csv_to_format_txt(output_file_name)
    # print("format finished")
    #
    # step7_create_shp_file(output_file_name)
    # print("create shp file")

    step6_get_static_info_file(Config.china_trajectory_output_file, Config.static_info_file, Config.split_degree)

    # deadweight = DeadweightDB(Config.deadweight_db)
    # print(deadweight.get_ships_deadweight(Config.deadweight_table))

