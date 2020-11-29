"""
custom widget library
"""

# imports third-parties
import PySide2.QtWidgets
import PySide2.QtCore

# import local
import cgp_generic_utils.python
import cgp_generic_utils.constants
from . import _qtGui


class CollapsibleWidget(PySide2.QtWidgets.QWidget):
    """widget that allows to hide/show its content by collapsing/expanding
    """

    collapseChanged = PySide2.QtCore.Signal(bool)

    # INIT #

    def __init__(self, title, titleHeight, backgroundColor=None, foregroundColor=None,
                 orientation=None, margins=None, spacing=0, isCollapsed=True, parent=None):
        """CollapsibleWidget class initialization

        :param title: title of the header
        :type title: str

        :param titleHeight: height of the header title
        :type titleHeight: int

        :param backgroundColor: background color of the header - [1, 1, 1] is default
        :type backgroundColor: list[int, float]

        :param foregroundColor: foreground color of the header - [1, 1, 1] is default
        :type foregroundColor: list[int, float]

        :param orientation: orientation of the content layout - [Orientation.HORIZONTAL - Orientation.VERTICAL]
        :type orientation: str

        :param margins: values of the margins of the content layout - [0, 0, 0, 0] is default
        :type margins: list[int]

        :param spacing: value of the spacing of the content layout
        :type spacing: int

        :param isCollapsed: defines whether or not the widget is collapsed at initialization
        :type isCollapsed: bool

        :param parent: widget under which the CollapsibleWidget will be parented
        :type parent: :class:`Pyside2.QtWidgets.QWidget`
        """

        # init
        orientation = orientation or cgp_generic_utils.constants.Orientation.VERTICAL
        backgroundColor = backgroundColor or [1, 1, 1]
        foregroundColor = foregroundColor or [1, 1, 1]
        margins = margins or [0, 0, 0, 0]

        # error
        if orientation not in cgp_generic_utils.constants.Orientation.ALL:
            raise ValueError('{0} is an invalid orientation - {1}'
                             .format(orientation, cgp_generic_utils.constants.Orientation.ALL))

        # init
        super(CollapsibleWidget, self).__init__(parent=parent)

        # store data
        self._isCollapsed = False
        self._title = title
        self._titleHeight = titleHeight
        self._bgColor = backgroundColor
        self._fgColor = foregroundColor
        self._orientation = orientation

        # set size
        self.setMinimumHeight(self._titleHeight)

        ###############
        # MAIN LAYOUT #
        ###############

        # build
        self._mainLayout = PySide2.QtWidgets.QVBoxLayout(self)

        # set parameters
        self._mainLayout.setContentsMargins(0, 0, 0, 0)
        self._mainLayout.setSpacing(0)

        ##########
        # HEADER #
        ##########

        # build
        self._header = PySide2.QtWidgets.QPushButton(self)

        # set icon
        self._header.setIcon(_qtGui.Icon('arrow_plain_down_grey.png'))
        self._header.setIconSize(PySide2.QtCore.QSize(self._titleHeight - 10, self._titleHeight - 10))

        # format colors
        bgColor = [float(value) * 100.0 for value in self._bgColor]
        fgColor = [float(value) * 100.0 for value in self._fgColor]

        # set parameters
        self._header.setText(self._title)
        self._header.setFixedHeight(self._titleHeight)

        style = """QPushButton {
                                text-align: left;
                                font-weight: bold;
                                font-size: 11px;
                                padding-left: 5px;
                                background-color: %s;
                                color: %s;
                               }

                QPushButton:pressed {
                                background-color: %s;
                                border-style: solid;
                                color: %s;
                                };"""

        pressedBgColor = 'rgb({0}%, {1}%, {2}%)'.format(bgColor[0] * 0.8, bgColor[1] * 0.8, bgColor[2] * 0.8)
        pressedFgColor = 'rgb({0}%, {1}%, {2}%)'.format(fgColor[0] * 0.8, fgColor[1] * 0.8, fgColor[2] * 0.8)
        bgColor = 'rgb({0}%, {1}%, {2}%)'.format(*bgColor)
        fgColor = 'rgb({0}%, {1}%, {2}%)'.format(*fgColor)

        self._header.setStyleSheet(style % (bgColor, fgColor, pressedBgColor, pressedFgColor))

        # add to main layout
        self._mainLayout.addWidget(self._header)

        ##################
        # CONTENT LAYOUT #
        ##################

        # build content widget
        self._contentWidget = PySide2.QtWidgets.QWidget(self)

        # build content layout
        if orientation == 'vertical':
            self._contentLayout = PySide2.QtWidgets.QVBoxLayout()
        else:
            self._contentLayout = PySide2.QtWidgets.QHBoxLayout()

        self._contentWidget.setLayout(self._contentLayout)

        # set parameters
        self._contentLayout.setContentsMargins(*margins)
        self._contentLayout.setSpacing(spacing)

        # add to main layout
        self._mainLayout.addWidget(self._contentWidget)

        # set collapse state
        if isCollapsed:
            self.collapse()
        else:
            self.expand()

        # setup connections
        self.__setupConnections()

    def __setupConnections(self):
        """setup connections
        """

        # execute
        self._header.clicked.connect(self.toggleCollapse)

    # COMMANDS

    def addLayout(self, layout):
        """add layout to the CollapsibleWidget

        :param layout: layout to add to the CollapsibleWidget
        :type layout: :class:`PySide2.QtWidgets.QLayout`
        """

        # execute
        self._contentLayout.addLayout(layout)

    def addWidget(self, widget):
        """add widget to the CollapsibleWidget

        :param widget: widget to add to the CollapsibleWidget
        :type widget: :class:`PySide2.QtWidgets.QWidget`
        """

        # execute
        self._contentLayout.addWidget(widget)

    def collapse(self):
        """collapse the content of the CollapsibleWidget
        """

        # execute
        self._header.setIcon(_qtGui.Icon('arrow_plain_right_grey.png'))
        self._contentWidget.setHidden(True)
        self._isCollapsed = True

        # resize
        self.setMaximumHeight(self._titleHeight)

        # emit
        self.collapseChanged.emit(True)

    def contentWidget(self):
        """get the content widget

        :return: the content widget
        :rtype: :class:`PySide2.QtWidgets.QWidget`
        """

        # return
        return self._contentWidget

    def expand(self):
        """expand the content of the CollapsibleWidget
        """

        # execute
        self._header.setIcon(_qtGui.Icon('arrow_plain_down_grey.png'))
        self._contentWidget.setHidden(False)
        self._isCollapsed = False

        # resize
        self.setMaximumHeight(16777215)

        # emit
        self.collapseChanged.emit(False)

    def isCollapsed(self):
        """get the collapsed state of the CollapsibleWidget

        :return: the collapsed state
        :rtype: bool
        """

        # return
        return self._isCollapsed

    def toggleCollapse(self):
        """toggle collapse state of the CollapsibleWidget
        """

        # toggle
        if self._isCollapsed:
            self.expand()
        else:
            self.collapse()


class Tool(PySide2.QtWidgets.QWidget):
    """widget handling UI tool generic functionalities through subclass inheritance
    """

    # ATTRIBUTES #

    _object = None
    _name = NotImplemented

    # INIT #

    def __init__(self, parent=None):
        """Tool class initialization

        :param parent: parent under which the ui will be parented
        :type parent: :class:`PySide2.QtWidgets.QWidget`
        """

        # init
        super(Tool, self).__init__(parent=parent)

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

    # OBJECT COMMANDS #

    @classmethod
    def load(cls, *args, **kwargs):
        """load the tool with the arguments and keywords of the init
        """

        # store tool
        tool = cls(*args, **kwargs)

        # execute
        tool.show()

        # return
        return tool

    # COMMANDS #

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

    def setTitle(self, title=None):
        """set the title of the widget

        :param title: title of the widget to set - if nothing specified title will be -> name version
        :type title: str
        """

        # get title
        title = title or self.name().replace('_', ' ')

        # execute
        self.setObjectName(self.name)
        self.setWindowTitle(title)
