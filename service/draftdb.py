# -*- encoding: utf -*-
"""
Create on 2020/10/15 11:26
@author: Xiao Yijia
"""
from beans.draftstate import DraftState
# from config.config import Config
from const.const import Const
from dao.commondb import CommonDB
from beans.draft import Draft
from service.kmeansservice import KmeansService


class DraftDB(object):

    def __init__(self, db_name):
        self.draft_db = CommonDB(db_name)
        self.draft = None

    def import_data(self, source_db, source_table, target_table, rol_list):
        self.draft_db.create_new_table(target_table, rol_list)

        sql = "INSERT INTO {} SELECT mmsi, mark, draft, count() FROM {} GROUP BY mmsi, mark, draft" \
            .format(target_table, source_table)
        self.draft_db.import_data(source_db, sql)

    def insert_data(self, data_list, target_table):
        insert_cursor = self.draft_db.db_file.cursor()
        for data in data_list:
            insert_cursor.execute("INSERT INTO {} VALUES(?,?,?,?,?)".format(target_table),
                                  (data.mmsi, data.mark, data.draft, data.count, data.load_state))
        # self.draft_db.db_file.commit()
        return

    # def export_to_csv(self, data_list, ):

    def single_ship_draft_state_identify(self, data_list, target_table):
        kmeans_service = KmeansService(data_list, 'draft', 'count', 'load_state')
        if kmeans_service.k_means_calculate() == Const.SUCCESS:
            # 输出
            self.insert_data(data_list, target_table)
            pass

    def ships_draft_state_identify(self, source_table, target_table, rol_list):
        self.draft_db.create_new_table(target_table, rol_list)

        self.draft_db.run_sql("SELECT * FROM {} ORDER BY mmsi, mark, draft".format(source_table))
        data_list = []

        for row in self.draft_db.db_cursor:
            if len(data_list) == 0:
                data_list.append(Draft(row[0], row[1], row[2], row[3]))
            elif data_list[0].mmsi == row[0] and data_list[0].mark == row[1]:
                data_list.append(Draft(row[0], row[1], row[2], row[3]))
            else:
                self.single_ship_draft_state_identify(data_list, target_table)
                data_list = [Draft(row[0], row[1], row[2], row[3])]

        # 最后一个的判断
        self.single_ship_draft_state_identify(data_list, target_table)

        self.draft_db.db_file.commit()
        return

    def fetch_draft_state(self):
        draft_dict = DraftState(self.draft.mmsi, self.draft.mark, float(self.draft.draft), self.draft.load_state)

        for row in self.draft_db.db_cursor:
            if row[0] != self.draft.mmsi or row[1] != self.draft.mark:
                self.draft = Draft(row[0], row[1], float(row[2]), row[3], row[4])
                return draft_dict
            else:
                draft_dict.add_draft_state(float(row[2]), row[4])

        self.draft = None
        return draft_dict

    def has_next_draft_state(self):
        return self.draft is not None

    def start_fetch_transaction(self, source_table):
        self.draft_db.run_sql("SELECT * FROM {} ORDER BY mmsi, mark".format(source_table))
        row = self.draft_db.db_cursor.next()
        self.draft = Draft(row[0], row[1], float(row[2]), row[3], row[4])
        return DraftState(-1, -1, -1, -1)

    def close(self):
        self.draft_db.close_db()


if __name__ == '__main__':
    # Config.parse_from_file("../config/config.yml")
    #
    # draft = DraftDB(Config.target_db)
    #
    # draft.import_data(Config.ais_table, Config.draft_table, Config.ais_table, Config.draft_rol_list)
    #
    # draft.ships_draft_state_identify(Config.draft_table, Config.draft_state_table, Config.draft_state_rol_list)
    pass
