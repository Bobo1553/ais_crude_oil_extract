# -*- encoding: utf -*-
"""
Create on 2020/10/30 14:51
@author: Xiao Yijia
"""
import csv
import os

from const.const import Const
from dao.commondb import CommonDB
from util.Utils import Utils


def parse_file_name(file_name):
    return file_name.split("_")[1].split(".")[0]


def get_record_count(source_path, source_table, target_db_name, target_table, target_table_rol_list, ):
    target_db = CommonDB(target_db_name)
    if target_db.is_exists(target_table):
        target_db.drop_table(target_table)
    target_db.create_table(target_table, target_table_rol_list)

    original_count = 0
    tanker_count = 0
    for file_name in os.listdir(source_path):
        if file_name.endswith(".db"):
            print(file_name)
            date = parse_file_name(file_name)
            db = CommonDB(os.path.join(source_path, file_name))
            original_day_count = db.get_count(source_table)
            original_count += original_day_count
            tanker_day_count = db.get_count(source_table,
                                            filter_list=["Vessel_type_sub = 'Crude Oil Tanker'"],
                                            connect_word=Const.OR_CONNECT_WORD)
            tanker_count += tanker_day_count
            target_db.db_file.execute("INSERT INTO {} VALUES (?,?,?)".format(target_table),
                                      (date, original_day_count, tanker_day_count))

    target_db.db_file.commit()
    print("original_count:" + str(original_count))
    print("tanker_count:" + str(tanker_count))


def get_ship_count(source_path, source_table, target_db, ship_table, ship_rol_list, ):
    db = CommonDB(target_db)

    sql = "INSERT INTO {} SELECT DISTINCT MMSI, Vessel_type_sub FROM {}".format(ship_table, source_table)

    db.import_data_from_path(source_path, ship_table, ship_rol_list, sql, )

    db.run_sql("SELECT COUNT(DISTINCT MMSI) FROM {}".format(ship_table))
    original_ship = db.db_cursor.next()[0]

    print("original_ship:" + str(original_ship))

    db.run_sql("SELECT COUNT(DISTINCT MMSI) FROM {} WHERE Vessel_type = 'Crude Oil Tanker'".format(
        ship_table))
    tanker_ship = db.db_cursor.next()[0]

    print("tanker_ship:" + str(tanker_ship))


def show_file_content(file_name):
    with open(file_name) as file:
        csv_reader = csv.reader(file)
        print(next(csv_reader))
        for row in csv_reader:
            if row[14] == '55':
                print(row)
        # while True:
        #     for i in range(10000):
        #         row = next(csv_reader)
        #         print(row)


def get_use_time(db_name, csv_name):
    db_file = CommonDB(db_name)
    db_file.run_sql("SELECT * FROM china_trajectory_cn WHERE load_state = 1 AND input_or_output = 'Input' AND "
                    "vessel_type_sub = 'Crude Oil Tanker' ORDER BY arrive_Time;")

    with open(csv_name, 'wb') as csv_file:
        csv_writer = csv.writer(csv_file)
        for row in db_file.db_cursor:
            use_time = Utils.convert_str_time_to_utc(str(row[10])) - Utils.convert_str_time_to_utc(str(row[9]))
            csv_writer.writerow(list(row) + [use_time])


def get_all_ship_country(source_db, mmsi_db, csv_name):
    result_csv = open(csv_name, 'wb')
    csv_writer = csv.writer(result_csv)
    csv_writer.writerow(['MMSI', 'country'])
    source_db_file = CommonDB(source_db)

    mmsi_db_file = CommonDB(mmsi_db)
    mmsi_db_file.run_sql("""
    SELECT DISTINCT mmsi
  FROM china_trajectory_cn
 WHERE load_state = 1 AND 
       input_or_output = 'Input' AND 
       vessel_type_sub = 'Crude Oil Tanker'
 ORDER BY mmsi;
""")
    for row in mmsi_db_file.db_cursor:
        source_db_file.run_sql("SELECT mmsi, flag_country  FROM OilTanker WHERE mmsi = {} LIMIT 1;".format(row[0]))
        csv_writer.writerow(list(next(source_db_file.db_cursor)))


if __name__ == '__main__':
    # SupportConfig.parse_from_file("config/support_config.yml")
    source_path = r'G:\NewShipsDB2015'
    source_table = 'Tracks'
    target_db_name = r'D:\graduation\data\step_result\support\support.db'
    target_table = 'RecordCount2015'
    target_table_rol_list = ["date TEXT", "original_count INTEGER", "tanker_count INTEGER"]

    get_record_count(source_path, source_table, target_db_name, target_table, target_table_rol_list)

    target_db = r'D:\graduation\data\step_result\support\support.db'
    ship_table = 'MMSIShip2015 '
    ship_rol_list = ['mmsi INTEGER', 'vessel_type TEXT']
    get_ship_count(source_path, source_table, target_db, ship_table, ship_rol_list, )
    # show_file_content(r"D:\graduation\data\result\china_trajectory.csv")

    # get_use_time(r"D:\graduation\data\step_result\total\step7\trajectory.db", r"D:\graduation\data\step_result\total\step7\use_time.csv")

    # get_all_ship_country(r"D:\graduation\data\step_result\total\step1\OilTankerTemp.db",
    #                      r"D:\graduation\data\step_result\total\step7\trajectory.db", r"D:\test.csv")
