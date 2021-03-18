# -*- encoding: utf -*-
"""
Create on 2020/12/12 16:48
@author: Xiao Yijia
"""

from pyecharts.charts import Bar
from pyecharts.charts import Sankey
from pyecharts import options as opts


class TestEcharts(object):

    def __init__(self):
        pass

    def testBar(self):
        bar = Bar()
        bar.add_xaxis(["衬衫", "毛衣", "领带", "裤子", "风衣", "高跟鞋", "袜子"])
        bar.add_yaxis("商家A", [114, 55, 27, 101, 125, 27, 105])
        bar.add_yaxis("商家B", [57, 134, 137, 129, 145, 60, 49])
        bar.set_global_opts(title_opts=opts.TitleOpts(title="某商场销售情况"))
        bar.render()

    def testSankey(self):
        nodes = [
            {"name": "category1"},
            {"name": "category2"},
            {"name": "category3"},
            {"name": "category4"},
            {"name": "category5"},
            {"name": "category6"},
        ]

        links = [
            {"source": "category1", "target": "category2", "value": 10},
            {"source": "category2", "target": "category3", "value": 15},
            {"source": "category3", "target": "category4", "value": 20},
            {"source": "category5", "target": "category6", "value": 25},
        ]
        c = (
            Sankey()
                .add(
                "sankey",
                nodes,
                links,
                linestyle_opt=opts.LineStyleOpts(opacity=0.2, curve=0.5, color="source"),
                label_opts=opts.LabelOpts(position="right"),
            )
                .set_global_opts(title_opts=opts.TitleOpts(title="Sankey-基本示例"))
                .render("figure_html\sankey_base.html")
        )


if __name__ == '__main__':
    testEcharts = TestEcharts()
    testEcharts.testBar()
    # testEcharts.testSankey()
