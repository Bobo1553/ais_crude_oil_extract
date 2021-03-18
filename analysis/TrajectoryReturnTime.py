# -*- encoding: utf -*-
"""
Create on 2021/1/13 14:48
@author: Xiao Yijia
"""
import csv

from analysis.TrajectoryTime import TrajectoryTime
from basemodel.BetweenLineTransaction import BetweenLineTransaction
from util.Utils import Utils


class TrajectoryReturnTime(TrajectoryTime, BetweenLineTransaction, ):

    def __init__(self, db_name, mmsi_db_name, ):
        super(TrajectoryReturnTime, self).__init__(db_name, mmsi_db_name, )

    def fetch_trajectory_return_time(self, sql, trajectory_file_name, trajectory_header):
        self.start_fetch_data_transaction(sql)
        with open(trajectory_file_name, "wb") as output_file:
            output_writer = csv.writer(output_file)
            output_writer.writerow(trajectory_header)

            self.between_line_transaction_deal(self.source_db.db_cursor, output_writer)

    def fetch_data(self, data_reader, ):
        return data_reader.fetchone()

    def output_info_init(self, info):
        mmsi = info[TrajectoryTime.MMSI_INDEX]
        arrive_time = Utils.convert_str_time_to_utc(info[TrajectoryTime.ARRIVE_TIME_INDEX])
        deadweight = info[TrajectoryTime.DEADWEIGHT_INDEX]
        ship_static_info = self.fetch_ship_static_info(mmsi)
        return [str(mmsi), arrive_time, deadweight] + ship_static_info

    def judge_first_situation(self, before_info, after_info):
        return self.judge_same_line(before_info, after_info)

    def judge_second_situation(self, before_info, after_info):
        return self.judge_same_ship(before_info, after_info)

    def deal_second_situation(self, output_info, info, output_saver):
        next_arrive_time = Utils.convert_str_time_to_utc(info[TrajectoryTime.ARRIVE_TIME_INDEX])
        output_info[1] = next_arrive_time - output_info[1]
        mmsi = output_info[0]
        deadweight = output_info[2]
        output_saver.writerow(output_info)

        self.update_ship_level_info(str(mmsi) + "-" + str(deadweight), output_info[1])
        return self.output_info_init(info)

    def deal_default_situation(self, output_info, info, output_saver):
        return self.output_info_init(info)


if __name__ == '__main__':
    mmsi_db_name = r"D:\graduation\data\step_result\total\step1\OilTankerTemp.db"
    db_name = r"D:\graduation\data\step_result\total\step4\trajectory.db"
    sql = """
    SELECT *
      FROM trajectory_all
     WHERE
           vessel_type = 'Crude Oil Tanker' and input_or_output = 'Input' and load_state = 1
     ORDER BY line_index;
    """
    trajectory_file = r"D:\graduation\data\step_result\total\analysis\trajectory_analysis\trajectory_return_time_0113.csv"
    trajectory_header = ["mmsi", "return_time", "deadweight", "flag_country", ]
    return_time_item = TrajectoryReturnTime(db_name, mmsi_db_name)
    return_time_item.fetch_trajectory_return_time(sql, trajectory_file, trajectory_header)

    ship_file = r"D:\graduation\data\step_result\total\analysis\trajectory_analysis\ship_return_time_0113.csv"
    ship_header = ["mmsi", "return_time", "deadweight", "flag_country", ]
    return_time_item.export_ship_level_info_to_csv(ship_file, ship_header)
