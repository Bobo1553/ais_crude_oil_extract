# -*- encoding: utf -*-
"""
Create on 2020/11/6 22:33
@author: Xiao Yijia
"""
import csv

from const.const import Const
from dao.commondb import CommonDB
from service.aisservice import AISService
from service.deadweightdb import DeadweightDB
from service.draftdb import DraftDB
from service.portservice import PortService
from util.Utils import Utils


def split_ship_trajectory(target_db, draft_db, draft_state_table, ais_table, port_name, trajectory_output_file,
                          trajectory_output_header, search_distance, trajectory_distance_threshold,
                          trajectory_speed_threshold, outliers_output_file):
    Utils.check_file_path(trajectory_output_file)
    Utils.check_file_path(outliers_output_file)

    # 1. 读取数据库
    draft = DraftDB(draft_db)
    ais = AISService(target_db)
    port_service = PortService(port_name)

    trajectory_file = open(trajectory_output_file, 'wb')
    trajectory_writer = csv.writer(trajectory_file)
    trajectory_writer.writerow(trajectory_output_header)
    outliers_file = open(outliers_output_file, 'wb')
    outliers_writer = csv.writer(outliers_file)
    outliers_writer.writerow(['mmsi', 'mark', 'count'])

    # 2. 开始读取
    draft_state_dict = draft.start_fetch_transaction(draft_state_table)
    ais.start_fetch_data_transaction(ais_table)
    line_index = 0

    while draft.has_next_draft_state() and ais.has_next_ais_ship():
        compare_result = Utils.compare_mmsi(ais.ais_point, draft_state_dict)
        mmsi = ais.ais_point.mmsi
        mark = ais.ais_point.mark
        if compare_result < 0:
            ais.skip_useless_trajectory()
        elif compare_result > 0:
            draft_state_dict = draft.fetch_draft_state()
        else:
            line_index, outliers_count = ais.form_trajectory(draft_state_dict, trajectory_writer, line_index,
                                                             port_service, search_distance,
                                                             trajectory_distance_threshold, trajectory_speed_threshold)
            outliers_writer.writerow([mmsi, mark, outliers_count])

    # 3. 关闭
    trajectory_file.close()
    draft.close()
    ais.close()


def check_file(filename):
    with open(filename) as trajectory_file:
        file_reader = csv.reader(trajectory_file)
        print(next(file_reader))
        print(next(file_reader))
        print(next(file_reader))
        print(next(file_reader))
        print(next(file_reader))
        print(next(file_reader))


def check_file_by_creating_trajectory():
    mmsi = 215153000
    filename = r"D:\graduation\data\step_result\check\step4\trajectory_{}.csv".format(mmsi)
    target_file_name = r"D:\graduation\data\step_result\check\step4\trajectory_{}.txt".format(mmsi)
    port_name = r"D:\GeoData\Port\WPI.shp"
    degree_threshold = Const.LINE_NO_SPLIT_DEGREE

    port_service = PortService(port_name)
    Utils.convert_csv_to_format_txt(filename, target_file_name, port_service, degree_threshold)

    shp_file_name = r"D:\graduation\data\step_result\check\step4\trajectory_{}.shp".format(mmsi)
    Utils.create_shp(target_file_name, shp_file_name)


def start_init(ship_info, ships_deadweight, port_service):
    # ["line_index", "mmsi", "mark", "imo", "vessel_name", "vessel_type", "length", "width", "longitude", "latitude",
    #  "draft", "speed", "date", "utc", "source_port", "target_port", "load_state", ]
    deadweight_of_mmsi = ships_deadweight.get_deadweight_by_mmsi(ship_info[1])
    start_time = Utils.convert_utc_to_str_time(int(ship_info[12]))

    source_country = port_service.get_port_by_name(ship_info[13]).country
    input_or_output = get_input_or_output_state(None, source_country, True)

    trajectory_info = ship_info[:8] + [deadweight_of_mmsi, start_time, None, ] + ship_info[13:] + [input_or_output]
    # print(trajectory_info)

    return trajectory_info


def same_ship_deal(ship_info, another_ship_info, trajectory_info, port_service, csv_writer, ships_deadweight,
                   new_ship=False):
    final_deal(ship_info, trajectory_info, port_service, csv_writer)

    trajectory_info = start_init(another_ship_info, ships_deadweight, port_service)

    if not new_ship:
        trajectory_info[11] = ship_info[14]
    return trajectory_info


def get_input_or_output_state(input_or_output, country_name, before=True):
    if not before and country_name in Const.CHINA_NAME:
        if input_or_output is None:
            input_or_output = "Input"
        else:
            input_or_output = "Both"
    if before and country_name in Const.CHINA_NAME:
        if input_or_output is None:
            input_or_output = "Output"
        else:
            input_or_output = "Both"

    return input_or_output


def final_deal(ship_info, trajectory_info, port_service, csv_writer):
    arrive_time = Utils.convert_utc_to_str_time(int(ship_info[12]))
    trajectory_info[10] = arrive_time

    # input_or_output = trajectory_info[-1]
    target_country = port_service.get_port_by_name(ship_info[14]).country
    input_or_output = get_input_or_output_state(trajectory_info[-1], target_country, False)

    trajectory_info[-1] = input_or_output
    # print(trajectory_info)
    csv_writer.writerow(trajectory_info)


