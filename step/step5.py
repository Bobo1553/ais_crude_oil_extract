# -*- encoding: utf -*-
"""
Create on 2021/4/4 22:47
@author: Xiao Yijia
"""

import csv

import pandas as pd

from service.deadweightdb import DeadweightDB
from service.portservice import PortService
from util.Utils import Utils


class TrajectoryStep:
    MMSI_INDEX = 0
    MARK_INDEX = 1
    LON_INDEX = 8
    LAT_INDEX = 9
    DATE_INDEX = 12
    UTC_INDEX = 13
    FLAG_COUNTRY_INDEX = 7
    SOURCE_PORT_INDEX = 14
    SOURCE_DISTANCE_INDEX = 15
    TARGET_PORT_INDEX = 16
    TARGET_DISTANCE_INDEX = 17

    def __init__(self, trajectory_file_name, ):
        self.trajectory_file = open(trajectory_file_name)
        self.trajectory_reader = csv.reader(self.trajectory_file)

    def dirty_trajectory_clean(self, clean_file_name, time_threshold, distance_threshold, ):
        Utils.check_file_path(clean_file_name)

        clean_file = open(clean_file_name, 'wb')
        file_writer = csv.writer(clean_file)

        file_writer.writerow(next(self.trajectory_reader))  # write head

        trajectory_first = self.trajectory_reader.next()
        trajectory_list = [trajectory_first]

        for after_point in self.trajectory_reader:
            if not self.judge_same_line(trajectory_first, after_point):
                if not self.judge_dirty(trajectory_list, time_threshold, distance_threshold):
                    self.export_clean_trajecotry(trajectory_list, file_writer)

                trajectory_first = after_point
                trajectory_list = [trajectory_first]
            trajectory_list.append(after_point)

        if not self.judge_dirty(trajectory_list, time_threshold, distance_threshold):
            self.export_clean_trajecotry(trajectory_list, file_writer)

        clean_file.close()

    def extract_country_crude_oil(self, port_shp_name, deadweight_db, deadweight_table, import_file_name,
                                  export_file_name, file_header, need_full_load):
        Utils.check_file_path(import_file_name)
        Utils.check_file_path(export_file_name)

        import_file = open(import_file_name, "wb")
        import_writer = csv.writer(import_file)
        import_writer.writerow(file_header)
        export_file = open(export_file_name, "wb")
        export_writer = csv.writer(export_file)
        export_writer.writerow(file_header)

        port_service = PortService(port_shp_name)

        # get trajectory _info
        deadweights = DeadweightDB(deadweight_db)
        deadweights.init_ships_deadweight(deadweight_table)

        # skip header
        next(self.trajectory_reader)

        before = self.trajectory_reader.next()
        source_port_name = before[TrajectoryStep.SOURCE_PORT_INDEX]
        self.export_country_info(before, source_port_name, port_service, deadweights, export_writer, need_full_load)

        for after in self.trajectory_reader:
            if not self.judge_same_line(before, after):
                target_port_name = before[TrajectoryStep.TARGET_PORT_INDEX]
                self.export_country_info(before, target_port_name, port_service, deadweights, import_writer,
                                         need_full_load)
                source_port_name = after[TrajectoryStep.SOURCE_PORT_INDEX]
                self.export_country_info(after, source_port_name, port_service, deadweights, export_writer,
                                         need_full_load)
            before = after

        target_port_name = before[TrajectoryStep.TARGET_PORT_INDEX]
        self.export_country_info(before, target_port_name, port_service, deadweights, import_writer, need_full_load)

    def judge_same_line(self, before, after):
        return before[-1] == after[-1]

    def export_country_info(self, info, port_name, port_service, deadweights, writer, need_full_load):
        if need_full_load and not self.judge_full_load(info):
            return

        port = port_service.get_port_by_name(port_name)
        deadweight = deadweights.get_deadweight_by_mmsi(info[TrajectoryStep.MMSI_INDEX])
        writer.writerow([port.country, port.name, info[TrajectoryStep.MMSI_INDEX], info[TrajectoryStep.MARK_INDEX],
                         info[TrajectoryStep.LON_INDEX], info[TrajectoryStep.LAT_INDEX],
                         info[TrajectoryStep.DATE_INDEX], deadweight, info[TrajectoryStep.FLAG_COUNTRY_INDEX],
                         info[-1]])

    def judge_full_load(self, info):
        return int(info[-2]) == 1

    def judge_dirty(self, trajectory_list, time_threshold, distance_threshold, ):

        first_point = trajectory_list[0]
        last_point = trajectory_list[-1]

        if float(last_point[TrajectoryStep.UTC_INDEX]) - float(first_point[TrajectoryStep.UTC_INDEX]) < time_threshold:
            return True

        if float(first_point[TrajectoryStep.SOURCE_DISTANCE_INDEX]) > distance_threshold:
            return True

        if float(first_point[TrajectoryStep.TARGET_DISTANCE_INDEX]) > distance_threshold:
            return True

        return False

    def export_clean_trajecotry(self, trajectory_list, output_saver):
        for trajectory_point in trajectory_list:
            output_saver.writerow(trajectory_point)


def distance_check(trajectory_file_name):
    distance_list = []
    with open(trajectory_file_name) as trajectory_file:
        trajectory_reader = csv.reader(trajectory_file)

        before = next(trajectory_reader)
        for row in trajectory_reader:
            if row[-1] != before[-1]:
                distance_list.append(float(row[15]))
                distance_list.append(float(row[17]))
                before = row

    pd_distance = pd.Series(distance_list)
    print(pd_distance.describe())


def check_clean_file(clean_file_name):
    with open(clean_file_name) as clean_file:
        clean_reader = csv.reader(clean_file)
        mark = 0

        for row in clean_reader:
            if str(row[-1]) == '1091':
                print(row)
                mark = 1
            elif mark == 1:
                return


if __name__ == '__main__':
    trajectory_file_name = r"D:\graduation\data\step_result\step4\trajectory.csv"
    clean_file_name = r"D:\graduation\data\step_result\step4\trajectory_clean_time.csv"
    time_threshold = 86400
    distance_threshold = 1.07

    # trajectory = TrajectoryStep(trajectory_file_name)
    # trajectory.dirty_trajectory_clean(clean_file_name, time_threshold, distance_threshold, )

    port_name = r"D:\graduation\data\collection_data\graduation.gdb\world_port"
    deadweight_db = r"D:\graduation\data\OilTankerWithDeadWeight.db"
    deadweight_table = "OilTankerFiles"
    import_file_name = r"D:\graduation\data\step_result\step5\port_import_ship.csv"
    export_file_name = r"D:\graduation\data\step_result\step5\port_export_ship.csv"
    file_header = ["country", "port", "mmsi", "mark", "longitude", "latitude", "date", "deadweight", "flag_country",
                   "line_index", ]
    need_full_load = False

    new_trajectory = TrajectoryStep(clean_file_name)
    new_trajectory.extract_country_crude_oil(port_name, deadweight_db, deadweight_table, import_file_name,
                                             export_file_name, file_header, need_full_load)

    # check_clean_file(clean_file_name)
