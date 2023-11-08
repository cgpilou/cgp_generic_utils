"""
custom widget library
"""

# imports python
import inspect
import os

# imports third-parties
import PySide2.QtCore
import PySide2.QtGui
import PySide2.QtWidgets

# imports local
import cgp_generic_utils.python
import cgp_generic_utils.constants
import cgp_generic_utils.files
from . import _api
from . import _qtGui


class BaseTool(PySide2.QtWidgets.QWidget):
    """widget object that manipulates a tool
    """

    # ATTRIBUTES #

    _GRIP_SIZE = _api.scaledSize(8)
    _HELP_URL = NotImplemented
    _INSTANCE = None
    _LAYOUT_INDEX = 2
    _ICON = NotImplemented
    _NAME = NotImplemented
    _VERSION = None

    # INIT #

    def __init__(self, parent=None):
        """Tool class initialization

        :param parent: parent under which the ui will be parented
        :type parent: :class:`PySide2.QtWidgets.QWidget`
        """

        # init
        super(BaseTool, self).__init__(parent=parent)

        # set window flags
        self.setWindowFlags(PySide2.QtCore.Qt.FramelessWindowHint)

        # set focus policy
        self.setFocusPolicy(PySide2.QtCore.Qt.StrongFocus)

        # setup base layout
        self._baseLayout = PySide2.QtWidgets.QVBoxLayout(self)
        self._baseLayout.setContentsMargins(1, 1, 1, 1)
        self._baseLayout.setSpacing(0)

        # setup title bar
        self._titleBar = TitleBar(parent=self)
        self._baseLayout.addWidget(self._titleBar)

        #
        self._baseLayout.addSpacing(1)

        # setup content widget
        self._contentWidget = PySide2.QtWidgets.QWidget(parent=self)
        self._baseLayout.addWidget(self._contentWidget)

        # setup status bar
        self._statusBar = StatusBar(parent=self)
        self._statusBar.setVisible(False)
        self._baseLayout.addWidget(self._statusBar)

        # create context menu
        self.setContextMenuPolicy(PySide2.QtCore.Qt.CustomContextMenu)
        self._contextMenu = PySide2.QtWidgets.QMenu(parent=self)
        self.customContextMenuRequested.connect(self.showContextMenu)

        # setup resize grips
        self._grips = []
        for _ in range(4):
            grip = PySide2.QtWidgets.QSizeGrip(self)
            grip.resize(self._GRIP_SIZE, self._GRIP_SIZE)
            self._grips.append(grip)

        # setup drag and drop window moves
        self._dragPosition = None

        # setup style
        palette = PySide2.QtGui.QPalette()
        palette.setColor(PySide2.QtGui.QPalette.Window, PySide2.QtGui.QColor('#1d2121'))
        self.setAutoFillBackground(True)
        self.setPalette(palette)

        palette = PySide2.QtGui.QPalette()
        palette.setColor(PySide2.QtGui.QPalette.Window, PySide2.QtGui.QColor('#444444'))
        self._contentWidget.setAutoFillBackground(True)
        self._contentWidget.setPalette(palette)

        self.setStyleSheet('QSizeGrip{border: none;}')

        # setup object name
        name = self.name()
        self.setObjectName(name)

        # setup title
        title = '{0} {1}'.format(name.replace('_', ' '), self.version()).title()
        self.setWindowTitle(title)

        # setup tool icon
        if self._ICON != NotImplemented:
            self.titleBar().setIcon(self._ICON)

        # connect title bar
        self.titleBar().closeButton().clicked.connect(self.close)
        self.titleBar().doubleClicked.connect(lambda: self.showNormal() if self.isMaximized() else self.showMaximized())
        url = PySide2.QtCore.QUrl(self._HELP_URL)
        self.titleBar().helpButton().clicked.connect(lambda: PySide2.QtGui.QDesktopServices.openUrl(url))
        self.titleBar().maximizeButton().clicked.connect(lambda: self.showNormal() if self.isMaximized() else self.showMaximized())
        self.titleBar().minimizeButton().clicked.connect(self.showMinimized)

    def __new__(cls, *args, **kwargs):
        """override new method

        :return: the created instance
        :rtype: :class:`cgp_generic_utils.qt.Tool`
        """

        # init
        if cls._INSTANCE:
            cls._INSTANCE.deleteLater()

        # update attribute
        cls._INSTANCE = super(BaseTool, cls).__new__(cls, *args, **kwargs)

        # return
        return cls._INSTANCE

    # OBJECT COMMANDS #

    @classmethod
    def load(cls, *args, **kwargs):
        """load the tool

        :return: the loaded tool
        :rtype: Tool
        """

        # get tool instance
        tool = cls._INSTANCE or cls(*args, **kwargs)

        # show and raise on top
        tool.show()
        cls._INSTANCE.raise_()

        # return
        return cls._INSTANCE

    # COMMANDS #

    def contextMenu(self):
        """get the context menu

        :return: the context menu
        :rtype: :class:`PySide2.QtWidgets.QMenu`
        """

        # return
        return self._contextMenu

    def layout(self):
        """get the layout of the Tool

        :return: the layout of the Tool
        :rtype: :class:`PySide2.QtWidgets.QLayout`
        """

        # return
        return self._contentWidget.layout()

    def mousePressEvent(self, event):
        """event handler triggered when the mouse is pressed in the Tool

        :param event: the mouse event that as been triggered
        :type event: :class:`PySide2.QtGui.QMouseEvent`
        """
        
        # init
        super(BaseTool, self).mousePressEvent(event)

        # store tool position for dragging
        self._dragPosition = self.window().mapFromGlobal(event.globalPos())

    def mouseMoveEvent(self, event):
        """event handler triggered when the mouse is moved in the Tool

        :param event: the mouse event that as been triggered
        :type event: :class:`PySide2.QtGui.QMouseEvent`
        """

        # init
        super(BaseTool, self).mouseMoveEvent(event)

        # update tool position
        delta = self.window().mapFromGlobal(event.globalPos()) - self._dragPosition
        self.move(self.x() + delta.x(), self.y() + delta.y())

        # store tool position for dragging
        self._dragPosition = self.window().mapFromGlobal(event.globalPos())

    def name(self):
        """get the name of the Tool

        :return: the name of the Tool
        :rtype: str
        """

        # errors
        if self._NAME == NotImplemented:
            raise NotImplementedError('name is not implemented')

        # return
        return self._NAME

    def showContextMenu(self, clickPosition):
        """show the context menu

        :param clickPosition: the position of the click that requested the context menu
        :type clickPosition: :class:`PySide2.QtCore.QPoint`
        """

        # execute
        self.contextMenu().exec_(self.mapToGlobal(clickPosition))

    def resizeEvent(self, event):
        """event handler triggered when the the Tool is resized

        :param event: the resize event that as been triggered
        :type event: :class:`PySide2.QtGui.QResizeEvent`
        """

        # default behavior
        super(BaseTool, self).resizeEvent(event)

        # update grips positions
        rect = self.rect()
        self._grips[1].move(rect.right() - self._GRIP_SIZE, 0)
        self._grips[2].move(rect.right() - self._GRIP_SIZE, rect.bottom() - self._GRIP_SIZE)
        self._grips[3].move(0, rect.bottom() - self._GRIP_SIZE)

    def setLayout(self, layout):
        """set the layout of the Tool

        :param layout: the layout of the Tool
        :type layout: :class:`PySide2.QtWidgets.QLayout`
        """

        # execute
        self._contentWidget.setLayout(layout)

    def version(self):
        """get the version of the Tool

        :return: the version of the Tool
        :rtype: str
        """

        # return
        return self._VERSION

    def setWindowTitle(self, title):
        """set the window title of the Tool

        :param title: the window title of the Tool
        :type title: str
        """

        # execute
        super(BaseTool, self).setWindowTitle(title)
        self._titleBar.setTitle(title)

    def statusBar(self):
        """get the status bar of the Tool

        :return: the status bar of the Tool
        :rtype: :class:`cgp_generic_utils.qt.StatusBar`
        """

        # return
        return self._statusBar

    def titleBar(self):
        """get the title bar of the Tool

        :return: the title bar of the Tool
        :rtype: :class:`cgp_generic_utils.qt.TitleBar`
        """

        # return
        return self._titleBar


