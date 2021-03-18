# -*- encoding: utf -*-
"""
Create on 2020/10/16 22:13
@author: Xiao Yijia
"""
import csv
import datetime
import math
import os
import time


class Utils(object):
    # line_index const value
    mmsi_index = 0
    mark_index = 1
    imo_index = 2
    vessel_name_index = 3
    vessel_type_index = 4
    length_index = 5
    width_index = 6
    longitude_index = 7
    latitude_index = 8
    utc_index = 11
    source_port_index = 12
    target_port_index = 13
    load_state_index = 14
    line_index_index = 15
    input_or_output_index = 16

    @staticmethod
    def parse_filter_query(filter_list, connect_word):
        filter_query = []

        for filter_condition in filter_list:
            filter_query.append(filter_condition)
            filter_query.append(connect_word)

        return " ".join(filter_query)[:-len(connect_word)]

    @staticmethod
    def compare_mmsi(after_ship, draft_dict):
        mmsi_compare_result = after_ship.mmsi - draft_dict.mmsi
        if mmsi_compare_result != 0:
            return mmsi_compare_result
        return after_ship.mark - draft_dict.mark

    @staticmethod
    def export_to_csv(datas, csv_writer, append_info=None):
        if append_info is None:
            append_info = []

        for data in datas:
            csv_writer.writerow(data.export_to_csv() + append_info)

    @staticmethod
    def extract_country_trajectories(port_service, source_file, target_file, target_header, country_name):
        with open(source_file) as total_trajectory:
            total_trajectory_reader = csv.reader(total_trajectory)
            next(total_trajectory_reader)
            before_line = total_trajectory_reader.next()

            source_status = True if port_service.get_port_by_name(
                before_line[Utils.source_port_index]).country in country_name else False
            target_status = True if port_service.get_port_by_name(
                before_line[Utils.target_port_index]).country in country_name else False

            with open(target_file, 'wb') as china_trajectory:
                china_trajectory_writer = csv.writer(china_trajectory)

                china_trajectory_writer.writerow(target_header)
                for line in total_trajectory_reader:
                    if source_status and target_status:
                        china_trajectory_writer.writerow(before_line + ['Both'])
                    elif source_status:
                        china_trajectory_writer.writerow(before_line + ['Output'])
                    elif target_status:
                        china_trajectory_writer.writerow(before_line + ['Input'])

                    if line[Utils.line_index_index] != before_line[Utils.line_index_index]:
                        source_status = True if port_service.get_port_by_name(
                            line[Utils.source_port_index]).country in country_name else False
                        target_status = True if port_service.get_port_by_name(
                            line[Utils.target_port_index]).country in country_name else False

                    before_line = line

                if source_status and target_status:
                    china_trajectory_writer.writerow(before_line + ['Both'])
                elif source_status:
                    china_trajectory_writer.writerow(before_line + ['Output'])
                elif target_status:
                    china_trajectory_writer.writerow(before_line + ['Input'])

    @staticmethod
    def temp_extract_country_trajectories(port_service, source_file, target_file, target_header, country_name):
        line_index = 0
        with open(source_file) as total_trajectory:
            total_trajectory_reader = csv.reader(total_trajectory)
            next(total_trajectory_reader)
            before_line = total_trajectory_reader.next()

            source_status = True if port_service.get_port_by_name(
                before_line[Utils.source_port_index]).country in country_name else False
            target_status = True if port_service.get_port_by_name(
                before_line[Utils.target_port_index]).country in country_name else False

            with open(target_file, 'wb') as china_trajectory:
                china_trajectory_writer = csv.writer(china_trajectory)

                china_trajectory_writer.writerow(target_header)
                for line in total_trajectory_reader:
                    if source_status and target_status:
                        china_trajectory_writer.writerow(before_line + [line_index, 'Both'])
                    elif source_status:
                        china_trajectory_writer.writerow(before_line + [line_index, 'Output'])
                    elif target_status:
                        china_trajectory_writer.writerow(before_line + [line_index, 'Input'])

                    if line[Utils.load_state_index] != before_line[Utils.load_state_index] or \
                            line[Utils.mmsi_index] != before_line[Utils.mmsi_index]:
                        source_status = True if port_service.get_port_by_name(
                            line[Utils.source_port_index]).country in country_name else False
                        target_status = True if port_service.get_port_by_name(
                            line[Utils.target_port_index]).country in country_name else False
                        line_index += 1

                    before_line = line

                if source_status and target_status:
                    china_trajectory_writer.writerow(before_line + [line_index, 'Both'])
                elif source_status:
                    china_trajectory_writer.writerow(before_line + [line_index, 'Output'])
                elif target_status:
                    china_trajectory_writer.writerow(before_line + [line_index, 'Input'])

    @staticmethod
    def convert_csv_to_format_txt(source_file_name, target_file_name, port_service, degree_threshold):
        # line_index const value

        with open(source_file_name) as source_file:
            source_reader = csv.reader(source_file)
            next(source_reader)
            before_line = source_reader.next()

            with open(target_file_name, 'w') as target_file:
                target_file.write("Polyline\n")

                total_index = 0
                target_file.write("{} 0\n".format(total_index))
                source_port = port_service.get_port_by_name(before_line[Utils.source_port_index])
                target_file.write('{} {} {} 1.#QNAN 1.#QNAN\n'.format(0, source_port.get_x(), source_port.get_y()))
                point_index = 1
                total_index += 1

                for line in source_reader:

                    target_file.write(
                        "{} {} {} 1.#QNAN 1.#QNAN\n".format(point_index, before_line[Utils.longitude_index],
                                                            before_line[Utils.latitude_index]))
                    point_index += 1

                    # 新的轨迹了
                    if line[Utils.line_index_index] != before_line[Utils.line_index_index]:
                        target_port = port_service.get_port_by_name(before_line[Utils.target_port_index])
                        target_file.write(
                            '{} {} {} 1.#QNAN 1.#QNAN\n'.format(point_index, target_port.get_x(), target_port.get_y()))

                        target_file.write("{} 0\n".format(total_index))
                        source_port = port_service.get_port_by_name(line[Utils.source_port_index])
                        target_file.write(
                            '{} {} {} 1.#QNAN 1.#QNAN\n'.format(0, source_port.get_x(), source_port.get_y()))

                        point_index = 1
                        total_index += 1

                    if math.fabs(float(line[Utils.longitude_index]) - float(
                            before_line[Utils.longitude_index])) > degree_threshold:
                        target_file.write("{} 0\n".format(total_index))
                        point_index = 1
                        total_index += 1

                    before_line = line

                target_file.write("{} {} {} 1.#QNAN 1.#QNAN\n".format(point_index, before_line[Utils.longitude_index],
                                                                      before_line[Utils.latitude_index]))
                point_index += 1
                target_port = port_service.get_port_by_name(before_line[Utils.target_port_index])
                target_file.write(
                    '{} {} {} 1.#QNAN 1.#QNAN\n'.format(point_index, target_port.get_x(), target_port.get_y()))
                target_file.write('END\n')

    @staticmethod
    def convert_str_time_to_utc(str_time):
        """
        convert date in string type to utc time
        :param str_time: date in string type, like '19960403112010'
        :return: the time in int type
        """
        str_time = str(str_time)
        if len(str_time) != 14:
            return int(str_time)

        date = datetime.datetime(int(str_time[0:4]), int(str_time[4:6]), int(str_time[6:8]),
                                 int(str_time[8:10]), int(str_time[10:12]), int(str_time[12:14]))
        utc_time = int(time.mktime(date.timetuple()))
        return utc_time

    @staticmethod
    def convert_str_to_bool(str_bool):
        return True if str_bool.lower() == 'true' else False

    @staticmethod
    def split_china_trajectory_file(file_name, start_line_num, end_line_num):
        with open(file_name) as input_file:
            csv_reader = csv.reader(input_file)

            with open(file_name.replace(".csv", "_{}_{}.csv".format(start_line_num, end_line_num)), 'w') as output_file:
                csv_writer = csv.writer(output_file)

                row = csv_reader.next()

                csv_writer.writerow(row)

                for row in csv_reader:
                    if start_line_num <= int(row[Utils.line_index_index]) < end_line_num:
                        csv_writer.writerow(row)

                    if int(row[Utils.line_index_index]) >= end_line_num:
                        return

    @staticmethod
    def get_trajectory_static_info_file(source_file_name, ships_deadweight, static_info_file_name,
                                        static_info_file_header, degree_threshold):
        static_info_file = open(static_info_file_name, 'wb')
        static_info_file_writer = csv.writer(static_info_file)

        static_info_file_writer.writerow(static_info_file_header)

        with open(source_file_name) as source_file:
            source_reader = csv.reader(source_file)
            next(source_reader)
            before_line = source_reader.next()

            total_index = 0
            start_time = Utils.convert_utc_to_str_time(int(before_line[Utils.utc_index]))
            ship_deadweight = ships_deadweight.get_deadweight_by_mmsi(before_line[Utils.mmsi_index])
            line_before_info = [[total_index, before_line[Utils.mmsi_index], before_line[Utils.mark_index],
                                 before_line[Utils.imo_index], before_line[Utils.vessel_name_index],
                                 before_line[Utils.vessel_type_index], before_line[Utils.length_index],
                                 before_line[Utils.width_index], ship_deadweight]]
            line_after_info = [[before_line[Utils.source_port_index], before_line[Utils.target_port_index],
                                before_line[Utils.load_state_index], before_line[Utils.input_or_output_index]]]
            total_index += 1

            for line in source_reader:

                # 新的轨迹了
                if line[Utils.line_index_index] != before_line[Utils.line_index_index]:
                    arrive_time = Utils.convert_utc_to_str_time(int(before_line[Utils.utc_index]))
                    for i in range(len(line_after_info)):
                        static_info_file_writer.writerow(
                            line_before_info[i] + [start_time, arrive_time] + line_after_info[i])

                    ship_deadweight = ships_deadweight.get_deadweight_by_mmsi(line[Utils.mmsi_index])
                    line_before_info = [[total_index, line[Utils.mmsi_index], line[Utils.mark_index],
                                         line[Utils.imo_index], line[Utils.vessel_name_index],
                                         line[Utils.vessel_type_index], line[Utils.length_index],
                                         line[Utils.width_index], ship_deadweight]]
                    start_time = Utils.convert_utc_to_str_time(int(line[Utils.utc_index]))
                    line_after_info = [[line[Utils.source_port_index], line[Utils.target_port_index],
                                        line[Utils.load_state_index], line[Utils.input_or_output_index]]]

                    total_index += 1

                if math.fabs(float(line[Utils.longitude_index]) - float(
                        before_line[Utils.longitude_index])) > degree_threshold:
                    ship_deadweight = ships_deadweight.get_deadweight_by_mmsi(line[Utils.mmsi_index])
                    line_before_info.append([total_index, line[Utils.mmsi_index], line[Utils.mark_index],
                                             line[Utils.imo_index], line[Utils.vessel_name_index],
                                             line[Utils.vessel_type_index], line[Utils.length_index],
                                             line[Utils.width_index], ship_deadweight])
                    line_after_info.append([line[Utils.source_port_index], line[Utils.target_port_index],
                                            line[Utils.load_state_index], line[Utils.input_or_output_index]])
                    total_index += 1

                before_line = line

            arrive_time = Utils.convert_utc_to_str_time(int(before_line[Utils.utc_index]))
            for i in range(len(line_before_info)):
                static_info_file_writer.writerow(line_before_info[i] + [start_time, arrive_time] + line_after_info[i])

    @staticmethod
    def check_file_path(check_file):
        path, filename = os.path.split(check_file)
        Utils.check_path(path)

    @staticmethod
    def check_path(file_path):
        if not os.path.exists(file_path):
            os.makedirs(file_path)

    @classmethod
    def export_trajectory_static_info_to_csv(cls, before_datas, append_info, after_datas, csv_writer):
        for i in range(len(before_datas)):
            csv_writer.writerow(before_datas[i] + append_info + after_datas[i])

    @staticmethod
    def convert_utc_to_str_time(utc):
        if len(str(utc)) == 14:
            return

        time_local = time.localtime(int(utc))
        return time.strftime("%Y%m%d%H%M%S", time_local)


if __name__ == '__main__':
    print(Utils.convert_utc_to_str_time('1451577604'))
