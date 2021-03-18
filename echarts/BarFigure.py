# -*- encoding: utf -*-
"""
Create on 2020/12/15 10:49
@author: Xiao Yijia
"""
from pyecharts import options as opts
from pyecharts.charts import Bar
from pyecharts.faker import Faker

from const.ConstColor import ConstColor


def test_bar_figure1():
    x, y = Faker.choose(), Faker.values()
    bar = Bar()
    bar.add_xaxis(x)
    bar.add_yaxis("商家A", y, )
    print(bar.options.get("legend"))
    print(bar.options.get("series"))
    bar.add_yaxis("商家B", Faker.values(), )
    # bar.set_global_opts(title_opts=opts.TitleOpts(title="Bar-MarkPoint（自定义）"), )
    # bar.set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    print(bar.options.get("legend"))
    print(bar.options.get("series"))
    bar.options.get("legend")[0].get("data").append("aaa")
    bar.options.get("legend")[0].get("selected").update({"aaa": True})
    print(bar.options.get("legend"))
    bar.render()


class BarFigure(object):

    def __init__(self, top=10):
        self.x_axis = []
        self.y_input_sets = []
        self.y_output_sets = []
        self.y_axiss = []

        self.countrys_color = {}
        self.color_index = 0
        self.top = top

    def show_year_different_figure(self, figure_name, title):
        self.init_ship_deadweight_datas()
        self.show_bar_figure(figure_name, title)

    def show_bar_figure(self, figure_name, title):
        bar = Bar(init_opts=opts.InitOpts(bg_color='white'))
        bar.add_xaxis(self.x_axis)
        for y_set in self.y_input_sets:
            self.format_yaxis(y_set)
        # for y_set in self.y_output_sets:
        #     self.format_yaxis(y_set, self.top, -1, 1)
        for idx, y_axis in enumerate(self.y_axiss[:self.top]):
            bar.add_yaxis("", y_axis, gap="0", stack="stack{}".format(idx))
        # for idx, y_axis in enumerate(self.y_axiss[self.top:]):
        #     bar.add_yaxis("", y_axis, gap="0", stack="stack{}".format(idx))
        bar.set_global_opts(title_opts=opts.TitleOpts(title=title, pos_left="center"), )
        bar.set_series_opts(label_opts=opts.LabelOpts(is_show=False), )
        bar.render(figure_name)

    def init_ship_deadweight_datas(self):
        self.x_axis = ['General Tanker', 'Panamax Tanker', 'Aframax Tanker', 'Suezmax Tanker', 'Very large Tanker']
        # 进口石油的载重吨
        self.y_input_sets = [
            {'KR': 4708311, 'JP': 1670704, 'SG': 1185608, 'RU': 969683, 'TW': 957468, 'HK': 752297, 'MY': 746799,
             'ID': 631923, 'MO': 483654, 'IN': 450379, },
            {'SG': 1362913, 'KR': 1299369, 'HK': 867296, 'MY': 791404, 'SA': 509282, 'TW': 509145, 'ID': 502432,
             'MO': 424687, 'JP': 364238, 'NL': 296852, },
            {'RU': 47400293, 'MY': 20590436, 'SG': 10903797, 'KR': 9893507, 'ID': 9638564, 'AU': 8816915, 'VN': 3912938,
             'SD': 3783416, 'HK': 3044809, 'AE': 2794951, },
            {'SD': 10279241, 'BR': 7846770, 'EG': 5615162, 'MY': 5350152, 'CW': 4563651, 'RU': 4295805, 'SG': 3495814,
             'AO': 3289786, 'ID': 2523941, 'LK': 2512642, },
            {'AO': 127470544, 'SA': 112488183, 'OM': 84515229, 'IR': 79494841, 'IQ': 77457087, 'AE': 48557994,
             'KW': 40676206, 'VE': 39484253, 'BR': 24785499, 'QA': 22306009, },
        ]

        # # 进口石油的船次
        # self.y_input_sets = [
        #     {'KR': 117, 'SG': 55, 'JP': 34, 'IR': 33, 'TW': 24, 'MY': 23, 'RU': 23, 'ID': 19, 'HK': 15, 'IN': 15, },
        #     {'SG': 19, 'KR': 18, 'HK': 12, 'MY': 11, 'ID': 7, 'SA': 7, 'TW': 7, 'MO': 6, 'JP': 5, 'AE': 4, },
        #     {'RU': 430, 'MY': 190, 'SG': 101, 'KR': 90, 'ID': 89, 'AU': 80, 'VN': 36, 'SD': 35, 'HK': 28, 'AE': 26, },
        #     {'SD': 66, 'BR': 50, 'EG': 36, 'MY': 34, 'CW': 29, 'RU': 27, 'SG': 22, 'AO': 21, 'ID': 16, 'LK': 16, },
        #     {'AO': 414, 'SA': 366, 'OM': 276, 'IR': 259, 'IQ': 252, 'AE': 159, 'KW': 129, 'VE': 126, 'BR': 80,
        #      'QA': 73, },
        # ]

        # # 来往中国的船次分析
        # self.y_input_sets = [
        #     {'KR': 147, 'SG': 77, 'HK': 73, 'TW': 72, 'JP': 62, 'ID': 33, 'IR': 33, 'MO': 32, 'MY': 27, 'RU': 25, },
        #     {'KR': 37, 'HK': 33, 'MO': 30, 'SG': 21, 'JP': 17, 'TW': 15, 'MY': 12, 'ID': 10, 'SA': 7, 'US': 6, },
        #     {'RU': 432, 'MY': 194, 'KR': 126, 'SG': 104, 'ID': 93, 'AU': 82, 'JP': 50, 'HK': 41, 'VN': 41, 'SD': 35, },
        #     {'SD': 66, 'BR': 51, 'EG': 36, 'MY': 35, 'CW': 29, 'RU': 27, 'SG': 24, 'AO': 21, 'ID': 16, 'LK': 16, },
        #     {'AO': 414, 'SA': 366, 'OM': 276, 'IR': 259, 'IQ': 252, 'AE': 159, 'KW': 129, 'VE': 126, 'BR': 80,
        #      'QA': 73, },
        # ]

        self.y_output_sets = [
            {'SG': 126, 'KR': 121, 'HK': 61, 'TW': 60, 'JP': 49, 'MY': 37, 'IR': 36, 'MO': 35, 'RU': 24, 'ID': 19, },
            {'SG': 36, 'HK': 33, 'MO': 31, 'KR': 26, 'MY': 15, 'IN': 12, 'JP': 12, 'TW': 12, 'AE': 9, 'ID': 9, },
            {'RU': 416, 'MY': 169, 'SG': 128, 'KR': 116, 'ID': 110, 'HK': 65, 'JP': 58, 'AE': 55, 'BN': 45, 'VN': 42, },
            {'IQ': 92, 'IR': 72, 'SA': 49, 'AE': 45, 'SD': 33, 'AO': 32, 'NG': 26, 'MY': 24, 'QA': 23, 'ID': 18, },
            {'SA': 644, 'IQ': 357, 'IR': 342, 'AO': 326, 'AE': 239, 'OM': 216, 'KW': 213, 'QA': 123, 'NG': 51,
             'MY': 46, },
        ]

    def init_datas(self):
        self.x_axis = ['2014年', '2015年', '2016年', '2017年']
        self.y_input_sets = [
            {'SA': 87, 'AO': 85, 'OM': 66, 'KR': 54, 'IR': 50, 'HK': 46, 'MY': 44, 'RU': 44, 'ID': 40, 'JP': 39, },
            {'RU': 132, 'AO': 106, 'SA': 97, 'IR': 87, 'KR': 82, 'MY': 74, 'OM': 74, 'AE': 62, 'IQ': 61, 'SG': 58, },
            {'RU': 174, 'SA': 125, 'AO': 119, 'OM': 105, 'IR': 92, 'IQ': 88, 'KR': 86, 'MY': 69, 'SG': 65, 'AE': 64, },
            {'RU': 141, 'MY': 129, 'AO': 125, 'KR': 125, 'IR': 86, 'SA': 83, 'SG': 78, 'ID': 75, 'IQ': 73, 'OM': 59, },
        ]

        self.y_output_sets = [
            {'SA': 176, 'IQ': 83, 'AE': 80, 'AO': 68, 'IR': 67, 'OM': 60, 'KR': 58, 'SG': 56, 'RU': 55, 'MY': 53, },
            {'SA': 187, 'IR': 127, 'RU': 116, 'IQ': 108, 'AO': 97, 'AE': 90, 'KR': 72, 'SG': 69, 'MY': 66, 'KW': 60, },
            {'SA': 206, 'RU': 158, 'IQ': 151, 'IR': 132, 'SG': 99, 'AE': 98, 'AO': 89, 'MY': 82, 'KR': 81, 'KW': 74, },
            {'SA': 151, 'IR': 136, 'RU': 136, 'IQ': 112, 'AO': 110, 'SG': 107, 'AE': 93, 'MY': 90, 'KR': 81,
             'ID': 62, },
        ]

    def format_yaxis(self, y_set, offset=0, sign=1, opacity: float = 1):
        while len(self.y_axiss) < len(y_set) + offset:
            self.y_axiss.append([])
        for idx, item in enumerate(y_set.items()):
            country, value = item
            color = self.get_country_color(country)
            self.y_axiss[idx + offset].append(
                opts.BarItem(name=country, value=value * sign,
                             itemstyle_opts=opts.ItemStyleOpts(color=color, opacity=opacity))
            )

    def get_country_color(self, country_name):
        if country_name not in self.countrys_color:
            self.countrys_color[country_name] = ConstColor.COLOR_HEX_RAMP[self.color_index]
            self.color_index += 1
            self.color_index = self.color_index % (len(ConstColor.COLOR_HEX_RAMP))

        return self.countrys_color[country_name]


bar = Bar()
bar.options.get("legend")[0].get("data").append("aaa")

if __name__ == '__main__':
    figure_name = "figure_html/input_deadweight_size_compare.html"
    title = "分船舶大小的中国石油进口统计分析"

    bar_figure = BarFigure()
    bar_figure.show_year_different_figure(figure_name, title)
    # test_bar_figure1()
