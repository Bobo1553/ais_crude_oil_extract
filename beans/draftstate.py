# -*- encoding: utf -*-
"""
Create on 2020/10/26 10:51
@author: Xiao Yijia
"""


class DraftState:

    def __init__(self, mmsi, mark, draft=None, load_state=None):
        self.mmsi = mmsi
        self.mark = mark
        if draft is None:
            self.draft_dict = {}
        else:
            self.draft_dict = {draft: load_state}

    def add_draft_state(self, draft, load_state):
        self.draft_dict[draft] = load_state

    def fetch_draft_state(self, draft):
        if draft in self.draft_dict:
            return self.draft_dict[draft]
        print("!!! mmsi:{},mark:{} don't have draft:{}".format(self.mmsi, self.mark, draft))
        return 0

    def __str__(self):
        return str(self.mmsi) + " " + str(self.mark) + " " + self.draft_dict.__str__()
