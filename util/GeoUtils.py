# -*- encoding: utf -*-
"""
Create on 2020/12/12 20:17
@author: Xiao Yijia
"""

import arcgisscripting


class GeoUtils(object):

    @staticmethod
    def create_shp(txt_file_name, shp_file_name, coordinate_system='#'):
        gp = arcgisscripting.create()
        in_sep = '.'
        gp.CreateFeaturesFromTextFile(txt_file_name, in_sep, shp_file_name, coordinate_system)
