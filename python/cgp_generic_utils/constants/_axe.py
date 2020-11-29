"""
Constants used to manipulate Axis data
"""


class Axis(object):

    X = 'x'
    Y = 'y'
    Z = 'z'
    ALL = [X, Y, Z]


class AxisTable(object):

    ALL = {'xy': 'z', 'yz': 'x', 'xz': 'y'}
