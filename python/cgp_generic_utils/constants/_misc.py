"""
Constants used to manipulate miscellaneous data
"""

# imports python
import os


class Environment(object):

    GENERIC_UTILS_ROOT = os.sep.join(os.path.dirname(__file__).split(os.sep)[:-3])
    ICON_LIBRARY = os.path.join(GENERIC_UTILS_ROOT, 'icons')
    SCRIPT_EDITOR = 'C:\\Program Files (x86)\\Notepad++\\notepad++.exe'


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


class TransformMode(object):

    RELATIVE = 'relative'
    ABSOLUTE = 'absolute'
    ALL = [RELATIVE, ABSOLUTE]
