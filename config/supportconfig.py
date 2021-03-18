# -*- encoding: utf -*-
"""
Create on 2020/11/1 10:18
@author: Xiao Yijia
"""
import configparser


class SupportConfig:
    # db config
    source_path = None
    source_table = None
    target_db = None

    # ship config
    ship_table = None
    ship_rol_list = None

    def __init__(self):
        pass

    @staticmethod
    def parse_from_file(filename):
        conf = configparser.ConfigParser()
        conf.read(filename, encoding="utf-8")

        SupportConfig.parse_db_config(conf)
        SupportConfig.parse_ship_config(conf)

    @classmethod
    def parse_db_config(cls, conf):
        SupportConfig.source_path = conf['db']['source_path']
        SupportConfig.source_table = conf['db']['source_table']
        SupportConfig.target_db = conf['db']['target_db']

    @classmethod
    def parse_ship_config(cls, conf):
        SupportConfig.ship_table = conf['ship']['target_table']
        SupportConfig.ship_rol_list = conf['ship']['rol_list'].split("; ")
