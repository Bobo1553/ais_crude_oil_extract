# -*- encoding: utf -*-
"""
Create on 2021/1/13 15:02
@author: Xiao Yijia
"""


class BetweenLineTransaction(object):

    def __init__(self):
        pass

    def between_line_transaction_deal(self, data_reader, output_saver, ):
        before_info = self.fetch_data(data_reader)

        output_info = self.output_info_init(before_info)

        after_info = self.fetch_data(data_reader)
        while self.has_next_data(after_info):
            if self.judge_first_situation(before_info, after_info):
                output_info = self.deal_first_situation(output_info, after_info, output_saver, )
            elif self.judge_second_situation(before_info, after_info):
                output_info = self.deal_second_situation(output_info, after_info, output_saver, )
            else:
                output_info = self.deal_default_situation(output_info, after_info, output_saver, )

            before_info = after_info
            after_info = self.fetch_data(data_reader)

        self.final_deal_situation(output_info, before_info, output_saver, )

    def fetch_data(self, data_reader):
        return data_reader.next()

    def output_info_init(self, info):
        return info

    def has_next_data(self, info):
        return info

    def judge_first_situation(self, before_info, after_info):
        return False

    def deal_first_situation(self, output_info, info, output_saver):
        return output_info

    def judge_second_situation(self, before_info, after_info):
        return False

    def deal_second_situation(self, output_info, info, output_saver, ):
        return output_info

    def deal_default_situation(self, output_info, info, output_saver):
        return output_info

    def final_deal_situation(self, output_info, info, output_saver):
        pass
