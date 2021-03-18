# -*- encoding: utf -*-
"""
Create on 2021/1/13 15:01
@author: Xiao Yijia
"""
from abc import abstractmethod


class SingleLineTransaction(object):

    def __init__(self):
        pass

    def single_line_transaction_deal(self, data_reader, output_saver):
        info = self.fetch_data(data_reader)
        while self.has_next_data(info):
            self.deal_situation(info, output_saver)
            info = self.fetch_data(data_reader)

    def fetch_data(self, data_reader):
        return data_reader.next()

    def has_next_data(self, info):
        return info

    def deal_situation(self, info, output_saver):
        return info
