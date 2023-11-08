"""
file management functions
"""

# imports python
import os

# imports local
import cgp_generic_utils.constants


FILE_TYPES = {}


# COMMANDS #


def createDirectory(path):
    """create a directory on the file system

    :param path: the path of the directory to create
    :type path: str

    :return: the created directory
    :rtype: :class:`cgp_generic_utils.files.Directory`
    """

    # return
    return FILE_TYPES['directory'].create(path)


def createFile(path, content=None, **extraData):
    """create a file on the file system

    :param path: the path of the file to create
    :type path: str

    :param content: the content to set into the file
    :type content: any

    :param extraData: the extra data used to create the file
    :type extraData: dict

    :return: the created file
    :rtype: File
    """

    # get extension
    extension = getExtension(path)

    # return
    return FILE_TYPES.get(extension, FILE_TYPES['file']).create(path, content=content, **extraData)


def entity(path):
    """get a file/directory object from the path

    :param path: the path to get the file/directory object from
    :type path: str

    :return: the file/directory object
    :rtype: File or Directory
    """

    # init
    pathObject = FILE_TYPES['path'](path)

    # return if path is directory
    if pathObject.isDirectory():
        return FILE_TYPES['directory'](path)

    # errors
    if not pathObject.isFile():
        raise ValueError('{0} is not an existing File / directory path'.format(path))

    # get the file extension
    ext = getExtension(path)

    # return
    return FILE_TYPES.get(ext, FILE_TYPES['file'])(path)


def getExtension(path):
    """get the extension of the path

    :param path: path of the file to get the extension from
    :type path: str

    :return: the extension of the file
    :rtype: str
    """

    # return
    return os.path.splitext(path)[-1][1:]


def registerFileTypes(fileTypes):
    """register file types to grant file management functions access to the file objects

    :param fileTypes: the types of files to register - ``{extension1: FileObject1, extension2: FileObject2 ...}``
    :type fileTypes: dict
    """

    # execute
    FILE_TYPES.update(fileTypes)
