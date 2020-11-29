"""
generic file object library
"""

# imports python
import os
import ast
import subprocess
import shutil

# imports local
import cgp_generic_utils.python
import cgp_generic_utils.constants
import cgp_generic_utils.files._api


# GENERIC FILE OBJECTS #


class Path(object):
    """path object that manipulates any kind of entity on the file system
    """

    # INIT #

    def __init__(self, path):
        """Path class initialization

        :param path: path of the entity
        :type path: str
        """

        # init
        self._path = os.path.abspath(path)

    def __eq__(self, path):
        """check if the Path has the same name as the other path

        :param path: path to check with
        :type path: str or :class:`cgp_generic_utils.files.Path`

        :return : ``True`` : the paths are identical - ``False`` : the paths are different
        :rtype: bool
        """

        # return
        return self.path() == str(path)

    def __ne__(self, path):
        """check if the Path has not the same name as the other path

        :param path: path to check with
        :type path: str or :class:`cgp_generic_utils.files.Path`

        :return : ``True`` : the paths are different - ``False`` : the paths are identical
        :rtype: bool
        """

        # return
        return self.path() != str(path)

    def __repr__(self):
        """the representation of the path

        :return: the representation of the path
        :rtype: str
        """

        # return
        return '{0}(\'{1}\')'.format(self.__class__.__name__, self.path())

    def __str__(self):
        """the print of the path

        :return: the print of the path
        :rtype: str
        """

        # return
        return self.path()

    # COMMANDS #

    def baseName(self, withExtension=True):
        """the baseName of the path

        :param withExtension: ``True`` : baseName with extension - ``False`` : baseName without extension
        :type withExtension: bool

        :return: the baseName of the path
        :rtype: str
        """

        # errors
        if not os.path.isdir(self.path()) and not os.path.isfile(self.path()):
            raise ValueError('{0} is not a valid path'.format(self.path()))

        # get baseName
        baseName = os.path.basename(self.path())

        # execute
        if os.path.isfile(self.path()) and not withExtension:
            baseName = baseName.split('.')[0]

        # return
        return baseName

    def directory(self):
        """the parent directory of the path

        :return: the directory of the path
        :rtype: :class:`cgp_generic_utils.files.Directory`
        """

        # return
        return cgp_generic_utils.files._api.entity(os.path.dirname(self.path()))

    def extension(self):
        """the extension of the path

        :return: the extension of the path
        :rtype: str
        """

        # get extension
        extension = os.path.splitext(self.path())[-1][1:]

        # return
        return (extension
                if extension and (self.isFile() or not self.isFile() and not self.isDirectory())
                else None)

    def isDirectory(self):
        """check if the path is a directory

        :return: ``True`` : the path is a directory - ``False`` the path is not a directory
        :rtype: bool
        """

        # return
        return os.path.isdir(self.path())

    def isFile(self):
        """check if the path is a file

        :return: ``True`` : the path is a file - ``False`` the path is not a file
        :rtype: bool
        """

        # return
        return os.path.isfile(self.path())

    def path(self):
        """the path of the entity on the file system

        :return: the path of the entity
        :rtype: str
        """

        # return
        return self._path

    def pathType(self):
        """the type of the path

        :return: the type of the path
        :rtype: str
        """

        # return
        return (cgp_generic_utils.constants.FileFilter.DIRECTORY if self.isDirectory()
                else cgp_generic_utils.constants.FileFilter.FILE)


