# -*- encoding: utf -*-
"""
Create on 2021/1/13 14:52
@author: Xiao Yijia
"""
from analysis.TrajectoryTime import TrajectoryTime
from util.Utils import Utils


class TrajectoryRelaxTime(TrajectoryTime):

    def __init__(self, db_name, ):
        super(TrajectoryRelaxTime, self).__init__(db_name, )

    def start_init(self, before_row):
        output_info = None
        if before_row[TrajectoryTime.INPUT_OR_OUTPUT_INDEX] == 'Input':
            mmsi = before_row[TrajectoryTime.MMSI_INDEX]
            arrive_time = Utils.convert_str_time_to_utc(before_row[TrajectoryTime.ARRIVE_TIME_INDEX])
            output_info = [mmsi, arrive_time]
        return output_info

    def deal_same_ship_case(self, after_row, output_info, csv_writer):
        if output_info is not None:
            next_start_time = Utils.convert_str_time_to_utc(after_row[TrajectoryTime.START_TIME_INDEX])
            output_info[1] = next_start_time - output_info[1]
            mmsi = output_info[0]
            dead_weight = after_row[TrajectoryTime.MMSI_INDEX]
            csv_writer.writerow(output_info)

            self.update_ship_level_info(mmsi, output_info[1])

        return self.start_init(after_row)
