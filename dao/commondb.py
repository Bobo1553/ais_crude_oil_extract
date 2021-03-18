# -*- encoding: utf -*-
"""
Create on 2020/10/16 15:33
@author: Xiao Yijia
"""
import os
import sqlite3 as db

from const.ConstSQL import ConstSQL
from util.Utils import Utils


class CommonDB(object):

    # 进行初始化，并且打开数据库
    def __init__(self, db_name):
        self.db_file = db.connect(db_name)
        self.db_cursor = self.db_file.cursor()

    # 最通用的用于执行sql语句
    def run_sql(self, sql):
        self.db_cursor.execute(sql)
        self.db_file.commit()

    # rol_list中保存着这个创建这个表需要的字段名称和字段类型
    def create_table(self, table_name, rol_list):
        query_info = ['CREATE TABLE {}('.format(table_name)]
        for rol in rol_list:
            query_info.append('%s,' % rol)
        sql_info = ''.join(query_info)
        sql_info = sql_info[:-1] + ')'
        self.db_cursor.execute(sql_info)
        self.db_file.commit()

    # 将全部的数据合并导入到一个表格中
    def import_data(self, source_db_name, sql):
        self.db_cursor.execute("ATTACH '{}' AS SourceDB".format(source_db_name))
        self.db_cursor.execute(sql)
        self.db_cursor.execute("DETACH SourceDB")
        self.db_file.commit()

    def delete_data(self, table_name, filter_list, connect_word):
        if not filter_list:
            self.clean_table(table_name)
            return

        filter_query = Utils.parse_filter_query(filter_list, connect_word)

        self.db_cursor.execute('DELETE FROM {} Where {}'.format(table_name, filter_query))
        self.db_file.commit()

    def clean_table(self, table_name):
        self.db_cursor.execute("DELETE FROM {}".format(table_name))
        self.db_file.commit()

    def is_exists(self, table_name):
        table_exists_judge = ("SELECT count(*) FROM sqlite_master WHERE type='table' AND name='{}'".format(table_name))
        table = self.db_cursor.execute(table_exists_judge).fetchone()
        return table[0] != 0

    def drop_table(self, table_name):
        self.db_cursor.execute("DROP TABLE {}".format(table_name))
        self.db_file.commit()
        pass

    # 关闭数据库
    def close_db(self):
        self.db_file.close()

    def import_data_from_path(self, source_path, target_table, rol_list, sql, create_table=True):
        if create_table:
            self.create_table(target_table, rol_list)

        for file_name in os.listdir(source_path):
            if file_name.endswith(".db"):
                print(file_name)
                self.import_data(os.path.join(source_path, file_name), sql)

    def create_new_table(self, target_table, rol_list):
        if self.is_exists(target_table):
            self.drop_table(target_table)

        self.create_table(target_table, rol_list)

    def get_count(self, source_table, count_target='*', filter_list=None, connect_word=''):
        if filter_list is None:
            self.db_cursor.execute("SELECT count({}) FROM {}".format(count_target, source_table))
        else:
            filter_query = Utils.parse_filter_query(filter_list, connect_word)
            self.db_cursor.execute("SELECT count({}) FROM {} WHERE {}".format(count_target, source_table, filter_query))
        row = next(self.db_cursor)
        return row[0]

    def select_ship(self, source_db_name, table_name, ship_type_list, ):
        self.db_cursor.execute("ATTACH '{}' AS SourceDB".format(source_db_name))
        for ship_type in ship_type_list:
            self.db_cursor.execute("INSERT INTO {} SELECT * FROM SourceDB.Tracks WHERE longitude BETWEEN 20 AND 142"
                                  " AND latitude BETWEEN -11 AND 42 AND vessel_type_main = '{}'".format(table_name,
                                                                                                        ship_type))
        self.db_cursor.execute("DETACH SourceDB")
        self.db_file.commit()


if __name__ == '__main__':
    db = CommonDB(r"D:\graduation\data\step_result\total\step7\trajectory.db")
    sql = ConstSQL.FETCH_ALL_SHIP_COUNT_SQL
    db.run_sql(sql)
