# -*- encoding: utf -*-
"""
Create on 2020/11/6 22:28
@author: Xiao Yijia
"""
import csv

from service.aisservice import AISService
from util.Utils import Utils

"""
1. identify the ship shared with the same MMSI
2. add the mark attribute

TODO check 
"""


def shared_mmsi_identify(source_db, source_table, speed_threshold, distance_threshold, point_percent, output_ais_csv,
                         output_header):
    """
    identify the situation of the shared MMSI, consider the speed, distance threshold, and delete the the ship which
    point is less than the point_threshold
    :param source_db: the database file of the original data
    :param source_table: the table name of the original data in the database file
    :param speed_threshold: the threshold of speed to identify whether the same ship
    :param distance_threshold: the threshold of distance to identify whether the same ship
    :param point_percent: delete the ship with the point less than the percent threshold
    :param output_ais_csv: the .csv file of the output data
    :param output_header: the header in the .csv file
    :return: None
    """
    Utils.check_file_path(output_ais_csv)

    ais = AISService(source_db)

    result_file = open(output_ais_csv, 'wb')
    csv_writer = csv.writer(result_file)
    csv_writer.writerow(output_header)

    ais.start_fetch_original_data_transaction(source_table)
    while ais.has_next_ais_ship():
        print(ais.ais_point.mmsi)
        ais.same_mmsi_identify(csv_writer, speed_threshold, distance_threshold, point_percent, )

    result_file.close()
    ais.close()

    return


def format_output_ais_csv(output_ais_csv, format_ais_txt):
    output_ais = open(output_ais_csv)
    output_ais_reader = csv.reader(output_ais)
    next(output_ais_reader)

    format_ais = open(format_ais_txt, 'w')
    format_ais.write("Polyline\n")
    line_index = 0
    point_index = 0

    format_ais.write("{} 0\n".format(line_index))
    before_row = next(output_ais_reader)
    format_ais.write("{} {} {} 1.#QNAN 1.#QNAN\n".format(point_index, before_row[7], before_row[8]))

    if 1 > float(before_row[7]) > -1 and 9 > float(before_row[8]) > 8:
        print(before_row)
    line_index += 1
    point_index += 1

    for row in output_ais_reader:
        if row[0] == before_row[0] and row[1] == before_row[1]:
            format_ais.write("{} {} {} 1.#QNAN 1.#QNAN\n".format(point_index, row[7], row[8]))
            if 1 > float(row[7]) > -1 and 9 > float(row[8]) > 8:
                print(row)
            point_index += 1
        else:
            before_row = row
            line_index = 0
            point_index = 0

            format_ais.write("{} 0\n".format(line_index))
            format_ais.write("{} {} {} 1.#QNAN 1.#QNAN\n".format(point_index, row[7], row[8]))

            if 1 > float(row[7]) > -1 and 9 > float(row[8]) > 8:
                print(row)
            line_index += 1
            point_index += 1

    format_ais.write("END\n")


def check_result(output_ais_csv):
    format_ais_txt = output_ais_csv.replace(".csv", ".txt")
    format_output_ais_csv(output_ais_csv, format_ais_txt)

    Utils.create_shp(format_ais_txt, format_ais_txt.replace(".txt", ".shp"))


def check_txt_file(output_ais_csv):
    format_ais_txt = output_ais_csv.replace(".csv", ".txt")

    with open(format_ais_txt) as format_txt:
        # print(format_txt.readline())
        for row in format_txt.readlines():
            infos = row.split(" ")
            if len(infos) < 5:
                continue
            longitude = float(infos[1])
            latitude = float(infos[2])
            if -1 < longitude < 1 and 8 < latitude < 9:
                print(row)


def check_result_count(output_ais_csv):
    with open(output_ais_csv) as output_ais:
        output_ais_reader = csv.reader(output_ais)
        next(output_ais_reader)

        count = 0
        for _ in output_ais_reader:
            count += 1

    print(count)


def check_file(filename):
    with open(filename) as trajectory_file:
        file_reader = csv.reader(trajectory_file)
        with open(filename.replace(".csv", "_test.csv", ), "wb") as test_file:
            test_writer = csv.writer(test_file)
            test_writer.writerow(next(file_reader))
            test_writer.writerow(next(file_reader))
            test_writer.writerow(next(file_reader))
            test_writer.writerow(next(file_reader))
            test_writer.writerow(next(file_reader))
            test_writer.writerow(next(file_reader))
            test_writer.writerow(next(file_reader))
            test_writer.writerow(next(file_reader))
            test_writer.writerow(next(file_reader))


if __name__ == '__main__':
    source_db = r"D:\graduation\data\step_result\step1\CrudeOilTankerTemp.db"
    source_table = "CrudeOilTanker"
    speed_threshold = 18
    distance_threshold = 3.4
    point_percent = 0.1
    output_ais_csv = r"D:\graduation\data\step_result\step2\CrudeOilTanker.csv"
    output_header = ["mmsi", "mark", "imo", "vessel_name", "vessel_type", "length", "width", "country", "longitude",
                     "latitude", "draft", "speed", "date", "utc"]

    shared_mmsi_identify(source_db, source_table, speed_threshold, distance_threshold, point_percent, output_ais_csv,
                         output_header)
    # check_file(output_ais_csv)
    # check_result(output_ais_csv)
    # check_txt_file(output_ais_csv)
    # check_result_count(output_ais_csv)
    print("finish!!!!")
