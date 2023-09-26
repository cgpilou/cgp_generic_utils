"""
qtWidgets object library
"""

# imports third-parties
import PySide2.QtWidgets
import PySide2.QtGui
import PySide2.QtCore

# imports rodeo
import cgp_generic_utils.python
import cgp_generic_utils.constants
from . import _qtGui


class ComboBox(PySide2.QtWidgets.QComboBox):
    """QComboBox with custom functionalities
    """

    # COMMANDS #

    def goTo(self, text):
        """go to the item with the specified text

        :param text: the text of the item to go to
        :type text: str
        """

        # execute
        value = self.findText(text)
        self.setCurrentIndex(value)


class LineEdit(PySide2.QtWidgets.QLineEdit):
    """QLineEdit with custom functionalities
    """

    # COMMANDS #

    def setBackground(self, color=None, pattern='solid'):
        """set the background color of the lineEdit

        :param color: the color to set - ``[R, V, B, A]`` - default is ``[0.8, 0.8, 0.8, 1]``
        :type color: list[int, float]

        :param pattern: the pattern of the background
        :type pattern: str
        """

        # init
        color = color or [0.8, 0.8, 0.8, 1]

        # error
        if pattern not in ['solid']:
            raise ValueError('{0} is not a pattern - [solid]'.format(pattern))

        # update color
        palette = PySide2.QtGui.QPalette(self.palette())
        palette.setColor(PySide2.QtGui.QPalette.Base, PySide2.QtGui.QColor.fromRgbF(*color))

        # update pattern
        brush = palette.brush(PySide2.QtGui.QPalette.Base)

        if pattern == 'solid':
            brush.setStyle(PySide2.QtCore.Qt.SolidPattern)

        palette.setBrush(PySide2.QtGui.QPalette.Base, brush)

        # set palette
        self.setPalette(palette)

    def setForeground(self, color=None):
        """set the foreground color of the lineEdit

        :param color: the color to set - ``[R, V, B, A]`` - default is ``[0.8, 0.8, 0.8, 1]``
        :type color: list[int, float]
        """

        # init
        color = color or [0.8, 0.8, 0.8, 1]

        # update color
        palette = PySide2.QtGui.QPalette(self.palette())
        palette.setColor(PySide2.QtGui.QPalette.Text, PySide2.QtGui.QColor.fromRgbF(*color))

        # set palette
        self.setPalette(palette)

    def setFrameColor(self, color=None):
        """set the frame color of the lineEdit

        :param color: the color to set - ``[R, V, B, A]`` - default is ``[0.8, 0.8, 0.8, 1]``
        :type color: list[int, float]
        """

        # init
        color = color or [0.8, 0.8, 0.8, 1]

        # build palette
        palette = PySide2.QtGui.QPalette()
        self.setBackgroundRole(palette.Window)
        palette.setColor(self.backgroundRole(), PySide2.QtGui.QColor.fromRgbF(*color))

        # set palette
        self.setPalette(palette)


class ListWidget(PySide2.QtWidgets.QListWidget):
    """QListWidget with custom functionalities
    """

    # COMMANDS #

    def addWidget(self, widget):
        """add widget to the QListWidget

        :param widget: the widget to add to the QListWidget
        :type widget: :class:`PySide2.QtWidgets.QWidget`
        """

        # create QListWidget item
        listItem = PySide2.QtWidgets.QListWidgetItem(self)
        listItem.setSizeHint(widget.size())

        # add item to QListWidget
        self.addItem(listItem)
        self.setItemWidget(listItem, widget)

        # update
        listItem.childWidget = widget
        widget.parentItem = listItem

    def childrenItems(self):
        """get the children items of the list

        :return: the children items of the listWidget
        :rtype: list[:class:`PySide2.QtWidgets.QListWidgetItem`]
        """

        # init
        data = []

        # execute
        for index in range(self.count()):
            data.append(self.item(index))

        # return
        return data


class Menu(PySide2.QtWidgets.QMenu):
    """QMenu with custom functionalities
    """

    # COMMANDS #

    def createAction(self, text, icon=None, triggeredCommand=None, shortcut=None):
        """create an action and add it to the menu

        :param text: the text of the action
        :type text: str

        :param icon: the icon of the action
        :type icon: str

        :param triggeredCommand: the command triggered by the action
        :type triggeredCommand: python

        :param shortcut: the shortcut keys combo associated to the action - written as text - ``[ex: 'Ctrl+C']``
        :type shortcut: str

        :return: the created action
        :rtype: :class:`PySide2.QtWidgets.QAction`
        """

        # create QAction
        action = PySide2.QtWidgets.QAction(self)

        # set action text
        action.setText(text)

        # set the shortcut text
        if shortcut:
            action.setShortcut(shortcut)

        # set icon
        if icon:
            action.setIcon(_qtGui.Icon(icon))

        # connect trigger signal
        if triggeredCommand:
            action.triggered.connect(triggeredCommand)

        # add action to menu
        self.addAction(action)

        # return
        return action