def get_trajectory_info(source_csv_file, static_info_file_header, static_info_file_for_analysis, deadweight_db,
                        deadweight_table, port_shp_file):
    # ['line_index', 'mmsi', 'mark', 'imo', 'vessel_name', 'vessel_type', 'length', 'width', 'deadweight',
    #  'start_time', 'arrive_time', 'source_port', 'target_port', 'load_state', 'input_or_output']
    Utils.check_file_path(static_info_file_for_analysis)

    # 1.acquire deadweight info and port info
    ships_deadweight = DeadweightDB(deadweight_db)
    ships_deadweight.init_ships_deadweight(deadweight_table)

    port_service = PortService(port_shp_file)

    static_info_file = open(static_info_file_for_analysis, 'wb')
    static_info_file_writer = csv.writer(static_info_file)

    static_info_file_writer.writerow(static_info_file_header)

    with open(source_csv_file) as source_file:
        source_reader = csv.reader(source_file)
        next(source_reader)
        before_line = source_reader.next()
        print(before_line)

        trajectory_info = start_init(before_line, ships_deadweight, port_service)

        for line in source_reader:

            if line[0] == before_line[0]:
                # print("!!!!!!!!!!!!!!1")
                pass
            elif line[1] == before_line[1]:
                # print(line)
                trajectory_info = same_ship_deal(before_line, line, trajectory_info, port_service,
                                                 static_info_file_writer, ships_deadweight, True)
            else:
                print(line)
                trajectory_info = same_ship_deal(before_line, line, trajectory_info, port_service,
                                                 static_info_file_writer, ships_deadweight, True)

            before_line = line

        final_deal(before_line, trajectory_info, port_service, static_info_file_writer)


def get_vessel_type_by_mmsi(addtion_info_db, mmsi):
    addtion_info_db.run_sql("SELECT vessel_type_sub FROM {} WHERE mmsi = {} limit 1;".format("OilTanker", mmsi))
    row = addtion_info_db.dbcursor.next()
    return row[0]


def add_vessel_type_info(source_csv_name, target_csv_name, addition_info_source_name):
    addition_info_db = CommonDB(addition_info_source_name)

    with open(source_csv_name, "r") as source_csv:
        source_reader = csv.reader(source_csv)
        with open(target_csv_name, "wb") as target_csv:
            target_writer = csv.writer(target_csv)

            line = next(source_reader)
            target_writer.writerow([line[-1]] + line[:-1])

            before_line = next(source_reader)
            before_mmsi = before_line[0]
            vessel_type = get_vessel_type_by_mmsi(addition_info_db, before_mmsi)
            before_line[4] = vessel_type
            target_writer.writerow([before_line[-1]] + before_line[:-1])

            for after_line in source_reader:
                after_mmsi = after_line[0]
                if before_mmsi != after_mmsi:
                    before_mmsi = after_mmsi
                    vessel_type = get_vessel_type_by_mmsi(addition_info_db, before_mmsi)
                after_line[4] = vessel_type
                target_writer.writerow([after_line[-1]] + after_line[:-1])


if __name__ == '__main__':
    target_db = r"D:\graduation\data\step_result\total\step2\OilTanker.db"
    draft_db = r"D:\graduation\data\step_result\total\step3\TankerDraft.db"
    draft_state_table = "TankerDraftState"
    ais_table = "OilTanker"
    port_name = r"D:\GeoData\Port\WPI.shp"
    # trajectory_output_file = r"D:\graduation\data\step_result\check\step4\trajectory_{}.csv".format(215153000)
    trajectory_output_file = r"D:\graduation\data\step_result\total\step4\trajectory.csv"
    outliers_output_file = r"D:\graduation\data\step_result\check\step4\outliers.csv"
    trajectory_output_header = ["mmsi", "mark", "imo", "vessel_name", "vessel_type", "length", "width", "longitude",
                                "latitude", "draft", "speed", "date", "utc", "source_port", "target_port", "load_state",
                                "line_index"]

    search_distance = 1000
    trajectory_distance_threshold = 3.4
    trajectory_speed_threshold = 18

    # split_ship_trajectory(target_db, draft_db, draft_state_table, ais_table, port_name, trajectory_output_file,
    #                       trajectory_output_header, search_distance, trajectory_distance_threshold,
    #                       trajectory_speed_threshold, outliers_output_file)
    #
    #
    # check_file_by_creating_trajectory()

    trajectory_output_with_vessel_type = r"D:\graduation\data\step_result\total\step4\trajectory_with_type.csv"
    source_db = r"D:\graduation\data\step_result\total\step1\OilTankerTemp.db"

    # check_file(trajectory_output_with_vessel_type)

    # add_vessel_type_info(trajectory_output_file, trajectory_output_with_vessel_type, source_db)

    header = ['line_index', 'mmsi', 'mark', 'imo', 'vessel_name', 'vessel_type', 'length', 'width', 'deadweight',
              'start_time', 'arrive_time', 'source_port', 'target_port', 'load_state', 'input_or_output']
    static_info_file_for_analysis = r"D:\graduation\data\step_result\total\step4\trajectory_info.csv"
    deadweight_db = r"D:\graduation\data\OilTankerWithDeadWeight.db"
    deadweight_table = "OilTankerFiles"
    port_shp_file = "D:\GeoData\Port\WPI.shp"
    get_trajectory_info(trajectory_output_with_vessel_type, header, static_info_file_for_analysis, deadweight_db,
                        deadweight_table, port_shp_file)
    # check_file(static_info_file_for_analysis)
