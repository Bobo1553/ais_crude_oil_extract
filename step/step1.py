# -*- encoding: utf -*-
"""
Create on 2020/11/6 22:26
@author: Xiao Yijia
"""
from service.aisservice import AISService
from util.Utils import Utils

"""
1. select crude oil tanker from the source data
2. clean the dirty data, including mmsi_error, speed_error, draft error, incomplete data and duplicate data
3. merge the data of 2014 - 2017 into the same database file

TODO check the doing things!
"""


def get_oil_tanker(source_path, source_table, target_db, ais_table, ais_rol_list, create_table=True,
                   is_need_cleaning=False, clean_speed_threshold=0, clean_draft_threshold=0):
    Utils.check_file_path(target_db)

    ais = AISService(target_db)

    # 数据导入
    ais.import_data_from_path(source_path, source_table, ais_table, ais_rol_list, create_table=create_table)

    # 数据清理
    if is_need_cleaning:
        ais.clean_dirty_data(ais_table, clean_speed_threshold, clean_draft_threshold)


if __name__ == '__main__':
    source_path = r"E:\NewShipsDB2017"
    source_table = r"Tracks"

    target_db = r"D:\graduation\data\step_result\total\step1\OilTankerTemp.db"
    ais_table = "OilTanker"
    ais_rol_list = ["mmsi INTEGER", "imo INTEGER", "vessel_name TEXT", "callsign TEXT", "vessel_type TEXT",
                    "vessel_type_code INTEGER", "vessel_type_cargo TEXT", "vessel_class TEXT", "length INTEGER",
                    "width INTEGER", "flag_country TEXT", "flag_code INTEGER", "destination TEXT", "eta INTEGER",
                    "draft DOUBLE", "longitude DOUBLE", "latitude DOUBLE", "speed DOUBLE", "cog DOUBLE", "rot DOUBLE",
                    "heading INTEGER", "nav_status TEXT", "nav_status_code INTEGER", "source TEXT", "utc INTEGER",
                    "ts_static_utc INTEGER", "dt_pos_utc TEXT", "dt_static_utc TEXT", "vessel_type_main TEXT",
                    "vessel_type_sub TEXT"]
    is_need_cleaning = True
    clean_speed_threshold = 40
    clean_draft_threshold = 100
    create_table = False

    get_oil_tanker(source_path, source_table, target_db, ais_table, ais_rol_list, create_table, is_need_cleaning,
                   clean_speed_threshold, clean_draft_threshold)
