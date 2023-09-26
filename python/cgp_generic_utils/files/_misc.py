"""
miscellaneous file object library
"""

# imports python
import os

# imports local
import cgp_generic_utils.python
from . import _generic, _python
from . import _api


# MISC FILE OBJECTS #


class TxtFile(_generic.File):
    """file object that manipulates a ``.txt`` file on the file system
    """

    # ATTRIBUTES #

    _extension = 'txt'


class UiFile(_generic.File):
    """file object that manipulates a ``.ui`` file on the file system
    """

    # ATTRIBUTES #

    _extension = 'ui'

    # OBJECT COMMANDS #

    @classmethod
    def create(cls, path, content=None, **kwargs):
        """create a uiFile

        :param path: path of the uiFile
        :type path: str

        :param content: content to set into the uiFile
        :type content: Any

        :return: the created uiFile
        :rtype: :class:`cgp_generic_utils.files.UiFile`
        """

        # errors
        if not _api.getExtension(path) == cls._extension:
            raise ValueError('{0} is not a UiFile path'.format(path))

        # get content
        if not content:
            content = """<?xml version="1.0" encoding="UTF-8"?>
                      <ui version="4.0">
                       <class>Form</class>
                       <widget class="QWidget" name="Form">
                        <property name="geometry">
                         <rect>
                          <x>0</x>
                          <y>0</y>
                          <width>400</width>
                          <height>300</height>
                         </rect>
                        </property>
                        <property name="windowTitle">
                         <string>Form</string>
                        </property>
                       </widget>
                       <resources/>
                       <connections/>
                      </ui>"""

        # execute
        with open(path, 'w') as toWrite:
            toWrite.write(str(content))

        # return
        return cls(path)

    # COMMANDS #

    def compile(self, targetDirectory=None):
        """compile the uiFile

        :param targetDirectory: directory of the compiled Ui - if not specified, command will use the UiFile directory
        :type targetDirectory: str or :class:`cgp_generic_utils.files.Directory`

        :return: the compiled file
        :rtype: :class:`cgp_generic_utils.files.PyFile`
        """

        # import qt lib - import here to avoid import issue in batch mode
        import pyside2uic

        # set target directory if not specified
        targetDirectory = targetDirectory or self.directory().path()

        # get compile file
        compiledFile = os.path.join(targetDirectory, self.baseName(withExtension=True).replace('.ui', '.py'))

        # generate file
        srcFile = open(self.path(), 'r')
        tgtFile = open(compiledFile, 'w')

        # compile
        pyside2uic.compileUi(srcFile, tgtFile)
        srcFile.close()
        tgtFile.close()

        # return
        return _python.PyFile(compiledFile)
