"""
Constants used to manipulate miscellaneous data
"""

# imports python
import os


class Environment(object):

    # text editor executable
    TEXT_EDITOR_EXECUTABLE = NotImplemented

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
