"""
miscellaneous file object library
"""

# imports python
import os

# imports local
import cgp_generic_utils.constants
from . import _generic, _python


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
    def create(cls, path, content=None, **__):
        """create a ui file

        :param path: path of the ui file
        :type path: str

        :param content: content of the ui file
        :type content: any

        :return: the created ui file
        :rtype: :class:`cgp_generic_utils.files.UiFile`
        """

        # errors
        if not _generic.Path(path).extension() == cls._extension:
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
        """compile the ui file

        :param targetDirectory: directory of the compiled Ui - if not specified, command will use the UiFile directory
        :type targetDirectory: str or :class:`cgp_generic_utils.files.Directory`

        :return: the compiled file
        :rtype: :class:`cgp_generic_utils.files.PyFile`
        """

        # import qt lib here to avoid import issue in batch mode
        import pyside2uic
        import cgp_generic_utils.qt

        # set target directory if not specified
        targetDirectory = str(targetDirectory) or self.directory().path()

        # get compile file
        compiledFile = os.path.join(targetDirectory, self.baseName(withExtension=True).replace('.ui', '.py'))

        # generate file
        srcFile = open(self.path(), 'r')
        tgtFile = open(compiledFile, 'w')

        # compile
        pyside2uic.compileUi(srcFile, tgtFile)
        srcFile.close()
        tgtFile.close()

        # get file object
        compiledFile = _python.PyFile(compiledFile)

        # get compiled file content
        content = compiledFile.read().replace('from PySide2 import QtCore, QtGui, QtWidgets',
                                              'from PySide2 import QtCore, QtGui, QtWidgets\n'
                                              'import cgp_generic_utils.qt')

        for qType in cgp_generic_utils.qt.__all__:
            content = content.replace('QtWidgets.Q{0}'.format(qType), 'cgp_generic_utils.qt.{0}'.format(qType))

        # rewrite compiled file
        compiledFile.write(content)

        # return
        return compiledFile
