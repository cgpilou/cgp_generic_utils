"""
Constants used to manipulate naming data
"""

# imports python
import collections


class Lod(object):

    LO = 'lo'
    MI = 'mi'
    HI = 'hi'
    ALL = [LO, MI, HI]


class RigSubType(object):
    AIM = 'AIM'
    BMM = 'BMM'
    FK = 'FK'
    IK = 'IK'
    IKFK = 'IKFK'
    ORIENT = 'ORI'
    PARENT = 'PAR'
    POINT = 'PNT'
    SCALE = 'SCL'
    SPACE_SWITCH = 'SSW'
    SRT = 'SRT'
    STICKY = 'STK'
    SUB = 'SUB'
    ALL = [AIM, BMM, FK, IK, IKFK, ORIENT, PARENT, POINT, SCALE, SPACE_SWITCH, SRT, STICKY, SUB]


class RigType(object):
    BUFFER = 'BUF'
    CONSTRAINT = 'CNS'
    CONTAINER = 'CTN'
    CONVERT_TO_LOCAL_SPACE = 'CTS'
    CONTROLLER = 'CON'
    CURVE = 'CRV'
    EFFECTOR = 'EFF'
    GROUP = 'GRP'
    GUIDE = 'GUD'
    HELPER = 'HLP'
    IK_HANDLE = 'IKH'
    INPUT = 'INP'
    JOINT = 'JNT'
    JOINT_DISPLAY = 'BNE'
    MESH = 'MSH'
    MOCAP = 'MCP'
    MODULE = 'MDU'
    OUT = 'OUT'
    REST = 'RST'
    SURFACE = 'SRF'
    UP_VECTOR = 'UPV'
    ALL = [BUFFER, CONSTRAINT, CONTAINER, CONVERT_TO_LOCAL_SPACE, CONTROLLER, CURVE, EFFECTOR, GROUP, GUIDE, HELPER,
           IK_HANDLE, INPUT, JOINT, JOINT_DISPLAY, MESH, MOCAP, MODULE, OUT, REST, SURFACE, UP_VECTOR]


class Side(object):
    LEFT = 'L'
    RIGHT = 'R'
    MIDDLE = 'M'
    MIRROR = collections.OrderedDict([(LEFT, RIGHT), (MIDDLE, None), (RIGHT, LEFT)])
    ALL = [LEFT, MIDDLE, RIGHT]


class TypoStyle(object):
    BOLD = 'bold'
    ITALIC = 'italic'
    UNDERLINE = 'underline'
    ALL = [BOLD, ITALIC, UNDERLINE]
