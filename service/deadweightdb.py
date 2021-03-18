# -*- encoding: utf -*-
"""
Create on 2020/11/4 10:46
@author: Xiao Yijia
"""
from dao.commondb import CommonDB


class DeadweightDB:

    def __init__(self, db_name):
        self.deadweight_db = CommonDB(db_name)
        self.ships_deadweight = None

    def init_ships_deadweight(self, table_name):
        self.ships_deadweight = {}
        self.deadweight_db.run_sql("SELECT mmsi, deadweight FROM {}".format(table_name))
        for row in self.deadweight_db.db_cursor:
            self.ships_deadweight[str(row[0])] = row[1]

        return self.ships_deadweight

    def get_deadweight_by_mmsi(self, mmsi):
        if mmsi not in self.ships_deadweight:
            print(mmsi)
            return ""

        return self.ships_deadweight[mmsi]