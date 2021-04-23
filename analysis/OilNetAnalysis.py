# -*- encoding: utf -*-
"""
Create on 2021/4/13 9:55
@author: Xiao Yijia
"""

import networkx as nx

# from dao.commondb import CommonDB
#
#
# class OilNetAnalysis(object):
#
#     def __init__(self, ):
#         self.oil_graph = nx.Graph()
#
#     def fetch_data(self, source_name, sql):
#         source_db = CommonDB(source_name)
#         source_db.run_sql(sql)
#
#         for row in source_db.db_cursor:
#             self.oil_graph.add_nodes_from([row[0], row[1]])
#             self.oil_graph.add_weighted_edges_from([(row[0], row[1], row[2])])


if __name__ == '__main__':
    G = nx.DiGraph()
    G.add_nodes_from(["CN", "US"])
    G.add_nodes_from(["CN", "JP"])
    G.add_nodes_from(["CN", "SA"])
    G.add_weighted_edges_from([("CN", "US", 10000)])
    G.add_weighted_edges_from([("JP", "US", 2)])
    G.add_weighted_edges_from([("SA", "US", 6)])
    G.add_weighted_edges_from([("CN", "SA", 1)])
    for u, v, wt in G.edges.data("weight"):
        print(u, v, wt)
    print(list(G.nodes))
    print(list(G.edges))
    G = G.reverse()
    print(G.edges)
    print(G.is_directed())
    print(nx.algorithms.degree_centrality(G))
    print(nx.algorithms.closeness_centrality(G))
    print(nx.algorithms.betweenness_centrality(G))
    # print(nx.algorithms.current_flow_closeness_centrality(G, weight='weight'))
    # print(nx.algorithms.current_flow_closeness_centrality(G, ))
    pass
