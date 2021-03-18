# -*- encoding: utf -*-
"""
Create on 2020/10/24 23:11
@author: Xiao Yijia
"""
from beans.draft import Draft
from beans.kmeans import Kmeans
from const.const import Const


class KmeansService(object):

    def __init__(self, datas, compare_key, weight_key, mark_key):
        self.full_load = Kmeans(datas[int(len(datas) / 2)].__getattribute__(compare_key))
        self.empty_load = Kmeans(datas[int(len(datas) / 2) - 1].__getattribute__(compare_key))
        self.datas = sorted(datas, key=lambda x: x.__getattribute__(compare_key))
        self.compare_key = compare_key
        self.weight_key = weight_key
        self.mark_key = mark_key
        return

    def k_means_calculate(self):
        # 如果吃水数据数量少于等于1个的话，退出
        if len(self.datas) <= 1:
            return Const.FAIL

        while self.full_load.judge_change() and self.empty_load.judge_change():

            self.full_load.clear_data()
            self.empty_load.clear_data()

            for data in self.datas:
                if self.full_load.center_value - data.__getattribute__(self.compare_key) <= \
                        data.__getattribute__(self.compare_key) - self.empty_load.center_value:
                    self.full_load.add_data(data)
                else:
                    self.empty_load.add_data(data)

            self.full_load.update_draught_center(self.compare_key, self.weight_key)
            self.empty_load.update_draught_center(self.compare_key, self.weight_key)

        self.full_load.set_state(Const.FULL_STATE, self.mark_key)
        self.empty_load.set_state(Const.EMPTY_STATE, self.mark_key)

        return Const.SUCCESS


if __name__ == '__main__':
    data_list = [
        Draft('aaa', 5, 3),
        Draft('aaa', 7, 3),
        Draft('aaa', 3, 5),
        Draft('aaa', 1, 4),
        Draft('aaa', 8, 1),
    ]

    kmeans_service = KmeansService(data_list, 'draft', 'count', 'load_state')
    print(kmeans_service.k_means_calculate())
    for data in data_list:
        print(data)