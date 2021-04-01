# -*- encoding: utf -*-
"""
Create on 2020/10/15 11:16
@author: Xiao Yijia
"""
import arcpy

from beans.aispoint import AISPoint
# from config.config import Config
from const.const import Const
from dao.commondb import CommonDB
from util.Utils import Utils


class AISService(object):

    def __init__(self, db_name=''):
        self.ais_db = CommonDB(db_name)
        self.ais_point = None

    def import_data_from_path(self, source_path, source_table, target_table, rol_list, create_table=True,
                              filter_query="WHERE Vessel_type_sub='Crude Oil Tanker'"):
        sql = "INSERT INTO {} SELECT * FROM {} {} GROUP BY MMSI, ts_pos_utc".format(target_table, source_table,
                                                                                    filter_query)
        self.ais_db.import_data_from_path(source_path, target_table, rol_list, sql, create_table)

    # region 数据清洗
    def clean_dirty_data(self, table_name, speed_threshold=None, draft_threshold=None):
        self.clean_mmsi_error_data(table_name)
        self.clean_lack_error_data(table_name)
        if speed_threshold is not None:
            self.clean_speed_error_data(table_name, speed_threshold)
        if draft_threshold is not None:
            self.clean_draft_error_data(table_name, draft_threshold)

    # 剔除掉mmsi错误的数据
    def clean_mmsi_error_data(self, table_name):
        self.ais_db.delete_data(table_name, ["MMSI > 999999999", "MMSI < 100000000"], Const.OR_CONNECT_WORD)

    # 剔除掉属性缺失的数据
    def clean_lack_error_data(self, table_name):
        filter_list = ["speed is null", "draft is null", "longitude is null", "latitude is null", "mmsi is null",
                       "utc is null"]
        self.ais_db.delete_data(table_name, filter_list, Const.OR_CONNECT_WORD)

    # 删除掉速度异常的数据
    def clean_speed_error_data(self, table_name, speed_threshold):
        self.ais_db.delete_data(table_name, ["speed < 0", "speed > {}".format(speed_threshold)], Const.OR_CONNECT_WORD)

    # 删除掉吃水异常的数据
    def clean_draft_error_data(self, table_name, draft_threshold):
        self.ais_db.delete_data(table_name, ["draft <= 0", "draft > {}".format(draft_threshold)], Const.OR_CONNECT_WORD)

    # endregion

    # region 数据获取
    def start_fetch_data_transaction(self, source_table):
        self.ais_db.run_sql("SELECT mmsi, mark, imo, vessel_name, vessel_type, length, width, longitude, latitude, "
                            "draft, speed, utc FROM {} WHERE mmsi = 215153000 ORDER BY mmsi, mark, utc".format(
            source_table))
        row = self.ais_db.db_cursor.next()
        self.ais_point = AISPoint(row[0], row[2], row[3], row[4], row[5], row[6], row[7], row[8], float(row[9]),
                                  row[10], row[11], row[1])
        return self.ais_point

    def start_fetch_original_data_transaction(self, source_table):
        self.ais_db.run_sql("SELECT mmsi, imo, vessel_name, vessel_type_sub, length, width, flag_country, longitude, "
                            "latitude, draft, speed, utc FROM {} ORDER BY mmsi, utc ".format(source_table))
        row = self.ais_db.db_cursor.next()
        self.ais_point = AISPoint(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], float(row[9]),
                                  row[10])
        return self.ais_point

    def has_next_ais_ship(self):
        return self.ais_point is not None

    # endregion

    # region form trajectory
    def form_trajectory(self, draft_dict, static_info_writer, line_index, port_service, port_search_distance_threshold,
                        outliers_distance_threshold, outliers_speed_threshold):
        # init
        is_line_head = True
        before_ship = self.ais_point
        ais_points = []
        load_state = draft_dict.fetch_draft_state(before_ship.draft)
        outliers_count = 0

        for row in self.ais_db.db_cursor:
            after_ship = AISPoint(row[0], row[2], row[3], row[4], row[5], row[6], row[7], row[8], float(row[9]),
                                  row[10], row[11], row[1])
            if is_line_head:
                before_ship, after_ship = self.line_head_outliers_detection(
                    before_ship, after_ship, outliers_distance_threshold, outliers_speed_threshold)
                is_line_head = False

            if len(ais_points) == 0 or ais_points[-1] != before_ship:
                ais_points.append(before_ship)

            if after_ship.is_same_ship(before_ship):
                # 判断是否异常点
                if AISService.is_outliers(after_ship, before_ship, outliers_distance_threshold,
                                          outliers_speed_threshold):
                    outliers_count += 1
                    continue
                if draft_dict.fetch_draft_state(after_ship.draft) != load_state:
                    print(after_ship)
                    if len(ais_points) > 1:
                        AISService.export_trajectory_to_csv(ais_points, load_state, port_service,
                                                            port_search_distance_threshold, static_info_writer,
                                                            line_index)
                        line_index += 1
                    load_state = draft_dict.fetch_draft_state(after_ship.draft)
                    self.ais_point = after_ship
                    ais_points = []
            else:
                AISService.export_trajectory_to_csv(ais_points, load_state, port_service,
                                                    port_search_distance_threshold, static_info_writer, line_index)
                self.ais_point = after_ship
                return line_index + 1, outliers_count

            before_ship = after_ship

        AISService.export_trajectory_to_csv(ais_points, load_state, port_service, port_search_distance_threshold,
                                            static_info_writer,
                                            line_index)

        self.ais_point = None
        return line_index + 1, outliers_count

    def skip_useless_trajectory(self):
        for row in self.ais_db.db_cursor:
            after_ship = AISPoint(row[0], row[2], row[3], row[4], row[5], row[6], row[7], row[8], float(row[9]),
                                  row[10],
                                  row[11], row[1])
            if not after_ship.is_same_ship(self.ais_point):
                self.ais_point = after_ship
                return

        self.ais_point = None
        return

    # endregion

    def close(self):
        self.ais_db.close_db()

    @staticmethod
    def export_trajectory_to_csv(ais_points, load_state, port_service, distance_threshold, csv_writer, line_index):
        if len(ais_points) == 0:
            return

        first_point = ais_points[0]
        source_port = port_service.get_nearest_port(
            arcpy.PointGeometry(arcpy.Point(first_point.longitude, first_point.latitude)),
            distance_threshold)

        last_point = ais_points[-1]
        target_port = port_service.get_nearest_port(
            arcpy.PointGeometry(arcpy.Point(last_point.longitude, last_point.latitude)),
            distance_threshold)

        Utils.export_to_csv(ais_points, csv_writer, [source_port.name, target_port.name, load_state, line_index])

    def line_head_outliers_detection(self, before_ship, after_ship, outliers_distance_threshold,
                                     outliers_speed_threshold):
        if not AISService.is_outliers(after_ship, before_ship, outliers_distance_threshold, outliers_speed_threshold):
            return before_ship, after_ship
        row = next(self.ais_db.db_cursor)
        middle_ship = after_ship
        after_ship = AISPoint(row[0], row[2], row[3], row[4], row[5], row[6], row[7], row[8], float(row[9]), row[10],
                              row[11], row[1])
        if AISService.is_outliers(middle_ship, after_ship, outliers_distance_threshold, outliers_speed_threshold):
            return before_ship, after_ship
        else:
            return middle_ship, after_ship

    def same_mmsi_identify(self, csv_writer, speed_threshold, distance_threshold, point_percent):
        ship_point = 1
        before_ship = self.ais_point
        sequentially = [[before_ship]]

        for row in self.ais_db.db_cursor:
            after_ship = AISPoint(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9],
                                  row[10])

            if after_ship.is_same_ship(before_ship):
                self.sequentially_identify(after_ship, sequentially, speed_threshold, distance_threshold)
                ship_point += 1
            else:
                self.export_final_sequentially(sequentially, csv_writer, point_percent * ship_point)
                self.ais_point = after_ship
                return

            before_ship = after_ship

        self.export_final_sequentially(sequentially, csv_writer, point_percent * ship_point)
        self.ais_point = None
        return

    @staticmethod
    def is_outliers(after_ship, before_ship, outliers_distance_threshold, outliers_speed_threshold):
        average_speed = after_ship.get_average_speed_between(before_ship, outliers_distance_threshold)
        return average_speed > outliers_speed_threshold

    @staticmethod
    def sequentially_identify(ship_point, sequentially, speed_threshold, distance_threshold):
        for i in range(len(sequentially)):
            speed = ship_point.get_average_speed_between(sequentially[i][-1], distance_threshold)
            if speed < speed_threshold:
                sequentially[i].append(ship_point)
                return

        sequentially.append([ship_point])
        return

    @staticmethod
    def export_final_sequentially(sequentially, csv_writer, point_threshold):
        for i in range(len(sequentially)):
            if len(sequentially[i]) < point_threshold:
                continue
            for ship_point in sequentially[i]:
                ship_point.set_mark(i)
                csv_writer.writerow(ship_point.export_to_csv())
