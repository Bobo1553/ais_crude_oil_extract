# -*- encoding: utf -*-
"""
Create on 2020/10/15 10:35
@author: Xiao Yijia
"""

import configparser


class Config:
    # db_config
    source_path = None
    source_table = None
    target_db = None
    target_ais_csv = None

    # ais_config
    ais_table = None
    ais_rol_list = None

    # draft_config
    draft_table = None
    draft_rol_list = None
    draft_state_table = None
    draft_state_rol_list = None

    # data_cleaning_config
    speed_threshold = None
    draft_threshold = None
    is_need_cleaning = None

    # trajectory_config
    trajectory_output_header = None
    trajectory_output_file = None
    china_trajectory_output_file = None
    trajectory_distance_threshold = None
    trajectory_speed_threshold = None
    static_info_file = None
    split_degree = None

    # port_config
    port_name = None
    search_distance = None

    # deadweight_config
    deadweight_table = None
    deadweight_db = None

    def __init__(self):
        pass

    @staticmethod
    def parse_from_file(filename):
        conf = configparser.ConfigParser()
        conf.read(filename, encoding="utf-8")

        Config.parse_db_config(conf)
        Config.parse_ais_config(conf)
        Config.parse_draft_config(conf)
        Config.parse_data_cleaning_config(conf)
        Config.parse_trajectory_config(conf)
        Config.parse_port_config(conf)
        Config.parse_deadweight_config(conf)

    @staticmethod
    def parse_db_config(conf):
        Config.source_path = conf['db']['source_path']
        Config.source_table = conf['db']['source_table']
        Config.target_db = conf['db']['target_db']

    @staticmethod
    def parse_ais_config(conf):
        Config.ais_table = conf['ais']['target_table']
        Config.ais_rol_list = conf['ais']['rol_list'].split("; ")

    @staticmethod
    def parse_draft_config(conf):
        Config.draft_table = conf['draft']['target_table']
        Config.draft_rol_list = conf['draft']['rol_list'].split("; ")
        Config.draft_state_table = conf['draft']['state_table']
        Config.draft_state_rol_list = conf['draft']['state_rol_list'].split("; ")

    @staticmethod
    def parse_data_cleaning_config(conf):
        Config.is_need_cleaning = conf['data_cleaning'].getboolean('is_need_cleaning')
        Config.speed_threshold = int(conf['data_cleaning']['speed_threshold'])
        Config.draft_threshold = int(conf['data_cleaning']['draft_threshold'])

    @staticmethod
    def parse_trajectory_config(conf):
        Config.trajectory_output_header = conf['trajectory']['output_header'].split("; ")
        Config.trajectory_output_file = conf['trajectory']['output_file']
        Config.china_trajectory_output_file = conf['trajectory']['china_output_file']
        Config.trajectory_distance_threshold = float(conf['trajectory']['distance_threshold'])
        Config.trajectory_speed_threshold = int(conf['trajectory']['speed_threshold'])
        Config.static_info_file = conf['trajectory']['static_info_file']
        Config.split_degree = int(conf['trajectory']['split_degree'])

    @staticmethod
    def parse_port_config(conf):
        Config.port_name = conf['port']['port_name']
        Config.search_distance = int(conf['port']['search_distance'])

    @staticmethod
    def parse_deadweight_config(conf):
        Config.deadweight_db = conf['deadweight']['db_name']
        Config.deadweight_table = conf['deadweight']['table_name']
