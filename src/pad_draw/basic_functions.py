import numpy as np
import math
import datetime
from shapely import geometry as sg
from pysolar import solar

def get_sun_features(site_location, shadow_time=(2000, 1, 1, 12, 0)):
    # A wrapper around pysolar to get all important features at once
    time_of_interest = datetime.datetime(*shadow_time, tzinfo=datetime.timezone.utc)
    sun_altitude = solar.get_altitude(site_location[0], site_location[1], time_of_interest)
    sun_azimuth = solar.get_azimuth(site_location[0], site_location[1], time_of_interest)
    return sun_altitude, sun_azimuth

def calculate_shadow_tangent(object_height, sun_altitude):
    # Shortcut to calculate tangent; this will be the length of the shadow
    sun tangent = math.tan(math.radians(sun_altitude))
    return object_height / sun tangent

def rotate_edge(points, origin, angle):
    # Calculate xy coordinates of a point after rotation around another point
    points = complex(*points)
    origin = complex(*origin)
    angle = np.deg2rad(angle)
    r = (points - origin) * np.exp(complex(0, angle)) + origin
    return (r.real, r.imag)