# -*- encoding: utf -*-
"""
Create on 2020/12/14 15:01
@author: Xiao Yijia
"""


class ConstColor(object):
    COLOR_RGB_RAMP = ["89,175,245", "90,111,149", "166,225,252", "246,221,80", "252,153,76", "233,88,85", "108,98,233",
                      "73,112,225", "108,154,231", "34,194,218", "212,235,96", "255,232,141", "255,182,76",
                      "251,110,108", "97,217,172", "0,176,80", "157,187,97", "191,144,0", "217,150,144", "147,58,50",
                      "127,101,159", "127,127,127", "221,215,230", "0,0,0", "196,214,160", "77,77,255", "239,156,196",
                      "204,255,102", "204,0,204"]

    COLOR_HEX_RAMP = ['#59aff5', '#5a6f95', '#a6e1fc', '#f6dd50', '#fc994c', '#e95855', '#6c62e9', '#4970e1', '#6c9ae7',
                      '#22c2da', '#d4eb60', '#ffe88d', '#ffb64c', '#fb6e6c', '#61d9ac', '#00b050', '#9dbb61', '#bf9000',
                      '#d99690', '#933a32', '#7f659f', '#7f7f7f', '#ddd7e6', '#000000', '#c4d6a0', '#4d4dff', '#ef9cc4',
                      '#ccff66', '#cc00cc']

    def __init__(self):
        pass

    @staticmethod
    def convert_rgb_to_hex(color_rgb):
        color_hex = "#"
        color_rgbs = color_rgb.split(",")
        for item in color_rgbs:
            hex_item = hex(int(item))[2:]
            if len(hex_item) == 1:
                hex_item = '0' + hex_item
            color_hex += hex_item

        return color_hex


if __name__ == '__main__':
    COLOR_HEX_RAMP = []
    for color_item in ConstColor.COLOR_RGB_RAMP:
        COLOR_HEX_RAMP.append(ConstColor.convert_rgb_to_hex(color_item))

    print(COLOR_HEX_RAMP)