class File(Path):
    """file object that manipulates any kind of file on the file system
    """

    # ATTRIBUTES #

    _extension = None

    # OBJECT COMMANDS #

    @classmethod
    def create(cls, path, content=None, **__):
        """create the file

        :param path: path of the file
        :type path: str

        :param content: content of the file
        :type content: any

        :return: the created file
        :rtype: :class:`cgp_generic_utils.files.File`
        """

        # errors
        if not Path(path).extension() == cls._extension:
            raise ValueError('{0} is not a {1} path'.format(path, cls.__class__.__name__))

        # execute
        with open(path, 'w') as toWrite:
            toWrite.write(str(content or ''))

        # return
        return cls(path)

    # COMMANDS #

    def copy(self, destinationDirectory=None, destinationName=None):
        """copy the file

        :param destinationDirectory: directory where the copied file will be saved  - If None, same as original
        :type destinationDirectory: str or :class:`cgp_generic_utils.files.Directory`

        :param destinationName: name of the copied file - If None, same as original - ! HAS TO BE WITHOUT EXTENSION !
        :type destinationName: str

        :return: the copied file
        :rtype: :class:`cgp_generic_utils.files.File`
        """

        # init
        destinationDirectory = (str(destinationDirectory)
                                if destinationDirectory
                                else self.directory().path())

        destinationName = ('{0}.{1}'.format(destinationName, self.extension())
                           if destinationName
                           else self.baseName(withExtension=True))

        destinationFileName = os.path.join(destinationDirectory, destinationName)
        isDestinationFile = os.path.isfile(destinationFileName)

        # errors
        if not os.path.isdir(destinationDirectory):
            raise ValueError('{0} is not a valid directory'.format(destinationDirectory))

        if self.path() == destinationFileName:
            raise ValueError('can\'t copy the file on itself')

        if isDestinationFile and not os.access(destinationFileName, os.W_OK):
            raise ValueError('can\'t copy the file on a readOnly file - {0}'.format(destinationFileName))

        # remove destination file if existing - workAround to avoid - IOError: [Errno 13] Permission denied
        if isDestinationFile:
            os.remove(destinationFileName)

        # copy the file
        shutil.copy(self.path(), destinationFileName)

        # return
        return cgp_generic_utils.files._api.entity(destinationFileName)

    def evaluate(self, asLiteral=True):
        """evaluate the content of the file

        :param asLiteral: ``True`` : content evaluated with ast.literal_eval - ``False`` : content evaluated with eval
        :type asLiteral: bool

        :return: the evaluated content of the file
        :rtype: any
        """

        # execute
        return ast.literal_eval(self.read()) if asLiteral else eval(self.read())

    def execute(self):
        """execute the content of the file

        :return: the executed content of the file
        :rtype: any
        """

        # execute
        return execfile(self.path())

    def open(self):
        """open the file in the script editor
        """

        # execute
        subprocess.Popen([cgp_generic_utils.constants.Environment.SCRIPT_EDITOR, self.path()])

    def read(self):
        """read the file

        :return: the content of the file
        :rtype: any
        """

        # execute
        with open(self.path(), 'r') as toRead:
            data = toRead.read()

        # return
        return data

    def write(self, content):
        """write data in the specified path file

        :param content: content to write in the file
        :type content: any
        """

        # execute
        self.create(self.path(), content=content)


class Directory(Path):
    """directory object that manipulates a directory on the file system
    """

    # OBJECT COMMANDS #

    @classmethod
    def create(cls, path, **__):
        """create

        :param path: path of the file to create
        :type path: str

        :return: the created directory
        :rtype: :class:`cgp_generic_utils.files.Directory`
        """

        # execute
        if not os.path.exists(path):
            os.makedirs(path)

        # return
        return cls(path)

    # COMMANDS #

    def baseName(self):
        """the baseName of the directory

        :return: the baseName of the directory
        :rtype: str
        """

        # return
        return super(Directory, self).baseName(withExtension=False)

    def content(self, fileFilters=None, fileExtensions=None, fileExtensionsIncluded=True):
        """content of the directory

        :param fileFilters: filter of the directory children - default is ``cgp_generic_utils.constants.FileFilter.ALL``
        :type fileFilters: list[str]

        :param fileExtensions: extensions of the files to get - default is all extensions
        :type fileExtensions: list[str]

        :param fileExtensionsIncluded: ``True`` : file extensions are included -
                                       ``False`` : file extensions are excluded
        :type fileExtensionsIncluded: bool

        :return: the content of the directory
        :rtype: list[:class:`cgp_generic_utils.files.Directory`,
                :class:`cgp_generic_utils.files.File`,
                :class:`cgp_generic_utils.files.JsonFile`,
                :class:`cgp_generic_utils.files.PyFile`,
                :class:`cgp_generic_utils.files.TxtFile`,
                :class:`cgp_generic_utils.files.UiFile`]
        """

        # init
        fileFilters = fileFilters or cgp_generic_utils.constants.FileFilter.ALL

        # errors
        for fileFilter in fileFilters:
            if fileFilter not in cgp_generic_utils.constants.FileFilter.ALL:
                raise ValueError('{0} is not a file filter - Expected : {1}'
                                 .format(fileFilter, cgp_generic_utils.constants.FileFilter.ALL))

        # init
        filterChildren = {'directories': [],
                          'files': []}

        # get folder children
        children = os.listdir(self.path())

        # filter depending on filter
        for child in children:

            # get child absolute path
            absChild = Path(os.path.join(self.path(), child))

            # get extension
            extension = absChild.extension()

            # check validity
            if (cgp_generic_utils.constants.FileFilter.DIRECTORY not in fileFilters and absChild.isDirectory()
                    or cgp_generic_utils.constants.FileFilter.FILE not in fileFilters and absChild.isFile()):
                continue

            # directories
            if absChild.isDirectory():
                filterChildren['directories'].append(absChild.path())

            # update filterChildren
            elif (not fileExtensions and fileExtensionsIncluded
                    or fileExtensions and fileExtensionsIncluded and extension in fileExtensions
                    or fileExtensions and not fileExtensionsIncluded and extension not in fileExtensions):
                filterChildren['files'].append(absChild.path())

        # return
        return [cgp_generic_utils.files._api.entity(path)
                for path in sorted(filterChildren['directories']) + sorted(filterChildren['files'])]
