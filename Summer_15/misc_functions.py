import pyqtree
import csv
import math
from math import sin, cos, sqrt, atan2,radians,asin
import sys
import numpy as np

def loadCities():
    citys = []
    with open('citylist.csv', 'rb') as csvfile:
        citysCsv = csv.reader(csvfile, delimiter=',', quotechar='"')
        for city in citysCsv:
            citys.append({"Name":city[0],"Country":city[1],"lat":city[2],"lon":city[3]})
    return citys

def midPoint(lat1, lon1, lat2, lon2):
    """
    Calculate the midpoint between two coordinate points
    """

    # phi = 90 - latitude
    lat1 = deg2rad(lat1)
    lat2 = deg2rad(lat2)

    # theta = longitude
    lon1 = deg2rad(lon1)
    lon2 = deg2rad(lon2)

    X1 = cos(lat1) * cos(lon1)
    Y1 = cos(lat1) * sin(lon1)
    Z1 = sin(lat1)

    X2 = cos(lat1) * cos(lon1)
    Y2 = cos(lat1) * sin(lon1)
    Z2 = sin(lat1)

    X = (X1+X2) / 2
    Y = (Y1+Y2) / 2
    Z = (Z1+Z2) / 2

    Lon = atan2(Y, X)
    Hyp = sqrt(X * X + Y * Y)
    Lat = atan2(Z, Hyp)

    lat = Lat * 180/math.pi
    lon = Lon * 180/math.pi

    return[lat,lon]


def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 3959 # Radius of earth in miles. Use 6371  for kilometers
    return c * r

def displace(lat,lng,theta, distance):
    """
    Displace a LatLng theta degrees counterclockwise and some
    meters in that direction.
    Notes:
        http://www.movable-type.co.uk/scripts/latlong.html
        0 DEGREES IS THE VERTICAL Y AXIS! IMPORTANT!
    Args:
        theta:    A number in degrees.
        distance: A number in meters.
    Returns:
        A new LatLng.
    """
    theta = np.float32(theta)

    delta = np.divide(np.float32(distance), np.float32(3959))

    theta = deg2rad(theta)
    lat1 = deg2rad(lat)
    lng1 = deg2rad(lng)

    lat2 = np.arcsin( np.sin(lat1) * np.cos(delta) +
                      np.cos(lat1) * np.sin(delta) * np.cos(theta) )

    lng2 = lng1 + np.arctan2( np.sin(theta) * np.sin(delta) * np.cos(lat1),
                              np.cos(delta) - np.sin(lat1) * np.sin(lat2))

    lng2 = (lng2 + 3 * np.pi) % (2 * np.pi) - np.pi

    return [rad2deg(lat2), rad2deg(lng2)]

def deg2rad(theta):
        return np.divide(np.dot(theta, np.pi), np.float32(180.0))

def rad2deg(theta):
        return np.divide(np.dot(theta, np.float32(180.0)), np.pi)

"""
@public
@method get_bounding_box: Creates a bounding box around a single point that is "half_side_in_miles"
                          away in every cardinal direction.
@param {float}-lat      : latitude
@param {float}-lon      : longitude
@param distance         : distance in miles
@returns {object}       : bounding box
"""
def get_bounding_box(lat, lon, distance):
    assert distance > 0
    assert lat >= -180.0 and lat  <= 180.0
    assert lon >= -180.0 and lon <= 180.0

    lat = math.radians(lat)
    lon = math.radians(lon)

    radius  = 3959
    # Radius of the parallel at given latitude
    parallel_radius = radius*math.cos(lat)

    lat_min = lat - distance/radius
    lat_max = lat + distance/radius
    lon_min = lon - distance/parallel_radius
    lon_max = lon + distance/parallel_radius
    rad2deg = math.degrees

    box = BoundingBox()
    box.lat_min = rad2deg(lat_min)
    box.lon_min = rad2deg(lon_min)
    box.lat_max = rad2deg(lat_max)
    box.lon_max = rad2deg(lon_max)

    return (box)

class BoundingBox(object):
    def __init__(self, *args, **kwargs):
        self.lat_min = None
        self.lon_min = None
        self.lat_max = None
        self.lon_max = None

# Determine if a point is inside a given polygon or not
# Polygon is a list of (x,y) pairs. This function
# returns True or False.  The algorithm is called
# the "Ray Casting Method".
def point_in_poly(self,x,y,poly):

    x = self.lon2canvas(x)
    y = self.lat2canvas(y)
    poly = self.poly2canvas(poly)
    n = len(poly)
    inside = False

    p1x,p1y = poly[0]
    for i in range(n+1):
        p2x,p2y = poly[i % n]
        if y > min(p1y,p2y):
            if y <= max(p1y,p2y):
                if x <= max(p1x,p2x):
                    if p1y != p2y:
                        xints = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                    if p1x == p2x or x <= xints:
                        inside = not inside
        p1x,p1y = p2x,p2y

    return inside
