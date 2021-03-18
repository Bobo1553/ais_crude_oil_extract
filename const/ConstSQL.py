# -*- encoding: utf -*-
"""
Create on 2020/12/12 19:58
@author: Xiao Yijia
"""


class ConstSQL:
    FETCH_YEAR_SHIP_COUNT_SQL = """
SELECT source.source_country,
       target.target_country,
       count(),
       input_or_output
  FROM (
           SELECT line_index,
                  input_or_output,
                  country AS source_country
             FROM china_trajectory_cn
                  LEFT JOIN
                  port_info ON china_trajectory_cn.source_port = port_info.PORT_NAME
            WHERE vessel_type_sub = 'Crude Oil Tanker' AND 
                  arrive_time BETWEEN {0}0000000000 AND {1}0000000000 AND 
                  input_or_output = 'Input'
       )
       AS source
       LEFT JOIN
       (
           SELECT line_index,
                  country AS target_country
             FROM china_trajectory_cn
                  LEFT JOIN
                  port_info ON china_trajectory_cn.target_port = port_info.PORT_NAME
       )
       AS target ON source.line_index = target.line_index
 GROUP BY source.source_country,
          target.target_country
UNION
SELECT source.source_country,
       target.target_country,
       count(),
       input_or_output
  FROM (
           SELECT line_index,
                  input_or_output,
                  country AS source_country
             FROM china_trajectory_cn
                  LEFT JOIN
                  port_info ON china_trajectory_cn.source_port = port_info.PORT_NAME
            WHERE vessel_type_sub = 'Crude Oil Tanker' AND 
                  start_time BETWEEN {0}0000000000 AND {1}0000000000 AND 
                  input_or_output = 'Output'
       )
       AS source
       LEFT JOIN
       (
           SELECT line_index,
                  country AS target_country
             FROM china_trajectory_cn
                  LEFT JOIN
                  port_info ON china_trajectory_cn.target_port = port_info.PORT_NAME
       )
       AS target ON source.line_index = target.line_index
 GROUP BY source.source_country,
          target.target_country;
"""

    FETCH_YEAR_TRANSPORT_DEADWEIGHT_SQL = """
SELECT source.source_country,
       target.target_country,
       sum(deadweight),
       input_or_output
  FROM (
           SELECT line_index,
                  input_or_output,
                  deadweight,
                  country AS source_country
             FROM china_trajectory_cn
                  LEFT JOIN
                  port_info ON china_trajectory_cn.source_port = port_info.PORT_NAME
            WHERE load_state = 1 AND 
                  vessel_type_sub = 'Crude Oil Tanker' AND 
                  arrive_time BETWEEN {0}0000000000 AND {1}0000000000 AND 
                  input_or_output = 'Input'
       )
       AS source
       LEFT JOIN
       (
           SELECT line_index,
                  country AS target_country
             FROM china_trajectory_cn
                  LEFT JOIN
                  port_info ON china_trajectory_cn.target_port = port_info.PORT_NAME
       )
       AS target ON source.line_index = target.line_index
 GROUP BY source.source_country,
          target.target_country
UNION
SELECT source.source_country,
       target.target_country,
       sum(deadweight),
       input_or_output
  FROM (
           SELECT line_index,
                  input_or_output,
                  deadweight,
                  country AS source_country
             FROM china_trajectory_cn
                  LEFT JOIN
                  port_info ON china_trajectory_cn.source_port = port_info.PORT_NAME
            WHERE load_state = 1 AND 
                  vessel_type_sub = 'Crude Oil Tanker' AND 
                  start_time BETWEEN {0}0000000000 AND {1}0000000000 AND 
                  input_or_output = 'Output'
       )
       AS source
       LEFT JOIN
       (
           SELECT line_index,
                  country AS target_country
             FROM china_trajectory_cn
                  LEFT JOIN
                  port_info ON china_trajectory_cn.target_port = port_info.PORT_NAME
       )
       AS target ON source.line_index = target.line_index
 GROUP BY source.source_country,
          target.target_country;
 """

    FETCH_ALL_TRANSPORT_DEADWEIGHT_SQL = """
SELECT source.source_country,
       target.target_country,
       sum(deadweight),
       input_or_output
  FROM (
           SELECT line_index,
                  input_or_output,
                  deadweight,
                  country AS source_country
             FROM china_trajectory_cn
                  LEFT JOIN
                  port_info ON china_trajectory_cn.source_port = port_info.PORT_NAME
            WHERE load_state = 1 AND 
                  vessel_type_sub = 'Crude Oil Tanker'
       )
       AS source
       LEFT JOIN
       (
           SELECT line_index,
                  country AS target_country
             FROM china_trajectory_cn
                  LEFT JOIN
                  port_info ON china_trajectory_cn.target_port = port_info.PORT_NAME
            WHERE load_state = 1 AND 
                  vessel_type_sub = 'Crude Oil Tanker'
       )
       AS target ON source.line_index = target.line_index
 WHERE input_or_output != 'Both'
 GROUP BY source.source_country,
          target.target_country;
    """

    FETCH_ALL_SHIP_COUNT_SQL = """
SELECT source.source_country,
       target.target_country,
       count(),
       input_or_output
  FROM (
           SELECT line_index,
                  input_or_output,
                  country AS source_country
             FROM china_trajectory_cn
                  LEFT JOIN
                  port_info ON china_trajectory_cn.source_port = port_info.PORT_NAME
             WHERE vessel_type_sub = 'Crude Oil Tanker'
       )
       AS source
       LEFT JOIN
       (
           SELECT line_index,
                  country AS target_country
             FROM china_trajectory_cn
                  LEFT JOIN
                  port_info ON china_trajectory_cn.target_port = port_info.PORT_NAME
             WHERE vessel_type_sub = 'Crude Oil Tanker'
       )
       AS target ON source.line_index = target.line_index
 WHERE input_or_output != 'Both'
 GROUP BY source.source_country,
          target.target_country;
"""

    FETCH_SHIP_STATIC_INFO = "SELECT flag_country FROM OilTanker WHERE MMSI = {} LIMIT 1"

    def __init__(self):
        pass
