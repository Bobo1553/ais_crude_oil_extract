# -*- encoding: utf -*-
"""
Create on 2021/4/19 19:42
@author: Xiao Yijia
"""
import csv
import os

import igraph
import pandas as pd

china_port_dict = {}
# const
CHINA_PORT = ["BASUO", "BAYUQUAN", "BEIHAI", "CHANGZHOU", "CHAOZHOU", "CHIWAN", "DALIAN", "DANDONG", "DONGSHAN",
              "FANG-CHENG", "FUZHOU", "GAOGANG", "GUANGZHOU", "HAIKOU", "HAIMEN", "HUANGPUXINGANG", "HUIZHOU",
              "HULUDAO GANG", "JIANGYIN", "JINZHOU WAN", "LIANYUNGANG", "LONGKOU GANG", "LUSHUN", "NANTONG", "NINGBO",
              "PENGLAI", "QINGDAO GANG", "QINHUANGDAO", "QINZHOU", "QUANZHOU", "RIZHAO", "SANYA", "SHAN T OU",
              "SHANGHAI", "SHEKOU", "SHUI DONG", "TAICANG", "TANGSHAN (JINGTANG)", "TIANJIN XIN GANG", "WEIHAI",
              "WENZHOU", "XIAMEN", "XIUYU", "YANGPU", "YANGZHOU", "YANTAI", "YANTIAN", "ZHANGJIANGANG", "ZHANGZHOU",
              "ZHANJIANG", "ZHAPU", "ZHEN HAI", "ZHOUSHAN", "ZHUHAI"]
CHINA_PORT_INDEX = [1162, 1199, 1302, 1537, 1538, 1539, 1541, 1592, 1675, 1716, 1717, 1721, 1729, 181, 1834, 1849, 1892,
                    192, 196, 2009, 2012, 2029, 2030, 2036, 2037, 2038, 2039, 2069, 2070, 2071, 2072, 2073, 2074, 2075,
                    335, 336, 352, 408, 412, 444, 516, 558, 565, 615, 629, 630, 685, 688, 690, 741, 744, 926, 951, 964]


def communities_cluster(source_port_oil, communities_result, steps):
    """
    analysis:
    衡量划分的好坏：modularity、子图大小和子图结构、
    衡量子图的凝聚性：聚集系数、网络密度、平均最短距离
    :param source_port_oil:
    :param communities_result:
    :return:
    """
    df_data = pd.read_csv(source_port_oil)
    g = igraph.Graph.DataFrame(df_data, directed=True)

    # using walktrap
    # wtrap = g.community_walktrap(weights=g.es["weight"], steps=steps)
    wtrap = g.community_edge_betweenness(weights=g.es["weight"])
    g.community_infomap(edge_weights=g.es["weight"])
    g.community_multilevel(weights=g.es["weight"])
    g.community_fastgreedy(weights=g.es["weight"])
    g.community_leiden(weights=g.es["weight"])
    g.community_leading_eigenvector(weights=g.es["weight"])
    g.community_label_propagation(weights=g.es["weight"])
    clust = wtrap.as_clustering()

    print(clust)
    print(clust.modularity)

    with open(communities_result, "w", newline="") as result_file:
        result_writer = csv.writer(result_file)
        result_writer.writerow(["port_name", "idx"])
        for idx, c in enumerate(clust):
            for port_name in g.vs[c]["name"]:
                result_writer.writerow([port_name, idx])
                if port_name in CHINA_PORT:
                    print("{}:{}".format(port_name, str(idx)))

    # 指标：modularity
    # 子图大小
    # 子图的内部结构和外部联系


def init_china_port(china_port_file_name):
    with open(china_port_file_name) as china_port_file:
        china_port_reader = csv.reader(china_port_file)

        next(china_port_reader)

        for row in china_port_reader:
            china_port_dict[int(row[0])] = row[1]


def combine_centrality(centrality_files_name, save_file_name, save_header):
    centrality_files = []
    centrality_readers = []

    for idx, file_name in enumerate(centrality_files_name):
        centrality_files.append(open(file_name))
        centrality_readers.append(csv.reader(centrality_files[idx]))
        next(centrality_readers[idx])

    with open(save_file_name, "w", newline="") as save_file:
        save_writer = csv.writer(save_file)
        save_writer.writerow(save_header)
        for row in centrality_readers[0]:
            index = int(row[1])
            if index in china_port_dict:
                info = [index, china_port_dict[index]] + row[2:]
                for reader in centrality_readers[1:]:
                    try:
                        other_row = next(reader)
                        info += other_row[2:]
                    except:
                        continue
                save_writer.writerow(info)
            else:
                for reader in centrality_readers[1:]:
                    try:
                        next(reader)
                    except:
                        continue


