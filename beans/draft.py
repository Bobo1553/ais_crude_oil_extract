# -*- encoding: utf -*-
"""
Create on 2020/10/24 22:09
@author: Xiao Yijia
"""
from const.const import Const


class Draft(object):

    def __init__(self, mmsi, mark, draft, count, load_state=Const.UNDEFINED_STATE):
        self.mmsi = mmsi
        self.mark = mark
        self.draft = draft
        self.count = count
        self.load_state = load_state

    def __str__(self):
        return "{},{},{},{}".format(self.mmsi, self.draft, self.count, self.load_state)


if __name__ == '__main__':
    draft = Draft('aaa', 1, 12, 152)
    print(draft.__getattribute__('mmsi'))
    draft.__setattr__('load_state', Const.FULL_STATE)
    print(draft.load_state)
