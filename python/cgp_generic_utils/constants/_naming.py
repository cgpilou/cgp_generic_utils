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


class Tag(object):
    BIND_POSE = "rigToModPose"
    IS_SCRIPTED_MODULE = 'isScriptedModule'
    IS_LOCAL_MODULE = 'isLocalModule'
    SCRIPT_CONTENT = 'scriptContent'
    MATCH_GUIDE = 'matchGuide'
    MATCH_MODE = 'matchMode'
    MATCH_PRIORITY = 'matchPriority'
    MOCAP_AIM_OBJECT = 'mocapAimObject'
    MOCAP_AIM_OBJECT_OFFSET = 'mocapAimObjectOffset'
    MOCAP_AIM_VECTOR = 'mocapAimVector'
    MOCAP_ASSOCIATED = 'mocapAssociated'
    MOCAP_NAME = 'mocapName'
    MOCAP_PARENT = 'mocapParent'
    MOCAP_TRANSLATE_OFFSET = 'mocapTranslateOffset'
    MOCAP_ROTATE_OFFSET = 'mocapRotateOffset'
    MOCAP_TRANSLATE_DRIVER = 'mocapTranslateDriver'
    MOCAP_ROTATE_DRIVER = 'mocapRotateDriver'
    MOCAP_TYPE = 'mocapType'
    MOCAP_UP_VECTOR = 'mocapUpVector'
    MOCAP_REF_UP_VECTOR = 'mocapRefUpVector'
    ALL = [BIND_POSE, IS_SCRIPTED_MODULE, IS_LOCAL_MODULE, SCRIPT_CONTENT, MATCH_GUIDE, MATCH_MODE,  MATCH_PRIORITY,
           MOCAP_AIM_OBJECT, MOCAP_AIM_OBJECT_OFFSET, MOCAP_AIM_VECTOR, MOCAP_ASSOCIATED, MOCAP_NAME, MOCAP_PARENT,
           MOCAP_TRANSLATE_OFFSET, MOCAP_ROTATE_OFFSET, MOCAP_TRANSLATE_DRIVER,
           MOCAP_ROTATE_DRIVER, MOCAP_TYPE, MOCAP_UP_VECTOR, MOCAP_REF_UP_VECTOR]


class TypoStyle(object):
    BOLD = 'bold'
    ITALIC = 'italic'
    UNDERLINE = 'underline'
    ALL = [BOLD, ITALIC, UNDERLINE]