class ProgressBar(PySide2.QtWidgets.QWidget):
    """QProgressBar with custom functionalities - encapsulated in QWidget to offer better text management
    """

    # INIT #

    def __init__(self, barWidth=None, hasText=True, parent=None):
        """ProgressBar class initialization

        :param barWidth: the width of the progressBar
        :type barWidth: int

        :param hasText: ``True`` : the widget has a text widget - ``False`` : the widget doesn't have a text widget
        :type hasText: bool

        :param parent: the QWidget to parent the progressBar to
        :type parent: :class:`PySide2.QtWidgets.QWidget`
        """

        # init
        super(ProgressBar, self).__init__(parent=parent)

        # main layout
        self.mainLayout = PySide2.QtWidgets.QHBoxLayout(self)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.mainLayout)

        # progress bar
        self.progressBar = PySide2.QtWidgets.QProgressBar(self)

        if barWidth:
            self.progressBar.setFixedWidth(barWidth)

        # text widget
        self.textWidget = PySide2.QtWidgets.QLabel(self)
        self.textWidget.setSizePolicy(PySide2.QtWidgets.QSizePolicy.Expanding,
                                      PySide2.QtWidgets.QSizePolicy.Fixed)

        # add widgets to layout
        for widget in [self.progressBar, self.textWidget]:
            self.mainLayout.addWidget(widget)

        # set text widget status
        self.textWidget.setHidden(not hasText)

    # COMMANDS #

    def setText(self, text):
        """set the text of the progressBar

        :param text: the text to set on the progressBar
        :type text: str
        """

        # execute
        self.textWidget.setText(text)

    def setValue(self, value):
        """set the value of the progressBar

        :param value: the value to set on the progressBar
        :type value: float
        """

        # execute
        self.progressBar.setValue(value)


class PushButton(PySide2.QtWidgets.QPushButton):
    """QPushButton with custom functionalities
    """

    # COMMANDS #

    def setIcon(self, image):
        """set the icon on the pushButton

        :param image: image to set on the pushButton
        :type image: str
        """

        # execute
        super(PushButton, self).setIcon(_qtGui.Icon(image))

    def setIconSize(self, width, height):
        """set the size of the icon

        :param width: the icon width
        :type width: int

        :param height: the icon height
        :type height: int
        """

        # execute
        super(PushButton, self).setIconSize(PySide2.QtCore.QSize(width, height))


class TreeWidget(PySide2.QtWidgets.QTreeWidget):
    """QTreeWidget with custom functionalities
    """

    # INIT #

    def __init__(self, parent=None):
        """TreeWidget class initialization

        :param parent: the QWidget to parent the TreeWidget to
        :type parent: :class:`PySide2.QtWidget.QWidget`
        """

        # init
        super(TreeWidget, self).__init__(parent=parent)

        # setup connections
        self.__setupConnections()

    # COMMANDS #

    def childrenItems(self, recursive=False):
        """get the children items parented to the treeWidget

        :param recursive: ``True`` : the command gets the children items recursively through hierarchy -
                          ``False`` : the commands gets only the direct children items
        :type recursive: bool

        :return: the children items
        :rtype: list[:class:`PySide2.QtWidgets.QTreeWidgetItem`]
        """

        # init
        children = []

        # get the list of topLevelItems
        topLevelItems = [self.topLevelItem(iIndex) for iIndex in range(self.topLevelItemCount())]
        children.extend(topLevelItems)

        # get the rest if specified
        if recursive:
            for topLevelItem in topLevelItems:
                children.extend(topLevelItem.childrenItems(recursive=True))

        # return
        return children

    def clearSelection(self):
        """clear the selection of the treeWidget
        """

        # execute
        for item in self.selectedItems():
            item.setSelected(False)

    def resizeToContent(self, margin=0):
        """resize the treeWidget to content

        :param margin: margin within the columns
        :type margin: int
        """

        # get number of columns
        columnCount = self.columnCount()

        # resize
        for index in range(columnCount):

            # resize to content
            self.resizeColumnToContents(index)

            # get column current size
            currentSize = self.columnWidth(index)

            # apply margin
            self.setColumnWidth(index, currentSize + margin)

    def toggleExpand(self, item):
        """toggle the expand state of the item. If shift is pressed, children expand states are matched to the item expand state

        :param item: the item to toggle the expand state to
        :type: :class:`PySide2.QtWidgets.QTreeWidgetItem`
        """

        # get application modifiers
        modifiers = PySide2.QtGui.QGuiApplication.keyboardModifiers()

        # match children expand states if shift is pressed
        if modifiers == PySide2.QtCore.Qt.ShiftModifier:
            state = item.isExpanded()

            for child in item.childrenItems(recursive=True):
                child.setExpanded(state)

    def setSelectedItems(self, items):
        """set the selectedItems of the TreeWidget

        :param items: items to set as selectedItems
        :type items: list[:class:`PySide2.QtWidgets.QTreeWidgetItem`]
        """

        # init
        toSelect = []
        toUnselect = []

        # parse current selection states
        for child in self.childrenItems(recursive=True):

            # ignore items with correct selection status
            needSelection = child in items
            if child.isSelected() == needSelection:
                continue

            # collect items to select
            if needSelection:
                toSelect.append(child)

            # collect items to unselect
            else:
                toUnselect.append(child)

        # select needed items
        for item in toSelect:
            item.setSelected(True)

        # unselect needed items
        for item in toUnselect:
            item.setSelected(False)

    # PRIVATE COMMANDS #

    def __setupConnections(self):
        """setup connections
        """

        # set connections
        self.itemExpanded.connect(self.toggleExpand)
        self.itemCollapsed.connect(self.toggleExpand)


