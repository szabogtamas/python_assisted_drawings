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

def initialize_fib(n, cycle_limit=100):
    # Return the previous Fibonacci number (only if it is smaller than than first few given by cycle_limit)
    c, d = 0, True
    a, b = 0, 1
    while c < cycle_limit and d:
        c += 1
        a1 = a + 0
        a  = b + 0
        b = a1 + b
        if b >= n:
            d = False
    return a, b

def generate_fibonacci_series(start, length):
    # Return a series of Fibonacci numbers starting from a given number
    a, b = initialize_fib(start)
    l = []
    for i in range(0, length):
        a1 = a + 0
        a  = b + 0
        b = a1 + b
        l.append(a)
        
    return(l)