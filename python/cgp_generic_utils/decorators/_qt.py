"""
qt decorator library
"""

# imports local
from . import _abstract
import cgp_generic_utils.qt


class StatusDialog(_abstract.Decorator):
    """decorator popping a status dialog
    """

    def __init__(self, loadDescription,
                 validDescription,
                 errorDescription,
                 title,
                 size=None,
                 parent=None,
                 isFrameless=False):
        """StatusDialog class initialization

        :param loadDescription: description to set when the dialog is loaded
        :type loadDescription: str

        :param validDescription: description to set when the dialog closes with no occurring errors
        :type validDescription: str

        :param errorDescription: description to set when the dialog closes with errors
        :type errorDescription: str
        """

        # init
        self.loadDescription = loadDescription
        self.validDescription = validDescription
        self.errorDescription = errorDescription
        self.dialog = cgp_generic_utils.qt.StatusDialog(title, size=size, parent=parent, isFrameless=isFrameless)

    def __enter__(self):
        """enter StatusDialog decorator
        """

        # execute
        self.dialog.load(self.loadDescription)

    def __exit__(self, exceptionType, *args, **kwargs):
        """exit StatusDialog decorator
        """

        # get description
        description = self.validDescription if exceptionType is None else self.errorDescription

        # close dialog
        self.dialog.close(description)
