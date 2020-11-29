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

        :param text: text used to select the proper item
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
        """set the background color of the lineEdit using the specified color and pattern

        :param color: color to set - [R, V, B, A] - [0.8, 0.8, 0.8, 1] is default
        :type color: list[int, float]

        :param pattern: pattern of the background
        :type pattern: str
        """

        # init
        color = color or [0.8, 0.8, 0.8, 1]

        # error
        if pattern not in ['solid']:
            raise ValueError('{0} is not a pattern - [solid]'.format(pattern))

        # update color
        palette = PySide2.QtGui.QPalette(self.palette())
        palette.setColor(PySide2.QtGui.QPalette.Base, 
                         PySide2.QtGui.QColor.fromRgbF(*color))

        # update pattern
        brush = palette.brush(PySide2.QtGui.QPalette.Base)

        if pattern == 'solid':
            brush.setStyle(PySide2.QtCore.Qt.SolidPattern)

        palette.setBrush(PySide2.QtGui.QPalette.Base, brush)

        # set palette
        self.setPalette(palette)

    def setForeground(self, color=None):
        """set the foreground color of the lineEdit using the specified color and pattern

        :param color: color to set - [R, V, B, A] - [0.8, 0.8, 0.8, 1] is default
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
        """set the frame color of the lineEdit using the specified color

        :param color: color to set - [R, V, B, A] - [0.8, 0.8, 0.8, 1] is default
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

        :param widget: widget to add to the QListWidget
        :type widget: :class:`PySide2.QtWidgets.QWidget`
        """

        # create QListWidget item
        listItem = PySide2.QtWidgets.QListWidgetItem(self)
        listItem.setSizeHint(widget.size())

        # add item to QListWidget
        self.addItem(listItem)
        self.setItemWidget(listItem, widget)

        # update
        listItem.childwidget = widget
        widget.parentItem = listItem

    def childrenItems(self):
        """get the children items of the list

        :return: the list of children items
        :rtype: list[:class:`PySide2.QtWidgets.QListWidgetItem`]
        """

        # init
        data = []

        # execute
        for index in range(self.count()):
            data.append(self.item(index))

        # return
        return data


class PushButton(PySide2.QtWidgets.QPushButton):
    """QPushButton with custom functionalities
    """

    # COMMANDS #

    def setIcon(self, image):
        """set the icon on the QPushButton

        :param image: image to set on the QPushButton
        :type image: str
        """

        # init
        super(PushButton, self).setIcon(_qtGui.Icon(image))

    def setIconSize(self, width, height):
        """set the icon size

        :param width: width of the icon
        :type width: int

        :param height: height of the icon
        :type height: int
        """

        # init
        super(PushButton, self).setIconSize(PySide2.QtCore.QSize(width, height))


class TreeWidget(PySide2.QtWidgets.QTreeWidget):
    """QTreeWidget with custom functionalities
    """

    # COMMANDS #

    def childrenItems(self, recursive=False):
        """get the children items parented to the TreeWidget

        :param recursive: defines whether or not the command will get the children items recursively through hierarchy
        :type recursive: bool

        :return: list of children items
        :rtype: list[:class:`PySide2.QtWidgets.QTreeWidgetItem`, :class:`cgp_generic_utils.qt.TreeWidgetItem`]
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
        """clear the selection of the QTreeWidgetItem
        """

        # execute
        for item in self.selectedItems():
            item.setSelected(False)

    def resizeToContent(self, margin=0):
        """resize the list of specified tre widgets to content

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


class TreeWidgetItem(PySide2.QtWidgets.QTreeWidgetItem):
    """QTreeWidgetItem with custom functionalities
    """

    # INIT #

    def __init__(self, parent=None):
        """QTreeWidgetItem class initialization

        :param parent: QWidget under which the QTreeWidgetItem will be parented
        :type parent: :class:`PySide2.QtWidgets.QTreeWidget` or :class:`PySide2.QtWidgets.QTreeWidgetItem`
        """

        # init
        super(TreeWidgetItem, self).__init__(parent)

        # parent if specified
        if isinstance(parent, PySide2.QtWidgets.QTreeWidget) or isinstance(parent, TreeWidget):
            parent.addTopLevelItem(self)

        elif isinstance(parent, PySide2.QtWidgets.QTreeWidgetItem) or isinstance(parent, TreeWidgetItem):
            parent.addChild(self)

    # COMMANDS #

    def addWidget(self, widget, index):
        """add the specified widget to the specified column of the QTreeWidgetItem

        :param widget: widget to add the the QTreeWidgetItem
        :type widget: :class:`PySide2.QtWidgets.QWidget`

        :param index: index of the column where to add the widget
        :type index: int
        """

        # get treeWidget
        treeWidget = self.treeWidget()

        # errors
        if not treeWidget:
            raise UserWarning('can\'t add a widget to a TreeWidgetItem not docked to a TreeWidget')

        # set widget parent
        widget.setParent(treeWidget)

        # execute
        treeWidget.setItemWidget(self, index, widget)

    def childrenItems(self, recursive=False):
        """get the children items parented to the QTreeWidgetItem

        :param recursive: defines whether or not the command will get the children items recursively through hierarchy
        :type recursive: bool

        :return: list of children
        :rtype: list[:class:`PySide2.QtWidgets.QTreeWidgetItem`, :class:`cgp_generic_utils.qt.TreeWidgetItem`]
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

    def setBackgrounds(self, indexes, color=None, pattern='solid'):
        """set background colors of the columns of the specified indexes using the specified color and pattern

        :param indexes: list of the column indexes use to set the backgrounds
        :type indexes: list[int]

        :param color: color to set - [R, V, B, A] - [0.8, 0.8, 0.8, 1] is default
        :type color: list[int, float]

        :param pattern: pattern of the backgrounds
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
            self.setBackground(index, brush)

    def setFonts(self, indexes, size=9, styles=None):
        """set fonts of the columns of the specified indexes using the specified size and styles

        :param indexes: list of the column indexes use to set the fonts
        :type indexes: list[int]

        :param size: size of the font
        :type size: int

        :param styles: styles of the font - [bold - italic - underline]
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

    def setIcons(self, indexes, icon):
        """set the icon of the specified column of the custom QTreeWidgetItem

        :param indexes: index of the column to set the icon to
        :type indexes: list

        :param icon: name of the icon to set
        :type icon: str
        """

        # execute
        for index in indexes:
            self.setIcon(index, _qtGui.Icon(icon))

    def setForegrounds(self, indexes, color=None, pattern='solid'):
        """set foreground colors of the columns of the specified indexes using the specified color and pattern

        :param indexes: list of the column indexes use to set the foregrounds
        :type indexes: list[int]

        :param color: color to set - [R, V, B, A] - [0.8, 0.8, 0.8, 1] is default
        :type color: list[int, float]

        :param pattern: pattern of the foregrounds
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

    def setSelectable(self, isSelectable):
        """set the status flags of the item

        :param isSelectable: defines whether or not the item is selectable
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
        """set texts in the specified column using the specified texts

        :param texts: dictionary holding column indexes and texts to set - {0: 'text1', 2:'text2' ...}
        :type texts: dict[int: str]
        """

        # execute
        for index in texts:
            self.setText(index, texts[index])