class TreeWidgetItem(PySide2.QtWidgets.QTreeWidgetItem):
    """QTreeWidgetItem with custom functionalities
    """

    # INIT #

    def __init__(self, parent=None):
        """TreeWidgetItem class initialization

        :param parent: the QWidget under which the QTreeWidgetItem will be parented
        :type parent: :class:`PySide2.QtWidgets.QTreeWidget` or :class:`PySide2.QtWidgets.QTreeWidgetItem`
        """

        # init
        super(TreeWidgetItem, self).__init__(parent)

        # parent if specified
        if isinstance(parent, (PySide2.QtWidgets.QTreeWidget, TreeWidget)):
            parent.addTopLevelItem(self)

        elif isinstance(parent, (PySide2.QtWidgets.QTreeWidgetItem, TreeWidgetItem)):
            parent.addChild(self)

    # COMMANDS #

    def addWidget(self, widget, index=0):
        """add the widget to the indexed column of the treeWidgetItem

        :param widget: the widget to add to the treeWidgetItem
        :type widget: :class:`PySide2.QtWidgets.QWidget`

        :param index: the index of the column where to add the widget - default is first column
        :type index: int
        """

        # init
        treeWidget = self.treeWidget()

        # set widget parent
        widget.setParent(treeWidget)

        # execute
        treeWidget.setItemWidget(self, index, widget)

    def childrenItems(self, recursive=False):
        """get the children items parented to the treeWidgetItem

        :param recursive: ``True`` : the command gets the children items recursively through hierarchy -
                          ``False`` : the commands gets only the direct children items
        :type recursive: bool

        :return: the children items
        :rtype: list[:class:`PySide2.QtWidgets.QTreeWidgetItem`]
        """

        # init
        children = []
        tempList = [self]
        toIterate = []

        # recursive mode
        while len(tempList):
            for item in tempList:
                for index in range(item.childCount()):
                    children.append(item.child(index))
                    toIterate.append(item.child(index))
            if recursive:
                tempList = toIterate
                toIterate = []
            else:
                tempList = []

        # return
        return children

    def index(self):
        """get the index of the TreeWidgetItem

        :return: the index of the TreeWidgetItem
        :rtype: int
        """

        # get parent and treeWidget
        parent = self.parent()
        treeWidget = self.treeWidget()

        # return (if the item has no parent, it's a top level item)
        return treeWidget.indexOfTopLevelItem(self) if parent is None else parent.indexOfChild(self)

    def level(self):
        """get the level of the TreeWidgetItem

        :return: the level of the TreeWidgetItem
        :rtype: int
        """

        # init
        parent = self.parent()
        level = 0

        # execute
        while parent:
            level += 1
            parent = parent.parent()

        # return
        return level

    def nextItem(self):
        """get the item following the TreeWidgetItem (at the same level of the TreeWidget)

        :return: the tree item following the TreeWidgetItem
        :rtype: :class:`PySide2.QtWidgets.QTreeWidgetItem`
        """

        # get parent, index and treeWidget
        treeWidget = self.treeWidget()
        index = self.index()
        parent = self.parent()

        # return
        if parent:
            return parent.child(index + 1) if index < parent.childCount() - 1 else None
        return treeWidget.topLevelItem(index + 1) if index < treeWidget.topLevelItemCount() - 1 else None

    def previousItem(self):
        """get the item above the TreeWidgetItem (at the same level of the TreeWidget)

        :return: get the item above the TreeWidgetItem
        :rtype: :class:`PySide2.QtWidgets.QTreeWidgetItem`
        """

        # get parent, index and treeWidget
        treeWidget = self.treeWidget()
        index = self.index()
        parent = self.parent()

        # return
        if parent:
            return parent.child(index - 1) if index > 0 else None
        return treeWidget.topLevelItem(index - 1) if index > 0 else None

    def removeWidget(self, index=0):
        """remove the widget of a column of the TreeWidgetItem

        :param index: the index of the column to remove the widget from - default is first column
        :param index: int
        """

        # execute
        self.treeWidget().removeItemWidget(self, index)

    def setBackgrounds(self, indexes=None, color=None, pattern='solid'):
        """set the background of the index columns

        :param indexes: the indexes used to set the backgrounds - default is all columns
        :type indexes: list[int]

        :param color: the color to set - ``[R, V, B, A]`` - default is ``[0.8, 0.8, 0.8, 1]``
        :type color: list[float]

        :param pattern: the pattern of the backgrounds
        :type pattern: str
        """

        # init
        indexes = indexes or [index for index in range(self.columnCount())]
        color = color or [0.8, 0.8, 0.8, 1]

        # error
        if pattern not in ['solid']:
            raise ValueError('{0} is not a pattern - [solid]'.format(pattern))

        # create brush with pattern
        if pattern == 'solid':
            pattern = PySide2.QtCore.Qt.SolidPattern

        brush = PySide2.QtGui.QBrush(pattern)

        # set brush color
        brush.setColor(PySide2.QtGui.QColor.fromRgbF(*color))

        # execute
        for index in indexes:
            self.setBackground(index, brush)

    def setFonts(self, indexes, size=9, styles=None):
        """set the fonts of the index columns

        :param indexes: the column indexes used to set the fonts
        :type indexes: list[int]

        :param size: the size of the font
        :type size: int

        :param styles: the styles of the font - ``[bold - italic - underline]``
        :type: list[:class:`cgp_generic_utils.constants.TypoStyle`]
        """

        # error
        for style in styles:
            if style not in cgp_generic_utils.constants.TypoStyle.ALL:
                raise ValueError('{0} is not a style - {1}'.format(style, cgp_generic_utils.constants.TypoStyle.ALL))

        # create font
        font = _qtGui.Font(size, styles)

        # set fonts
        for index in indexes:
            self.setFont(index, font)

    def setForegrounds(self, indexes, color=None, pattern='solid'):
        """set the foreground colors of the index columns

        :param indexes: the column indexes used to set the foregrounds
        :type indexes: list[int]

        :param color: color to set - ``[R, V, B, A]`` - default is ``[0.8, 0.8, 0.8, 1]``
        :type color: list[int, float]

        :param pattern: the pattern of the foregrounds
        :type pattern: str
        """

        # init
        color = color or [0.8, 0.8, 0.8, 1]

        # error
        if pattern not in ['solid']:
            raise ValueError('{0} is not a pattern - [solid]'.format(pattern))

        # create brush with pattern
        if pattern == 'solid':
            pattern = PySide2.QtCore.Qt.SolidPattern

        brush = PySide2.QtGui.QBrush(pattern)

        # set brush color
        brush.setColor(PySide2.QtGui.QColor.fromRgbF(*color))

        # execute
        for index in indexes:
            self.setForeground(index, brush)

    def setIcons(self, indexes, icon):
        """set the icon of the index columns

        :param indexes: the column indexes used to set the icons
        :type indexes: list[int]

        :param icon: the name of the icon to set
        :type icon: str
        """

        # execute
        for index in indexes:
            self.setIcon(index, _qtGui.Icon(icon))

    def setSelectable(self, isSelectable):
        """set the selection status of the treeWidgetItem

        :param isSelectable: ``True`` : the item is selectable - ``False`` : the item is not selectable
        :type isSelectable: bool
        """

        # init
        flags = PySide2.QtCore.Qt.ItemIsEnabled

        # if selectable
        if isSelectable:
            flags |= PySide2.QtCore.Qt.ItemIsSelectable

        # set flags
        self.setFlags(flags)

        # unselect item
        self.setSelected(False)

    def setTexts(self, texts):
        """set the texts of the index columns

        :param texts: the indexes and texts to set on the columns - ``{0: 'text1', 2:'text2' ...}``
        :type : dict
        """

        # execute
        for index in texts:
            self.setText(index, texts[index])

    def take(self):
        """take the item out of the TreeWidget
        """

        # get the child index
        index = self.index()

        # get the parent
        parent = self.parent()

        # take the item
        if parent is None:
            self.treeWidget().takeTopLevelItem(index)
        else:
            parent.takeChild(index)

    def widget(self, index=0):
        """get the widget associated to a column of the TreeWidgetItem

        :param index: the index of the column to get the widget from - default is first column
        :param index: int

        :return: the widget associated to a column of the TreeWidgetItem
        :rtype: :class:`Pyside2.QtWidgets.QWidget`
        """

        # return
        return self.treeWidget().itemWidget(self, index)
