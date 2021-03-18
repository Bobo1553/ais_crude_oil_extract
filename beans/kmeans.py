# -*- encoding: utf -*-
"""
Create on 2020/10/25 16:03
@author: Xiao Yijia
"""


class Kmeans(object):

    def __init__(self, value):
        self.center_value = value
        self.old_value = value - 1
        self.states = []

    def add_data(self, k_means_data):
        self.states.append(k_means_data)

    def update_draught_center(self, compare_key, weight_key):
        self.old_value = self.center_value
        self.center_value = 0
        total_weight = 0
        for data in self.states:
            self.center_value += data.__getattribute__(compare_key) * data.__getattribute__(weight_key)
            total_weight += data.count
        self.center_value = self.center_value * 1.0 / total_weight

    def clear_data(self):
        self.states = []

    def judge_change(self):
        return self.center_value != self.old_value

    def set_state(self, state_symbol, mark_key):
        for data in self.states:
            data.__setattr__(mark_key, state_symbol)
