"""
subclassed QApplication, QtWidgets, custom dialogs and widgets for UI development
"""

# imports local
from ._api import scaledSize
from ._application import Application
from ._qtGui import Font, Icon, Pixmap, Movie
from ._dialogs import (BaseDialog, CheckBoxDialog, ComboBoxDialog, ProgressBarDialog,
                       ComboBoxLineEditDialog, LineEditDialog, StatusDialog, TextEditDialog)
from ._custom import BaseTool, StatusBar, TitleBar, Tool
from ._qtWidgets import ComboBox, LineEdit, ListWidget, Menu, ProgressBar, PushButton, TreeWidget, TreeWidgetItem


# API


_APPLICATION_TYPE = Application


def application():
    """get the application
    """

    # return
    return _APPLICATION_TYPE()


def registerApplicationType(applicationType):
    """register application type - note that only one application type can be define at a time

    :param applicationType: the application type to register
    :type applicationType: python
    """

    # init
    global _APPLICATION_TYPE

    # execute
    _APPLICATION_TYPE = applicationType


# ALL


__all__ = ['scaledSize',
           'application', 'registerApplicationType', 'Application',
           'Font', 'Icon', 'Pixmap', 'Movie',
           'BaseDialog', 'CheckBoxDialog', 'ComboBoxDialog', 'ProgressBarDialog',
           'ComboBoxLineEditDialog', 'LineEditDialog', 'StatusDialog', 'TextEditDialog',
           'Tool',
           'ComboBox', 'LineEdit', 'ListWidget', 'Menu', 'ProgressBar', 'PushButton', 'TreeWidget', 'TreeWidgetItem']
