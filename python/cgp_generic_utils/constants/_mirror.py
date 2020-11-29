"""
Constants used to manipulate mirror data
"""


class MirrorMode(object):

    NO_MIRROR = 'noMirror'
    MIRROR = 'mirror'
    NEG_MIRROR = 'negMirror'
    ALL = [NO_MIRROR, MIRROR, NEG_MIRROR]


class MirrorPlane(object):

    XY = 'xy'
    YZ = 'yz'
    XZ = 'xz'
    ALL = [XY, YZ, XZ]
