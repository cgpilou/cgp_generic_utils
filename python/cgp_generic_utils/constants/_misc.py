"""
Constants used to manipulate miscellaneous data
"""

# imports python
import os


class EntityType(object):
    CONTAINER = 'container'
    MODULE = 'module'
    STRUCTURE = 'structure'
    ALL = [CONTAINER, MODULE, STRUCTURE]


class Environment(object):

    # script editor
    SCRIPT_EDITOR = NotImplemented

    # config directory
    CONFIG_DIRECTORY = os.path.join(os.path.expanduser("~"), '.cgpConfigs')

    # icon directory
    ICON_LIBRARY = os.path.join(os.sep.join(os.path.dirname(__file__).split(os.sep)[:-3]), 'icons')


class LogType(object):
    PRINT = 'print'
    INFO = 'info'
    WARNING = 'warning'
    ERROR = 'error'
    ALL = [PRINT, INFO, WARNING, ERROR]


class Orientation(object):
    HORIZONTAL = 'horizontal'
    VERTICAL = 'vertical'
    ALL = [HORIZONTAL, VERTICAL]


class Project(object):
    BASE = 'base'
    CORE_ANIM = 'coreAnim'
    CORE_VFX = 'coreVFX'
    RANCH = 'ranch'
    RIG_LIBRARY = 'facilityPublish'
    ALL = [BASE, CORE_ANIM, CORE_VFX, RANCH, RIG_LIBRARY]


class PublishType(object):
    MODULE = 'rigModule'
    STRUCTURE = 'rigStructure'
    ALL = [MODULE, STRUCTURE]


class SrtAttribute(object):
    SRT = 'SRT'
    SR = 'SR'
    ST = 'ST'
    RT = 'RT'
    S = 'S'
    R = 'R'
    T = 'T'
    ALL = [SRT, SR, ST, RT, S, R, T]


class StatusColor(object):
    ERROR = (0.91, 0.42, 0.42)      # red
    INFO = (0.2, 0.6, 0.8)          # blue
    VALID = (0.23, 0.87, 0.57)      # green
    WARNING = (0.93, 0.78, 0.17)    # yellow
    ALL = [ERROR, INFO, VALID, WARNING]


class TransformMode(object):
    RELATIVE = 'relative'
    ABSOLUTE = 'absolute'
    ALL = [RELATIVE, ABSOLUTE]
