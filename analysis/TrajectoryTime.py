# -*- encoding: utf -*-
"""
Create on 2020/11/30 16:31
@author: Xiao Yijia
"""
import csv

from const.ConstSQL import ConstSQL
from dao.commondb import CommonDB


class TrajectoryTime(object):
    LINE_INDEX = 0
    MMSI_INDEX = 1
    MARK_INDEX = 2
    DEADWEIGHT_INDEX = 8
    START_TIME_INDEX = 9
    ARRIVE_TIME_INDEX = 10
    SOURCE_INDEX = 11
    LOAD_STATE_INDEX = 13
    INPUT_OR_OUTPUT_INDEX = 14

    def __init__(self, db_name, mmsi_db_name):
        self.source_db = CommonDB(db_name)
        self.mmsi_db_name = CommonDB(mmsi_db_name)
        self.ship_level_info = {}

    def start_fetch_data_transaction(self, sql):
        self.source_db.run_sql(sql)
        return self.source_db.db_cursor

    @classmethod
    def judge_same_line(cls, before_row, after_row):
        return before_row[TrajectoryTime.LINE_INDEX] == after_row[TrajectoryTime.LINE_INDEX]

    @classmethod
    def judge_same_ship(cls, before_row, after_row):
        return before_row[TrajectoryTime.MMSI_INDEX] == after_row[TrajectoryTime.MMSI_INDEX] and \
               before_row[TrajectoryTime.MARK_INDEX] == after_row[TrajectoryTime.MARK_INDEX]

    def export_ship_level_info_to_csv(self, file_name, header):
        with open(file_name, "wb") as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(header)

            for key, values in self.ship_level_info.items():
                value, count = values
                mmsi, deadweight = key.split("-")
                ship_static_info = self.fetch_ship_static_info(mmsi)
                csv_writer.writerow([mmsi, value * 1.0 / count, deadweight, ] + ship_static_info)

    def update_ship_level_info(self, key, append_value):
        if key in self.ship_level_info:
            value, count = self.ship_level_info[key]
        else:
            value, count = 0, 0
        value += append_value
        count += 1
        self.ship_level_info[key] = (value, count)

    def fetch_ship_static_info(self, mmsi):
        self.mmsi_db_name.run_sql(ConstSQL.FETCH_SHIP_STATIC_INFO.format(mmsi))
        return list(self.mmsi_db_name.db_cursor.next())


if __name__ == '__main__':
    pass
