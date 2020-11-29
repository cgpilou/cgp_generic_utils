"""
file objects and management functions
"""

# imports local
from ._generic import File, Path, Directory
from ._misc import TxtFile, UiFile
from ._python import JsonFile, PyFile
from ._api import createFile, createDirectory, entity, registerFileTypes


# register files
fileTypes = {'txt': TxtFile,
             'ui': UiFile,
             'path': Path,
             'file': File,
             'directory': Directory,
             'py': PyFile,
             'json': JsonFile}

registerFileTypes(fileTypes)


__all__ = ['File', 'Path', 'Directory',
           'TxtFile', 'UiFile',
           'JsonFile', 'PyFile',
           'createFile', 'createDirectory', 'entity', 'registerFileTypes']
