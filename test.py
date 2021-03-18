# -*- encoding: utf -*-
"""
Create on 2020/10/15 10:36
@author: Xiao Yijia
"""
from dao.commondb import CommonDB

if __name__ == '__main__':
    db_name = r"D:\graduation\data\step_result\total\step1\OilTankerTemp.db"
    table_name = "OilTanker"
    db_file = CommonDB(db_name)

    db_file.run_sql("select * from {} limit 1".format(table_name))

    # row = db_file.db_cursor.fetchone()
    while (lambda x: x == "")(x=db_file.db_cursor.fetchone()):
        print("a")
