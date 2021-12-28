"""
qt decorator library
"""

# imports local
from . import _abstract
import cgp_generic_utils.qt


class StatusDialog(_abstract.Decorator):
    """StatusDialog class
    """

    def __init__(self, loadDescription, closeDescription, title, size=None, parent=None, isFrameless=False):
        """StatusDialog class initialization

        :param loadDescription: description to set when the dialog is loaded
        :type loadDescription: str

        :param closeDescription: description to set when the dialog closes
        :type closeDescription: str
        """

        # init
        self.loadDescription = loadDescription
        self.closeDescription = closeDescription
        self.dialog = cgp_generic_utils.qt.StatusDialog(title, size=size, parent=parent, isFrameless=isFrameless)

    def __enter__(self):
        """enter DisableAutokey decorator
        """

        # execute
        self.dialog.load(self.loadDescription)

    def __exit__(self, *args, **kwargs):
        """exit DisableAutokey decorator
        """

        # execute
        self.dialog.close(self.closeDescription)
