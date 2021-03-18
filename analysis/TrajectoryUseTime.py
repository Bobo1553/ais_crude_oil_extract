# -*- encoding: utf -*-
"""
Create on 2021/1/13 14:54
@author: Xiao Yijia
"""
import csv

from analysis.TrajectoryTime import TrajectoryTime
from basemodel.SingleLineTransaction import SingleLineTransaction
from util.Utils import Utils


class TrajectoryUseTime(TrajectoryTime, SingleLineTransaction):

    def __init__(self, db_name, mmsi_db_name):
        super(TrajectoryUseTime, self).__init__(db_name, mmsi_db_name)

    def fetch_trajectory_use_time(self, sql, file_name, header):
        self.start_fetch_data_transaction(sql)
        with open(file_name, "wb") as output_file:
            output_writer = csv.writer(output_file)
            output_writer.writerow(header)

            self.single_line_transaction_deal(self.source_db.db_cursor, output_writer)

    def fetch_data(self, data_reader):
        return data_reader.fetchone()

    def deal_situation(self, info, output_saver):
        start_time = info[TrajectoryTime.START_TIME_INDEX]
        arrive_time = info[TrajectoryTime.ARRIVE_TIME_INDEX]
        line_index = info[TrajectoryTime.LINE_INDEX]
        mmsi = info[TrajectoryTime.MMSI_INDEX]
        use_time = Utils.convert_str_time_to_utc(arrive_time) - Utils.convert_str_time_to_utc(start_time)
        source = info[TrajectoryTime.SOURCE_INDEX]
        load_state = info[TrajectoryTime.LOAD_STATE_INDEX]
        ship_static_info = self.fetch_ship_static_info(mmsi)
        deadweight = info[TrajectoryTime.DEADWEIGHT_INDEX]
        output_saver.writerow([line_index, use_time, arrive_time, source, load_state, deadweight] + ship_static_info)

        self.update_ship_level_info(str(mmsi) + "-" + str(deadweight), use_time)


if __name__ == '__main__':
    mmsi_db_name = r"D:\graduation\data\step_result\total\step1\OilTankerTemp.db"
    db_name = r"D:\graduation\data\step_result\total\step4\trajectory.db"
    sql = """
    SELECT *
      FROM trajectory_all
     WHERE vessel_type = 'Crude Oil Tanker' and input_or_output = 'Input'
     ORDER BY line_index;
    """
    trajectory_file = r"D:\graduation\data\step_result\total\analysis\trajectory_analysis\trajectory_use_time_0113.csv"
    trajectory_header = ["line_index", "use_time", "arrive_time", "source_port", "load_state", "deadweight",
                         "flag_country", ]
    use_time_item = TrajectoryUseTime(db_name, mmsi_db_name)
    use_time_item.fetch_trajectory_use_time(sql, trajectory_file, trajectory_header)

    ship_file = r"D:\graduation\data\step_result\total\analysis\trajectory_analysis\ship_use_time_0113.csv"
    ship_header = ["mmsi", "use_time", "deadweight", "flag_country", ]
    use_time_item.export_ship_level_info_to_csv(ship_file, ship_header)