def export_cluster_result(g, clust, output_file_name):
    print(output_file_name)
    with open(output_file_name, "w", newline="") as all_file:
        all_writer = csv.writer(all_file)
        all_writer.writerow(["port_name", "idx"])

        with open(output_file_name.replace(".csv", "-CN.csv"), "w", newline="") as china_file:
            china_writer = csv.writer(china_file)
            china_writer.writerow(["modularity", clust.modularity])
            china_writer.writerow(["port_name", "idx"])
            for idx, c in enumerate(clust):
                for port_name in g.vs[c]["name"]:
                    all_writer.writerow([port_name, idx])
                    if port_name in CHINA_PORT:
                        china_writer.writerow([port_name, idx])


def edge_cluster(g, output_path):
    print("community_edge_betweenness")
    edgebet = g.community_edge_betweenness(weights=g.es["weight"])
    clust = edgebet.as_clustering()

    export_cluster_result(g, clust, os.path.join(output_path, "edge_betweenness.csv"))


def walktrap_cluster(g, output_path, steps):
    print("community_walktrap")
    wtrap = g.community_walktrap(weights=g.es["weight"], steps=steps)
    clust = wtrap.as_clustering()

    export_cluster_result(g, clust, os.path.join(output_path, "wtrap-{}.csv".format(steps)))


def infomap_cluster(g, output_path, ):
    print("community_infomap")
    clust = g.community_infomap(edge_weights=g.es["weight"])

    export_cluster_result(g, clust, os.path.join(output_path, "infomap.csv"))


def multilevel_cluster(g, output_path, ):
    print("community_multilevel")
    clust = g.community_multilevel(weights=g.es["weight"])

    export_cluster_result(g, clust, os.path.join(output_path, "multilevel.csv"))


def fastgreedy_cluster(g, output_path, ):
    print("community_fastgreedy")
    fastgreedy = g.community_fastgreedy(weights=g.es["weight"])
    clust = fastgreedy.as_clustering()

    export_cluster_result(g, clust, os.path.join(output_path, "fastgreedy.csv"))


def leiden_cluster(g, output_path, ):
    print("community_leiden")
    clust = g.community_leiden(weights=g.es["weight"])

    export_cluster_result(g, clust, os.path.join(output_path, "leiden.csv"))


def leading_eigenvector_cluster(g, output_path, ):
    print("community_leading_eigenvector")
    clust = g.community_leading_eigenvector(weights=g.es["weight"])

    export_cluster_result(g, clust, os.path.join(output_path, "leading_eigenvector.csv"))


def label_propagation_cluster(g, output_path, ):
    print("community_label_propagation")
    clust = g.community_label_propagation(weights=g.es["weight"])

    export_cluster_result(g, clust, os.path.join(output_path, "label_propagation.csv"))


def all_communities_cluster(source_port_oil, communities_path, directed):
    df_data = pd.read_csv(source_port_oil)
    g = igraph.Graph.DataFrame(df_data, directed=directed)

    for i in range(1, 7):
        walktrap_cluster(g, communities_path, i)
    # edge_cluster(g, communities_path)
    infomap_cluster(g, communities_path)
    multilevel_cluster(g, communities_path)
    fastgreedy_cluster(g, communities_path)
    leiden_cluster(g, communities_path)
    leading_eigenvector_cluster(g, communities_path)
    label_propagation_cluster(g, communities_path)


def correct_file(source_file_name, output_file_name):
    with open(source_file_name) as source_file:
        source_reader = csv.reader(source_file)

        with open(output_file_name, "w", newline="") as output_file:
            output_writer = csv.writer(output_file)
            row = next(source_reader)
            output_writer.writerow(row)

            idx = 1
            for row in source_reader:
                while idx != int(row[1]):
                    output_writer.writerow([idx])
                    idx += 1
                output_writer.writerow([idx] + row[1:])
                idx += 1


if __name__ == '__main__':
    # correct_file(r"D:\graduation\data\analysis\chapter5\ship\undirected-centrality\all_closeness_w.csv",
    #              r"D:\graduation\data\analysis\chapter5\ship\undirected-centrality\all_closeness_w_correct.csv")

    china_port_file_name = r"D:\graduation\data\analysis\chapter5\network\china_port_code.csv"
    init_china_port(china_port_file_name)

    in_degree_file_name = r"D:\graduation\data\analysis\chapter5\ship\undirected-centrality\all_degree_w_in.csv"
    out_degree_file_name = r"D:\graduation\data\analysis\chapter5\ship\undirected-centrality\all_degree_w_out.csv"
    betweenness_file_name = r"D:\graduation\data\analysis\chapter5\ship\undirected-centrality\all_betweenness_w.csv"
    closeness_file_name = r"D:\graduation\data\analysis\chapter5\ship\undirected-centrality\all_closeness_w_correct.csv"
    centrality_files_name = [in_degree_file_name, out_degree_file_name, betweenness_file_name, closeness_file_name]
    save_file_name = r"D:\graduation\data\analysis\chapter5\ship\undirected-centrality\all_centrality.csv"
    save_header = ["code", "port", "in_degree", "in_output", "out_degree", "out_output", "betweenness", "closeness",
                   "n_closeness"]
    combine_centrality(centrality_files_name, save_file_name, save_header)