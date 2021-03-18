# -*- encoding: utf -*-
"""
Create on 2020/11/6 22:31
@author: Xiao Yijia
"""
from service.draftdb import DraftDB
from util.Utils import Utils


def get_draft_count_and_load_identify(source_db, ais_table, target_db, draft_table, draft_rol_list, draft_state_table,
                                      draft_state_rol_list):
    Utils.check_file_path(target_db)

    draft = DraftDB(target_db)
    draft.import_data(source_db, ais_table, draft_table, draft_rol_list)
    draft.ships_draft_state_identify(draft_table, draft_state_table, draft_state_rol_list)
    return


if __name__ == '__main__':
    source_db = r"D:\graduation\data\step_result\total\step2\OilTanker.db"
    ais_table = "OilTanker"
    target_db = r"D:\graduation\data\step_result\total\step3\TankerDraft.db"
    draft_table = "TankerDraft"
    draft_rol_list = ["mmsi INTEGER", "mark INTEGER", "draft DOUBLE", "count INTEGER"]
    draft_state_table = "TankerDraftState"
    draft_state_rol_list = ["mmsi INTEGER", "mark INTEGER", "draft DOUBLE", "count INTEGER", "load_state INTEGER"]

    get_draft_count_and_load_identify(source_db, ais_table, target_db, draft_table, draft_rol_list, draft_state_table,
                                      draft_state_rol_list)
