"""
custom widget library
"""

# imports python
import os

# imports third-parties
import PySide2.QtCore

# imports local
import cgp_generic_utils.python
import cgp_generic_utils.constants
import cgp_generic_utils.files


class Tool(PySide2.QtWidgets.QWidget):
    """widget holding the generic functions of a tool
    """

    # ATTRIBUTES #

    _object = None
    _name = NotImplemented
    _version = NotImplemented

    # INIT #

    def __init__(self, parent=None):
        """Tool class initialization

        :param parent: parent under which the ui will be parented
        :type parent: :class:`PySide2.QtWidgets.QWidget`
        """

        # init
        super(Tool, self).__init__(parent=parent)
        self._configFile = self._getConfigFile()

        # set title
        self.setTitle()

    def __new__(cls, *args, **kwargs):
        """override new method

        :return: the created instance
        :rtype: :class:`cgp_generic_utils.qt.Tool`
        """

        # init
        if cls._object:
            cls._object.deleteLater()

        # update attribute
        cls._object = super(Tool, cls).__new__(cls, *args, **kwargs)

        # return
        return cls._object

    # PROPERTIES #

    @property
    def name(self):
        """get the name of the tool

        :return: the name of the tool
        :rtype: str
        """

        # errors
        if self._name == NotImplemented:
            raise NotImplementedError('name is not implemented')

        # return
        return self._name

    @ property
    def version(self):
        """get the version of the tool

        :return: the version of the tool
        :rtype: str
        """

        # errors
        if self._name == NotImplemented:
            raise NotImplementedError('version is not implemented')

        # return
        return self._version

    # OBJECT COMMANDS #

    @classmethod
    def load(cls, *args, **kwargs):
        """load the tool

        :return: the loaded tool
        :rtype: Tool
        """

        # get tool instance
        tool = cls._object or cls(*args, **kwargs)

        # show and raise on top
        tool.show()
        cls._object.raise_()

        # return
        return cls._object

    # COMMANDS #

    def configFile(self):
        """get the config file of the tool

        :return: the config file of the tool
        :rtype: :class:`cgp_generic_utils.files.JsonFile`
        """

        # return
        return self._configFile

    def configValue(self, key):
        """get the config value from the config file of the tool

        :param key: key to get the value from the config file of the tool
        :type key: str
        """

        # get config
        config = self.configFile().read()

        # return
        return config.get(key, None)

    def setConfigValue(self, key, value):
        """set the config value in the config file of the tool

        :param key: key of the config to set the value to
        :type key: str

        :param value: value to set in the config file
        :type key: any
        """

        # get config
        config = self.configFile().read()

        # set config
        config[key] = value

        # update config file
        self.configFile().write(config)

    def setTitle(self, title=None):
        """set the title of the tool

        :param title: title of the tool to set - if nothing specified title will be -> name version
        :type title: str
        """

        # get title
        title = title or '{0} {1}'.format(self.name.replace('_', ' '), self.version).title()

        # execute
        self.setObjectName(self.name)
        self.setWindowTitle(title)

    # PRIVATE COMMANDS #

    def _getConfigFile(self):
        """get the config file of the tool

        :return: the config file of the tool
        :rtype: :class:`cgp_generic_utils.files.JsonFile`
        """

        # init
        configDirectory = cgp_generic_utils.constants.Environment.CONFIG_DIRECTORY
        configFile = os.path.join(cgp_generic_utils.constants.Environment.CONFIG_DIRECTORY,
                                  '{0}.json'.format(self.name))

        # create config directory if not existing
        if not os.path.isdir(configDirectory):
            os.makedirs(configDirectory)

        # return
        return (cgp_generic_utils.files.createFile(configFile)
                if not os.path.isfile(configFile)
                else cgp_generic_utils.files.entity(configFile))
