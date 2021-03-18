# -*- encoding: utf -*-
"""
Create on 2020/12/12 19:40
@author: Xiao Yijia
"""
from pyecharts.charts import Sankey
from pyecharts import options as opts

from const.ConstColor import ConstColor
from const.ConstSQL import ConstSQL
from dao.commondb import CommonDB


class SankeyFigure(object):
    SOURCE_COUNTRY_INDEX = 0
    TARGET_COUNTRY_INDEX = 1
    VALUE_INDEX = 2
    INPUT_OR_OUTPUT_INDEX = 3

    # LOAD_STATE_INDEX = 1

    def __init__(self, db_name, top, threshold=0):
        self.data_source = CommonDB(db_name)

        self.source_nodes = {}
        self.target_nodes = {}
        self.middle_nodes = {}

        self.format_nodes = []
        self.links = []
        self.nodes_color = {}
        self.color_index = 0

        self.top = top
        self.threshold = threshold

    def show_import_and_export_figure(self, sql, figure_name, title, clean_data=True):
        self.init_nodes_and_links(sql, clean_data)
        self.show_sankey_figure(figure_name, title)

    def init_nodes_and_links(self, sql, clean_data=True):
        if clean_data or self.has_datas():
            self.clean_data()
            self.create_datas(sql)

    def has_datas(self):
        return self.format_nodes != [] and self.links != []

    def create_datas(self, sql):
        self.start_transaction(sql)
        for line in self.data_source.db_cursor:
            self.append_nodes_links_from_line(line)
        self.convert_all_nodes_to_format()

    def start_transaction(self, sql):
        self.data_source.run_sql(sql)

    def append_nodes_links_from_line(self, line):
        source_port, target_port, value, input_or_output = self.parse_line(line)

        if value != 0:
            self.append_nodes(source_port, target_port, value, input_or_output)
            self.append_links(source_port, target_port, value)

    # !!! 图表设置部分
    def show_sankey_figure(self, figure_name, title):
        sankey = Sankey(init_opts=opts.InitOpts(width='600px', height='600px'))
        sankey.add(
            "",
            self.format_nodes,
            self.links,
            levels=[
                opts.SankeyLevelsOpts(
                    depth=0,
                    linestyle_opts=opts.LineStyleOpts(color="source", curve=0.5, opacity=0.6),
                    itemstyle_opts=opts.ItemStyleOpts(border_width=0),
                ),
                opts.SankeyLevelsOpts(
                    depth=1,
                    itemstyle_opts=opts.ItemStyleOpts(border_width=0),
                    linestyle_opts=opts.LineStyleOpts(color="target", curve=0.5, opacity=0.6),
                ),
                opts.SankeyLevelsOpts(
                    depth=2,
                    itemstyle_opts=opts.ItemStyleOpts(border_width=0)
                ),
            ],
            pos_right="13%",
            node_gap=1,
            label_opts=opts.LabelOpts(position="right"),
        )
        sankey.set_global_opts(title_opts=opts.TitleOpts(title=title, pos_left='center'))
        sankey.render("figure_html\{}.html".format(figure_name))

    def convert_all_nodes_to_format(self):
        self.format_nodes = []
        self.convert_nodes_to_format(self.source_nodes)
        self.convert_nodes_to_format(self.middle_nodes)
        self.convert_nodes_to_format(self.target_nodes)

    def clean_data(self):
        self.source_nodes = {}
        self.target_nodes = {}
        self.middle_nodes = {}

        self.format_nodes = []
        self.links = []
        self.nodes_color = {}
        self.color_index = 0

    @staticmethod
    def parse_line(line):
        source_port = line[SankeyFigure.SOURCE_COUNTRY_INDEX]
        target_port = line[SankeyFigure.TARGET_COUNTRY_INDEX]
        input_or_output = line[SankeyFigure.INPUT_OR_OUTPUT_INDEX]
        value = line[SankeyFigure.VALUE_INDEX]

        if input_or_output == 'Input':
            source_port = "source-" + source_port
        elif input_or_output == 'Output':
            target_port = "target-" + target_port

        if value is not None:
            value = int(value)
        else:
            value = 0

        return source_port, target_port, value, input_or_output

    def update_nodes(self, nodes, node, value):
        if node in nodes:
            origin_value = nodes[node]
            value += origin_value

        nodes[node] = value

    def append_format_nodes_judge_by_value(self, node):
        node_name, value = node
        color = self.get_node_color(node_name)

        format_node = {
            "name": node_name,
            "itemStyle": {"color": color},
        }
        if value <= self.threshold:
            format_node["label"] = {"show": False}

        self.format_nodes.append(format_node)

    def get_node_color(self, node_name):
        country_name = node_name.split("-")[-1]
        if country_name not in self.nodes_color:
            self.nodes_color[country_name] = ConstColor.COLOR_HEX_RAMP[self.color_index]
            self.color_index += 1
            self.color_index = self.color_index % (len(ConstColor.COLOR_HEX_RAMP))

        return self.nodes_color[country_name]

    def append_format_nodes(self, node, show_label):
        node_name, value = node
        color = self.get_node_color(node_name)

        format_node = {
            "name": node_name,
            "itemStyle": {"color": color},
            "label": {"show": show_label}
        }

        if show_label and value < self.threshold:
            format_node["label"] = {"show": not show_label}

        self.format_nodes.append(format_node)

    def append_links(self, source_port, target_port, value):
        self.links.append({
            "source": source_port,
            "target": target_port,
            "value": value
        })

    def append_nodes(self, source, target, value, input_or_output):
        if input_or_output == 'Input':
            self.update_nodes(self.source_nodes, source, value)
            self.update_nodes(self.middle_nodes, target, value)
        elif input_or_output == 'Output':
            self.update_nodes(self.middle_nodes, source, value)
            self.update_nodes(self.target_nodes, target, value)

    def convert_nodes_to_format(self, nodes):
        sorted_nodes = sorted(nodes.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
        for ahead_node in sorted_nodes[:self.top]:
            self.append_format_nodes(ahead_node, show_label=True)
        for behind_node in sorted_nodes[self.top:]:
            self.append_format_nodes(behind_node, show_label=False)
        # for node in sorted_nodes:
        #     self.append_format_nodes_judge_by_value(node)


if __name__ == '__main__':
    year = 2017

    db_name = r"D:\graduation\data\step_result\total\step7\trajectory.db"
    sql = ConstSQL.FETCH_YEAR_SHIP_COUNT_SQL.format(year, year + 1)
    figure_name = "china_oil_ship_count_{}".format(year)
    title = "{}年来往于中国的油轮航次统计".format(year)
    threshold = 0
    top = 10

    china_oil = SankeyFigure(db_name, top, threshold)
    china_oil.show_import_and_export_figure(sql, figure_name, title)
