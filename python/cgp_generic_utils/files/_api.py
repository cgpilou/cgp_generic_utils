"""
file management functions
"""

# imports local
import cgp_generic_utils.constants


FILE_TYPES = {}


# COMMANDS #

def createDirectory(path):
    """create a directory on the file system

    :param path: path of the directory to create
    :type path: str

    :return: the created directory
    :rtype: :class:`cgp_generic_utils.files.Directory`
    """

    # return
    return FILE_TYPES['directory'].create(path)


def createFile(path, content=None, **extraData):
    """create a file on the file system

    :param path: path of the file to create
    :type path: str

    :param content: content to set into the created file
    :type content: any

    :param extraData: extra data used to create the file
    :type extraData: dict

    :return: the created file
    :rtype: :class:`cgp_generic_utils.files.File`
    """

    # get extension
    extension = FILE_TYPES['path'](path).extension()

    # return
    return FILE_TYPES.get(extension, FILE_TYPES['file']).create(path, content=content, **extraData)


def entity(path):
    """a file/directory object from a path

    :param path: path of the file/directory to get the entity from
    :type path: str

    :return: the file/directory
    :rtype: :class:`cgp_generic_utils.files.Directory`,
            :class:`cgp_generic_utils.files.File`,
            :class:`cgp_generic_utils.files.JsonFile`,
            :class:`cgp_generic_utils.files.PyFile`,
            :class:`cgp_generic_utils.files.TxtFile`,
            :class:`cgp_generic_utils.files.UiFile`
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
    extension = FILE_TYPES['path'](path).extension()

    # return
    return FILE_TYPES.get(extension, FILE_TYPES['file'])(path)


def registerFileTypes(fileTypes):
    """register file types to grant file management functions access to the file objects

    :param fileTypes: types of files to register - {extension1: FileObject1, extension2: FileObject2 ...}
    :type fileTypes: dict
    """

    # execute
    FILE_TYPES.update(fileTypes)
