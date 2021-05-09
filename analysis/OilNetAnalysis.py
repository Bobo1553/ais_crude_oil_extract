# -*- encoding: utf -*-
"""
Create on 2021/4/13 9:55
@author: Xiao Yijia
"""

import networkx as nx

from dao.commondb import CommonDB


class OilNetAnalysis(object):

    def __init__(self, ):
        self.oil_graph = nx.Graph()
        self.total_oil = 0

    def fetch_data(self, source_name, sql):
        source_db = CommonDB(source_name)
        source_db.run_sql(sql)

        for row in source_db.db_cursor:
            self.oil_graph.add_nodes_from([row[0], row[1]])
            self.oil_graph.add_weighted_edges_from([(row[0], row[1], int(row[2]))])
            self.total_oil += int(row[2])

    def graph_analysis(self):
        try:
            print("nodes num:{}".format(len(self.oil_graph.nodes)))
            print("edges num:{}".format(len(self.oil_graph.edges)))
            print("total_oil_flow:{}".format(self.total_oil))
            print("density:{}".format(nx.density(self.oil_graph) * 100))
            print("clustering coefficient:{}".format(nx.average_clustering(self.oil_graph, weight="weight") * 1000))
            # print("shortest_path:{}".format(nx.average_shortest_path_length(self.oil_graph, weight="weight")))
        except:
            pass


if __name__ == '__main__':
    #     source_db = r"D:\graduation\data\analysis\chapter5\ship\all\ship_count.db"
    #     sql = """
    #     SELECT *
    #   FROM source_network
    #  WHERE source_network.source IN (
    #            SELECT port_name
    #              FROM [cluster_result]
    #             WHERE idx = '{0}'
    #        )
    # AND
    #        source_network.target IN (
    #            SELECT port_name
    #              FROM [cluster_result]
    #             WHERE idx = '{0}'
    #        );
    #     """
    #
    #     for community_index in range(14):
    #         print(community_index)
    #         community1 = OilNetAnalysis()
    #         community1.fetch_data(source_db, sql.format(community_index))
    #         community1.graph_analysis()

    oil_graph = nx.Graph()
    oil_graph.add_nodes_from(["US", "CN"])
    oil_graph.add_nodes_from(["US", "JP"])
    oil_graph.add_nodes_from(["US", "SM"])
    oil_graph.add_weighted_edges_from([("US", "CN", 5)])
    oil_graph.add_weighted_edges_from([("US", "JP", 5)])
    oil_graph.add_weighted_edges_from([("US", "SN", 5)])
    print(nx.is_directed(oil_graph))
    print(nx.average_shortest_path_length(oil_graph))
