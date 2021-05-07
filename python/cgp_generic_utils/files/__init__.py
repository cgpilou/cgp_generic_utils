"""
file objects and management functions
"""

# imports local
from ._generic import File, Path, Directory
from ._misc import TxtFile, UiFile
from ._python import JsonFile, PklFile, PyFile
from ._api import createFile, createDirectory, entity, registerFileTypes


# register files
fileTypes = {'txt': TxtFile,
             'ui': UiFile,
             'path': Path,
             'file': File,
             'directory': Directory,
             'pkl': PklFile,
             'py': PyFile,
             'json': JsonFile}

registerFileTypes(fileTypes)


__all__ = ['File', 'Path', 'Directory',
           'TxtFile', 'UiFile',
           'JsonFile', 'PklFile', 'PyFile',
           'createFile', 'createDirectory', 'entity', 'registerFileTypes']
