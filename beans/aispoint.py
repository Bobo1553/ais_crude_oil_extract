# -*- encoding: utf -*-
"""
Create on 2020/10/25 22:52
@author: Xiao Yijia
"""
import math

from util.Utils import Utils


class AISPoint(object):

    def __init__(self, mmsi, imo, vessel_name, vessel_type, length, width, country, longitude, latitude, draft, speed,
                 str_time, mark=0):
        self.mmsi = mmsi
        self.mark = mark
        self.imo = imo
        if vessel_name is not None:
            self.vessel_name = vessel_name.rstrip()
        else:
            self.vessel_name = None
        self.vessel_type = vessel_type
        self.length = length
        self.width = width
        self.country = country
        self.longitude = longitude
        self.latitude = latitude
        self.draft = draft
        self.speed = speed
        self.date = Utils.convert_utc_to_str_time(str(str_time))
        self.utc = Utils.convert_str_time_to_utc(str(str_time))

    def export_to_csv(self):
        return [self.mmsi, self.mark, self.imo, self.vessel_name, self.vessel_type, self.length, self.width,
                self.country, self.longitude, self.latitude, self.draft, self.speed, self.date, self.utc]

    def is_same_ship(self, another_ship_point):
        return self.mmsi == another_ship_point.mmsi and self.mark == another_ship_point.mark

    def __str__(self):
        return ("mmsi:{},mark:{},imo:{},vessel_name:{},vessel_type:{},length:{},width:{},country:{},longitude:{},"
                "latitude:{},draft:{},speed:{},date:{},utc:{}".
                format(self.mmsi, self.mark, self.imo, self.vessel_name, self.vessel_type, self.length, self.width,
                       self.country, self.longitude, self.latitude, self.draft, self.speed, self.date, self.utc))

    def get_average_speed_between(self, another_ship, distance_threshold):
        distance = 6378.138 * 2 * math.asin(math.sqrt(
            math.pow(math.sin(math.radians(self.latitude - another_ship.latitude) / 2), 2) + math.cos(
                math.radians(self.latitude)) * math.cos(math.radians(another_ship.latitude)) * pow(
                math.sin(math.radians(self.longitude - another_ship.longitude) / 2), 2)))
        if distance < distance_threshold:
            return 0
        speed = distance / (math.fabs(self.utc - another_ship.utc))
        speed = speed * 3600 / 1.852
        return speed

    def set_mark(self, mark):
        self.mark = mark
