"""
qt decorator library
"""

# import third parties
import PySide2.QtCore
import PySide2.QtWidgets

# imports local
import cgp_generic_utils.qt
from . import _generic


class StatusDialog(_generic.Decorator):
    """decorator popping a statusDialog
    """

    def __init__(self,
                 loadDescription,
                 validDescription=None,
                 errorDescription=None,
                 title=None,
                 size=None,
                 parent=None,
                 isFrameless=False):
        """StatusDialog class initialization

        :param loadDescription: description to set when the statusDialog is loaded
        :type loadDescription: str

        :param validDescription: description to set when the statusDialog closes without error
        :type validDescription: str

        :param errorDescription: description to set when the statusDialog closes with error
        :type errorDescription: str

        :param title: the title of the statusDialog
        :type title: str

        :param size: the size of the statusDialog - ``[width - height]`` - ``[None, None]`` is default
        :type size: list[int]

        :param parent: the QWidget to parent the statusDialog to
        :type parent: :class:`PySide2.QtWidgets.QWidget`

        :param isFrameless: ``True`` : the statusDialog is frameless - ``False`` : the statusDialog has a frame
        :type isFrameless: bool
        """

        # init
        self.loadDescription = loadDescription
        self.validDescription = validDescription
        self.errorDescription = errorDescription or 'failed'
        self.dialog = cgp_generic_utils.qt.StatusDialog(title or 'Status Dialog',
                                                        size=size,
                                                        parent=parent,
                                                        isFrameless=isFrameless)
        if parent:
            self.dialog.setModal(True)

    def __enter__(self):
        """enter StatusDialog decorator
        """

        # execute
        self.dialog.load(self.loadDescription)

    def __exit__(self, exceptionType, *_, **__):
        """exit StatusDialog decorator

        :param exceptionType: type of exception if an exception was raised
        :type exceptionType: Exception
        """

        # execute
        description = self.validDescription if exceptionType is None else self.errorDescription
        self.dialog.close(description, closeTime=1 if description else 0)


class WithCursor(_generic.Decorator):
    """decorator switching the cursor during process
    """

    def __init__(self, cursor):
        """initialization of the decorator

        :param cursor: the cursor to set during process
        :type cursor: :class:`PySide2.QtCore.Qt.CursorShape`
        """

        # init
        self._application = PySide2.QtWidgets.QApplication.instance()
        self._cursor = cursor

    def __enter__(self):
        """enter the decorator
        """

        # execute
        self._application.setOverrideCursor(self._cursor)

    def __exit__(self, *_, **__):
        """exit the decorator
        """

        # execute
        self._application.restoreOverrideCursor()
