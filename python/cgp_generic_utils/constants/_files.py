"""
Constants used to manipulate file data
"""


class FileExtension(object):
    JSON = 'json'
    MA = 'ma'
    MB = 'mb'
    OBJ = 'obj'
    PY = 'py'
    TXT = 'txt'
    UI = 'ui'
    ALL = [JSON, MA, MB, OBJ, PY, TXT, UI]


class FileFilter(object):
    FILE = 'file'
    DIRECTORY = 'directory'
    ALL = [FILE, DIRECTORY]


class PathType(object):
    RELATIVE = 'relative'
    ABSOLUTE = 'absolute'
    ALL = [RELATIVE, ABSOLUTE]
