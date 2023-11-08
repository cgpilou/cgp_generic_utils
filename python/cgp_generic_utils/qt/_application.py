"""
application object library
"""

# imports third-parties
import PySide2.QtWidgets

# imports local
import cgp_generic_utils.python


# APPLICATION OBJECT #


class Application(cgp_generic_utils.python.BaseObject):
    """application object that manipulates any kind of application
    """

    # INIT #

    def __init__(self):
        """Application initialization
        """

        # init
        self._qApplication = PySide2.QtWidgets.QApplication.instance()

        # validate
        if not self._qApplication:
            raise RuntimeError('Unable to init {} object. '
                               'No QApplication is currently running'.format(self.__class__.__name__))

    def __getattr__(self, attribute):
        """override the getattr method

        :param attribute: the attribute to get
        :type attribute: python
        """

        # return
        return getattr(self._qApplication, attribute)

    # COMMANDS #

    def name(self):
        """get the name of the application

        :return: the name of the application
        :rtype: str
        """

        # abstract command
        raise NotImplementedError

    def mainWindow(self):
        """get the main window of the application

        :return: the main window of the application
        :rtype: :class:`PySide2.QtWidgets.QMainWindow`
        """

        # abstract command
        raise NotImplementedError

    def version(self, asTuple=False):
        """get the version of the application

        :param asTuple: ``True`` : the version is queried as a tuple - ``False`` : the version is queried as a string
        :type asTuple: bool

        :return: the version of the application
        :rtype: str or tuple
        """

        # abstract command
        raise NotImplementedError

    def widget(self, name):
        """get a widget of the application

        :param name: name of the widget to get
        :type name: str

        :return: the widget of the application
        :rtype: :class:`PySide2.QtWidgets.QWidget`
        """

        # search for the widget
        for widget in self._qApplication.allWidgets():
            if widget.objectName() == name:
                return widget

        # return None if nothing found
        return None