class StatusBar(PySide2.QtWidgets.QStatusBar):
    """widget object that manipulates a tool status bar
    """

    # INIT #

    def __init__(self, parent=None):
        """initialization of the TitleBar

        :param parent: the parent widget of the TitleBar
        :type parent: :class:`PySide2.QtWidgets.QWidget`
        """

        # init
        super(StatusBar, self).__init__(parent=parent)

        # setup style
        palette = PySide2.QtGui.QPalette()
        palette.setColor(PySide2.QtGui.QPalette.Window, PySide2.QtGui.QColor('#444444'))
        self.setAutoFillBackground(True)
        self.setPalette(palette)


class TitleBar(PySide2.QtWidgets.QWidget):
    """widget object that manipulates a tool title bar
    """

    # ATTRIBUTES #

    _BACKGROUND_COLOR = '#33393b'
    _HEIGHT = _api.scaledSize(30)
    _ICON = NotImplemented

    # SIGNALS #

    doubleClicked = PySide2.QtCore.Signal()

    # INIT #

    def __init__(self, parent=None):
        """initialization of the TitleBar

        :param parent: the parent widget of the TitleBar
        :type parent: :class:`PySide2.QtWidgets.QWidget`
        """

        # init
        super(TitleBar, self).__init__(parent=parent)

        # setup style
        # we need a QPalette to have a full dark grey title bar, stylesheet is not enough here
        self.setFixedHeight(self._HEIGHT)
        palette = PySide2.QtGui.QPalette()
        palette.setColor(PySide2.QtGui.QPalette.Window, PySide2.QtGui.QColor(self._BACKGROUND_COLOR))
        self.setAutoFillBackground(True)
        self.setPalette(palette)
        self.setStyleSheet('QWidget{{color: #EEEEEE;}}'
                           'QPushButton'
                           '{{background: transparent;'
                           'border: 1px solid {};}}'
                           'QPushButton::hover'
                           '{{background: rgba(255, 255, 255, 0.1);}}'.format(self._BACKGROUND_COLOR))

        # create horizontal layout
        layout = PySide2.QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # add spacer
        layout.addSpacing(self._HEIGHT * 0.3)

        # create icon
        self._icon = PySide2.QtWidgets.QLabel(parent=self)
        self._icon.setFixedSize(self._HEIGHT * 0.68, self._HEIGHT * 0.68)
        self._icon.setScaledContents(True)

        # create title label
        self._label = PySide2.QtWidgets.QLabel(parent=self)

        # create help buttons
        self._helpButton = PySide2.QtWidgets.QPushButton('?', parent=self)

        # create minimize buttons
        iconPath = os.path.join(cgp_generic_utils.constants.Environment.ICON_LIBRARY, 'underscore_64_EEEEEE.png')
        iconSize = _api.scaledSize(10)
        self._minimizeButton = PySide2.QtWidgets.QPushButton(parent=self)
        self._minimizeButton.setIcon(_qtGui.Pixmap(iconPath))
        self._minimizeButton.setIconSize(PySide2.QtCore.QSize(iconSize, iconSize))

        # create maximize buttons
        iconPath = os.path.join(cgp_generic_utils.constants.Environment.ICON_LIBRARY, 'square_64_EEEEEE.png')
        iconSize = _api.scaledSize(14)
        self._maximizeButton = PySide2.QtWidgets.QPushButton(parent=self)
        self._maximizeButton.setIcon(_qtGui.Pixmap(iconPath))
        self._maximizeButton.setIconSize(PySide2.QtCore.QSize(iconSize, iconSize))

        # create close buttons
        iconPath = os.path.join(cgp_generic_utils.constants.Environment.ICON_LIBRARY, 'cross_64_EEEEEE.png')
        iconSize = _api.scaledSize(14)
        self._closeButton = PySide2.QtWidgets.QPushButton(parent=self)
        self._closeButton.setIcon(_qtGui.Pixmap(iconPath))
        self._closeButton.setIconSize(PySide2.QtCore.QSize(iconSize, iconSize))

        # collect buttons
        buttons = [self._helpButton, self._minimizeButton, self._maximizeButton, self._closeButton]

        # add icon
        layout.addWidget(self._icon)

        #
        for index in range(len(buttons) - 1):
            layout.addItem(PySide2.QtWidgets.QSpacerItem(self._HEIGHT,
                                                         self._HEIGHT,
                                                         PySide2.QtWidgets.QSizePolicy.Fixed,
                                                         PySide2.QtWidgets.QSizePolicy.Fixed))

        # add spacers
        spacer = PySide2.QtWidgets.QSpacerItem(0,
                                               0,
                                               PySide2.QtWidgets.QSizePolicy.Expanding,
                                               PySide2.QtWidgets.QSizePolicy.Expanding)
        layout.addItem(spacer)

        # add label
        layout.addWidget(self._label)

        # add spacers
        layout.addItem(spacer)

        # customize buttons
        for button in buttons:
            button.setFixedSize(self._HEIGHT, self._HEIGHT)
            layout.addWidget(button)

    # COMMANDS #

    def closeButton(self):
        """get the close button of the TitleBar

        :return: the close button of the TitleBar
        :rtype: :class:`PySide2.QtWidgets.QPushButton`
        """

        # return
        return self._closeButton

    def mouseDoubleClickEvent(self, event):
        """event handler triggered when the mouse is double clicked in the TitleBar

        :param event: the mouse event that as been triggered
        :type event: :class:`PySide2.QtGui.QMouseEvent`
        """

        # maximize window
        if event.button() == PySide2.QtCore.Qt.LeftButton:
            self.doubleClicked.emit()

        # default behavior
        super(TitleBar, self).mouseDoubleClickEvent(event)

    def helpButton(self):
        """get the help button of the TitleBar

        :return: the help button of the TitleBar
        :rtype: :class:`PySide2.QtWidgets.QPushButton`
        """

        # return
        return self._helpButton

    def maximizeButton(self):
        """get the maximize button of the TitleBar

        :return: the maximize button of the TitleBar
        :rtype: :class:`PySide2.QtWidgets.QPushButton`
        """

        # return
        return self._maximizeButton

    def minimizeButton(self):
        """get the minimize button of the TitleBar

        :return: the minimize button of the TitleBar
        :rtype: :class:`PySide2.QtWidgets.QPushButton`
        """

        # return
        return self._minimizeButton

    def setIcon(self, icon):
        """set the icon of the TitleBar

        :param icon: the icon path of the TitleBar
        :type icon: str
        """

        # execute
        self._icon.setPixmap(_qtGui.Pixmap(icon))

    def setTitle(self, title):
        """set the title of the TitleBar

        :param title: the title of the TitleBar
        :type title: str
        """

        # execute
        self._label.setText(title)

    def title(self):
        """get the title of the TitleBar

        :return: the title of the TitleBar
        :rtype: str
        """

        # return
        return self._label.text()


