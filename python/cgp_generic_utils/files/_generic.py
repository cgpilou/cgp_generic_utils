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
        """check if the Path is identical to the other path

        :param path: path to compare the path to
        :type path: str or :class:`cgp_generic_utils.files.Path`

        :return : ``True`` : the paths are identical - ``False`` : the paths are different
        :rtype: bool
        """

        # return
        return self.path() == str(path)

    def __ne__(self, path):
        """check if the Path is different from the other path

        :param path: path to compare the path to
        :type path: str or :class:`cgp_generic_utils.files.Path`

        :return : ``True`` : the paths are different - ``False`` : the paths are identical
        :rtype: bool
        """

        # return
        return self.path() != str(path)

    def __repr__(self):
        """get the representation of the path

        :return: the representation of the path
        :rtype: str
        """

        # return
        return '{0}({1!r})'.format(self.__class__.__name__, self.path())

    def __str__(self):
        """get the string representation of the path

        :return: the string representation of the path
        :rtype: str
        """

        # return
        return self.path()

    # COMMANDS #

    def baseName(self):
        """get the baseName of the path

        :return: the baseName of the path
        :rtype: str
        """

        # errors
        if not self.isFile() and not self.isDirectory():
            raise ValueError('{0} is not an existing path'.format(self.path()))

        # return
        return os.path.basename(self.path())

    def directory(self):
        """get the directory of the path

        :return: the directory of the path
        :rtype: :class:`cgp_generic_utils.files.Directory`
        """

        # errors
        if not self.isFile() and not self.isDirectory():
            raise ValueError('{0} is not an existing path'.format(self.path()))

        # return
        return cgp_generic_utils.files._api.FILE_TYPES['directory'](os.path.dirname(self.path()))

    def isDirectory(self):
        """check if the path is a directory

        :return: ``True`` : the path is a directory - ``False`` : the path is not a directory
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
        """get the path of the entity on the file system

        :return: the path of the entity on the file system
        :rtype: str
        """

        # return
        return self._path


class File(Path):
    """file object that manipulates any kind of file on the file system
    """

    # ATTRIBUTES #

    _extension = None

    # OBJECT COMMANDS #

    @classmethod
    def create(cls, path, content=None, **__):
        """create a file

        :param path: the path of the file
        :type path: str

        :param content: the content to set into the file
        :type content: any

        :return: the created file
        :rtype: File
        """

        # errors
        if not cgp_generic_utils.files._api.getExtension(path) == cls._extension:
            raise ValueError('{0} is not a {1} path'.format(path, cls.__class__.__name__))

        # execute
        with open(path, 'w') as toWrite:
            toWrite.write(str(content or ''))

        # return
        return cls(path)

    # COMMANDS #

    def baseName(self, withExtension=True):
        """get the baseName of the file

        :param withExtension: ``True`` : the baseName is returned with extension -
                              ``False`` : the baseName is returned without extension
        :type withExtension: bool

        :return: the baseName of the file
        :rtype: str
        """

        # get baseName
        baseName = os.path.basename(self.path())

        # return
        return baseName if withExtension else baseName.split('.')[0]

    def copy(self, destinationDirectory=None, destinationName=None, isPreservingMetadata=False):
        """copy the file

        :param destinationDirectory: directory where the copied file will be saved  - If None, same as original
        :type destinationDirectory: str or :class:`cgp_generic_utils.files.Directory`

        :param destinationName: name of the copied file - If None, same as original - ``HAS TO BE WITHOUT EXTENSION``
        :type destinationName: str

        :param isPreservingMetadata: ``True`` : the copy preserves the metadata -
                                     ``False`` : the copy doesn't preserve the metadata
        :type isPreservingMetadata: bool

        :return: the copied file
        :rtype: File
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
        if isPreservingMetadata:
            shutil.copy2(self.path(), destinationFileName)
        else:
            shutil.copy(self.path(), destinationFileName)

        # return
        return cgp_generic_utils.files._api.entity(destinationFileName)

    def evaluate(self, asLiteral=True):
        """evaluate the content of the file

        :param asLiteral: ``True`` : the content is evaluated with ast.literal_eval -
                          ``False`` : the content is evaluated with eval
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

    def extension(self):
        """get the extension of the file

        :return: the extension of the file
        :rtype: str
        """

        # return
        return self._extension or cgp_generic_utils.files._api.getExtension(self.path())

    def open_(self):
        """open the file
        """

        # check script editor variable
        if cgp_generic_utils.constants.Environment.SCRIPT_EDITOR is NotImplemented:
            raise RuntimeError('cgp_generic_utils.constants.Environment.SCRIPT_EDITOR constant needs to be implemented')

        # execute
        subprocess.Popen([cgp_generic_utils.constants.Environment.SCRIPT_EDITOR, self.path()])

    def read(self):
        """read the file

        :return: the content of the file
        :rtype: str
        """

        # execute
        with open(self.path(), 'r') as toRead:
            data = toRead.read()

        # return
        return data

    def setBasename(self, basename):
        """set the basename of the file

        :param basename: the basename to set to the file
        :type basename: str
        """

        # get new path
        newPath = '{0}{1}{2}.{3}'.format(self.directory().path(),
                                         os.sep,
                                         basename,
                                         self.extension())

        # return
        if self.path() == newPath:
            return

        # errors
        if os.path.isfile(newPath):
            raise ValueError('a file with the same basename is already existing')

        # set basename
        os.rename(self.path(), newPath)

        # update path attribute
        self._path = newPath

    def write(self, content):
        """write the content in the file

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
        """create a directory

        :param path: path of the directory to create
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

    def content(self, fileFilters=None, fileExtensions=None, fileExtensionsIncluded=True):
        """get the content of the directory

        :param fileFilters: the filter of the directory children - default is ``cgp_generic_utils.constants.FileFilter.ALL``
        :type fileFilters: list[:class:`cgp_generic_utils.constants.FileFilter`]

        :param fileExtensions: the extensions of the files to get - default is all extensions
        :type fileExtensions: list[str]

        :param fileExtensionsIncluded: ``True`` : the file extensions are included -
                                       ``False`` : the file extensions are excluded
        :type fileExtensionsIncluded: bool

        :return: the directory content
        :rtype: list[Directory, File]
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
            extension = cgp_generic_utils.files._api.getExtension(absChild.path())

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

    def setBasename(self, basename):
        """set the basename of the directory

        :param basename: the basename to set to the directory
        :type basename: str
        """

        # get new path
        newPath = '{0}{1}{2}'.format(self.directory().path(),
                                     os.sep,
                                     basename)

        # return
        if self.path() == newPath:
            return

        # errors
        if os.path.isdir(newPath):
            raise ValueError('a directory with the same basename is already existing')

        # set basename
        os.rename(self.path(), newPath)

        # update path attribute
        self._path = newPath