class Tool(PySide2.QtWidgets.QWidget):
    """widget holding the generic functions of a tool
    """

    # ATTRIBUTES #

    _object = None
    _name = NotImplemented
    _HELP_URL = ''

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

        # create context menu
        self.setContextMenuPolicy(PySide2.QtCore.Qt.CustomContextMenu)
        self._contextMenu = PySide2.QtWidgets.QMenu(parent=self)
        self.customContextMenuRequested.connect(lambda click: self._contextMenu.exec_(self.mapToGlobal(click)))

        #
        self._contextMenu.addSeparator()
        self._quitAction = PySide2.QtWidgets.QAction('Quit', parent=self)
        self._quitAction.setToolTip('Quit the tool')
        self._quitAction.triggered.connect(self.close)
        self._contextMenu.addAction(self._quitAction)

        # create repair action
        if self._HELP_URL:
            self._helpAction = PySide2.QtWidgets.QAction('Help', parent=self)
            self._helpAction.setToolTip('Show tool help')
            url = PySide2.QtCore.QUrl(self._HELP_URL)
            self._helpAction.triggered.connect(lambda: PySide2.QtGui.QDesktopServices.openUrl(url))
            self._contextMenu.addAction(self._helpAction)
        self._contextMenu.addSeparator()

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

    @property
    def version(self):
        """get the version of the tool

        :return: the version of the tool
        :rtype: str
        """

        # will return the version of the package from where this command will be called
        return inspect.getfile(self.__class__).split('python')[0].split(os.sep)[-2]

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