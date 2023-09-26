"""
dialog library
"""

# imports python
import collections
import time

# imports third-parties
import PySide2.QtWidgets
import PySide2.QtGui
import PySide2.QtCore

# imports local
import cgp_generic_utils.python
import cgp_generic_utils.constants
from . import _qtGui
from . import _qtWidgets


# BASE OBJECTS #


class BaseDialog(PySide2.QtWidgets.QDialog):
    """basic dialog with ok and cancel button
    """

    # INIT #

    def __init__(self, title, label, size=None, parent=None, isFrameless=False, orientation=None):
        """BaseDialog class initialization

        :param title: the title of the dialog
        :type title: str

        :param label: the label of the dialog
        :type label: str

        :param size: the size of the dialog - ``[width, height]`` - default is ``[None, None]``
        :type size: list[int]

        :param parent: the QWidget to parent the dialog to
        :type parent: :class:`PySide2.QtWidgets.QWidget`

        :param isFrameless: ``True`` : the dialog is frameless - ``False`` : the dialog has a frame
        :type isFrameless: bool

        :param orientation: the orientation of the content layout - 
                            default is ``cgp_generic_utils.constants.Orientation.VERTICAL``
        :type orientation: :class:`cgp_generic_utils.constants.Orientation`
        """

        # init
        orientation = orientation or cgp_generic_utils.constants.Orientation.VERTICAL
        size = size or [None, None]

        # errors
        if orientation not in cgp_generic_utils.constants.Orientation.ALL:
            raise ValueError('{0} is an invalid orientation ! {1}'
                             .format(orientation, cgp_generic_utils.constants.Orientation.ALL))

        # init
        PySide2.QtWidgets.QDialog.__init__(self, parent)
        self.setWindowTitle(title)
        self._isValid = False

        # set frame
        if isFrameless:
            self.setWindowFlags(self.windowFlags() | PySide2.QtCore.Qt.FramelessWindowHint)

        # set parameters
        self.setFocusPolicy(PySide2.QtCore.Qt.StrongFocus)

        if size[0]:
            self.setFixedWidth(size[0])
        if size[1]:
            self.setFixedHeight(size[1])

        # vertical layout
        self.__verticalLayout = PySide2.QtWidgets.QVBoxLayout(self)

        # label
        self.__label = PySide2.QtWidgets.QLabel(self)
        sizepolicy = PySide2.QtWidgets.QSizePolicy(PySide2.QtWidgets.QSizePolicy.Preferred,
                                                   PySide2.QtWidgets.QSizePolicy.Fixed)
        self.__label.setSizePolicy(sizepolicy)
        self.__label.setMinimumSize(PySide2.QtCore.QSize(0, 25))
        self.__label.setAlignment(PySide2.QtCore.Qt.AlignCenter)
        self.__verticalLayout.addWidget(self.__label)
        self.__label.setText(label)

        # content layout
        if orientation == cgp_generic_utils.constants.Orientation.VERTICAL:
            self.__contentLayout = PySide2.QtWidgets.QVBoxLayout(self)
        else:
            self.__contentLayout = PySide2.QtWidgets.QHBoxLayout(self)

        self.__verticalLayout.addLayout(self.__contentLayout)

        # spacer 01
        spacerItem_01 = PySide2.QtWidgets.QSpacerItem(20, 10,
                                                      PySide2.QtWidgets.QSizePolicy.Minimum,
                                                      PySide2.QtWidgets.QSizePolicy.Expanding)
        self.__verticalLayout.addItem(spacerItem_01)

        # horizontal layout
        self.__buttonLayout = PySide2.QtWidgets.QHBoxLayout()
        self.__verticalLayout.addLayout(self.__buttonLayout)

        # spacer 02
        spacerItem_02 = PySide2.QtWidgets.QSpacerItem(40, 20,
                                                      PySide2.QtWidgets.QSizePolicy.Expanding,
                                                      PySide2.QtWidgets.QSizePolicy.Minimum)
        self.__buttonLayout.addItem(spacerItem_02)

        # ok button
        self.__ok_b = PySide2.QtWidgets.QPushButton(self)
        self.__ok_b.setMinimumSize(PySide2.QtCore.QSize(0, 30))
        self.__buttonLayout.addWidget(self.__ok_b)
        self.setOkButton()

        # cancel button
        self.__cancel_b = PySide2.QtWidgets.QPushButton(self)
        self.__cancel_b.setMinimumSize(PySide2.QtCore.QSize(0, 30))
        self.__buttonLayout.addWidget(self.__cancel_b)
        self.setCancelButton()

        # spacer 03
        spacerItem_03 = PySide2.QtWidgets.QSpacerItem(40, 20,
                                                      PySide2.QtWidgets.QSizePolicy.Expanding,
                                                      PySide2.QtWidgets.QSizePolicy.Minimum)
        self.__buttonLayout.addItem(spacerItem_03)

        # set in space
        if not parent:
            cursorPosition = PySide2.QtGui.QCursor.pos()
            self.move(cursorPosition)

        # setup connections
        self.__setupConnections()

    def __setupConnections(self):
        """setup the connections of the widgets
        """

        # execute
        self.__ok_b.clicked.connect(self.accept)
        self.__cancel_b.clicked.connect(self.reject)

    # COMMANDS #

    def label(self):
        """get the label of the dialog

        :return: the label of the dialog
        :rtype: :class:`PySide2.QtWidgets.QLabel`
        """

        # return
        return self.__label

    def buttonLayout(self):
        """get the button layout

        :return: the button layout
        :rtype: :class:`PySide2.QtWidget.QBoxLayout`
        """

        # return
        return self.__buttonLayout

    def contentLayout(self):
        """get the content layout

        :return: the content layout
        :rtype: :class:`PySide2.QtWidget.QBoxLayout`
        """

        # return
        return self.__contentLayout

    def isValid(self):
        """check if the dialog is valid

        :return: ``True`` : it is valid - ``False`` : it is not valid
        :rtype: bool
        """

        # return
        return self._isValid

    def keyPressEvent(self, event):
        """override keyPressEvent
        """

        # escape
        if event.key() == PySide2.QtCore.Qt.Key_Escape:
            self.reject()

        # enter
        elif event.key() in [PySide2.QtCore.Qt.Key_Return, PySide2.QtCore.Qt.Key_Enter] and self.isValid():
            self.accept()

    def load(self):
        """load the dialog

        :return: ``cancel`` : self.rejection - ``ok`` : self.validation
        :rtype: any
        """

        # return
        return self._validation() if self.exec_() else self._rejection()

    def setButtonDisplayed(self, isOkDisplayed=True, isCancelDisplayed=True):
        """set the display status of the buttons

        :param isOkDisplayed: ``True`` : ok button is displayed - ``False`` : ok button is hidden
        :type isOkDisplayed: bool

        :param isCancelDisplayed: ``True`` : cancel button is displayed - ``False`` : cancel button is hidden
        :type isCancelDisplayed: bool
        """

        # execute
        self.__ok_b.setHidden(not isOkDisplayed)
        self.__cancel_b.setHidden(not isCancelDisplayed)

    def setCancelButton(self, text=None):
        """set the text of the cancel button

        :param text: the text to set on the cancel button
        :type text: str
        """

        # get text
        text = text or 'Cancel'

        # set text
        self.__cancel_b.setText(text)

    def setOkButton(self, text=None):
        """set the test of the okButton

        :param text: the text to set on the ok button
        :type text: str
        """

        # get text
        text = text or 'Ok'

        # set text
        self.__ok_b.setText(text)

    def setStatus(self, okEnabled=True):
        """set the status of the okButton

        :param okEnabled: ``True`` : the okButton is enabled - ``False`` : the okButton is disabled
        :type okEnabled: bool
        """

        # execute
        self._isValid = okEnabled
        self.__ok_b.setEnabled(okEnabled)

    def setSize(self, size):
        """set the size of the dialog

        :param size: the size of the dialog - ``[width, height]``
        :type size: list[int]
        """

        # return
        if not size[0] and not size[1]:
            return

        # get current geometry
        geometry = self.geometry()

        # execute
        if not size[0]:
            self.setGeometry(geometry.x(), geometry.y(), 240, size[1])

        elif not size[1]:
            self.setGeometry(geometry.x(), geometry.y(), size[0], 100)

        else:
            self.setGeometry(geometry.x(), geometry.y(), size[0], size[0])

    # PRIVATE COMMANDS #

    def _rejection(self):
        """get the result of the dialog when ``cancel`` is pressed

        :return: the rejection of the dialog
        :rtype: any
        """

        # execute
        return None

    def _validation(self):
        """get the result of the dialog when ``ok`` is pressed

        :return: the validation of the dialog
        :rtype: any
        """

        # execute
        return True


# DIALOG OBJECTS #


class CheckBoxDialog(BaseDialog):
    """dialog with checkbox checking
    """

    # INIT #

    def __init__(self, title, label, data, size=None, parent=None, isFrameless=False):
        """CheckBoxDialog class initialization

        :param title: the title of the dialog
        :type title: str

        :param label: the label of the dialog
        :type label: str

        :param data: the data used to build the checkBoxes - ``{label1: True, label2: False}``
        :type data: dict

        :param size: the size of the dialog - ``[width, height]`` - default is ``[None, None]``
        :type size: list[int]

        :param parent: the QWidget to parent the dialog to
        :type parent: :class:`PySide2.QtWidgets.QWidget`

        :param isFrameless: ``True`` : the dialog is frameless - ``False`` : the dialog has a frame
        :type isFrameless: bool
        """

        # init
        size = size or [None, None]

        super(CheckBoxDialog, self).__init__(title,
                                             label,
                                             size=size,
                                             parent=parent,
                                             isFrameless=isFrameless,
                                             orientation=cgp_generic_utils.constants.Orientation.HORIZONTAL)

        self.__data = data
        self.__checkboxes = []

        # add spacer
        spacer = PySide2.QtWidgets.QSpacerItem(10, 10,
                                               PySide2.QtWidgets.QSizePolicy.Expanding,
                                               PySide2.QtWidgets.QSizePolicy.Expanding)
        self.contentLayout().addItem(spacer)

        # create checkBoxes
        for checkLabel, isChecked in data.items():
            self.addCheckbox(checkLabel, isChecked)

        # add spacer
        spacer = PySide2.QtWidgets.QSpacerItem(10, 10,
                                               PySide2.QtWidgets.QSizePolicy.Expanding,
                                               PySide2.QtWidgets.QSizePolicy.Expanding)
        self.contentLayout().addItem(spacer)

    # COMMANDS #

    def addCheckbox(self, label, isChecked):
        """add a new checkBox to the dialog

        :param label: the label of the checkbox
        :type label: str

        :param isChecked: ``True`` : the checkbox is checked - ``False`` : the checkbox is not checked
        :type isChecked: bool

        :return: the created checkbox
        :rtype: :class:`PySide2.QtWidgets.QCheckBox`
        """

        # execute
        checkbox = PySide2.QtWidgets.QCheckBox(self)
        checkbox.setText(label)
        checkbox.setChecked(isChecked)
        self.contentLayout().addWidget(checkbox)

        # update
        self.__checkboxes.append(checkbox)

    # PRIVATE COMMANDS #

    def _validation(self):
        """get the result of the dialog when ``ok`` is pressed

        :return: ``Cancel`` : None - ``Ok`` : {checkBoxLabel1: isChecked1, checkBoxLabel2: isChecked2 ...}
        :rtype: dict or None
        """

        # init
        data = collections.OrderedDict()

        # get content
        for checkbox in self.__checkboxes:
            data[str(checkbox.text())] = checkbox.isChecked()

        # return
        return data or None


class ComboBoxDialog(BaseDialog):
    """dialog with combobox selection
    """

    # INIT #

    def __init__(self, title, label, data, entryLabelWidth=35, size=None,
                 parent=None, isFrameless=False, orientation=None):
        """ComboBoxDialog class initialization

        :param title: the title of the dialog
        :type title: str

        :param label: the label of the dialog
        :type label: str

        :param data: the data used to build the comboBoxes - ``[[label1, [itemA, itemB ...]], [label2, [...]], ...]``
        :type data: list[list[str, list[str]]]

        :param entryLabelWidth: the with of the label of the combobox entries
        :type entryLabelWidth: int

        :param size: the size of the dialog - ``[width, height]`` - default is ``[None, None]``
        :type size: list[int]

        :param parent: the QWidget to parent the lineEdit dialog to
        :type parent: :class:`PySide2.QtWidgets.QWidget`

        :param isFrameless: ``True`` : the dialog is frameless - ``False`` : the dialog has a frame
        :type isFrameless: bool

        :param orientation: defines the orientation of the content layout -
                            default is ``cgp_generic_utils.constants.Orientation.VERTICAL``
        :type orientation: :class:`cgp_generic_utils.constants.Orientation`
        """

        # init
        size = size or [None, None]
        orientation = orientation or cgp_generic_utils.constants.Orientation.VERTICAL

        super(ComboBoxDialog, self).__init__(title, label, size=size, parent=parent,
                                             isFrameless=isFrameless, orientation=orientation)

        self.__data = data
        self.__entryLabelWidth = entryLabelWidth
        self.__comboboxes = []

        # create comboBoxes
        for comboLabel, comboItems in data:
            self.addCombobox(comboLabel, comboItems)

    # COMMAND #

    def addCombobox(self, label, items):
        """add a new check box to the dialog

        :param label: label of the combobox
        :type label: str

        :param items: items of the combobox
        :type items: list[str]
        """

        # content layout
        contentLayout = PySide2.QtWidgets.QHBoxLayout(self)
        contentLayout.setContentsMargins(0, 0, 0, 0)
        contentLayout.setSpacing(6)
        self.contentLayout().addLayout(contentLayout)

        # label
        if label:
            entryLabel = PySide2.QtWidgets.QLabel(self)
            entryLabel.setAlignment(PySide2.QtCore.Qt.AlignRight | PySide2.QtCore.Qt.AlignVCenter)
            entryLabel.setText(label)
            entryLabel.setFixedWidth(self.__entryLabelWidth)
            contentLayout.addWidget(entryLabel)

        # combobox
        entryCombobox = PySide2.QtWidgets.QComboBox(self)
        entryCombobox.addItems(items)
        contentLayout.addWidget(entryCombobox)

        # update
        self.__comboboxes.append(entryCombobox)

    def comboBoxes(self):
        """get the combo boxes of the ComboBoxDialog

        :return: the combo boxes
        :rtype: :class:`PySide2.QtWidgets.QCombobox`
        """

        # return
        return self.__comboboxes

    # PRIVATE COMMANDS #

    def _validation(self):
        """result of the dialog when ``ok`` is pressed

        :return: Cancel : None - Ok : list of combobox currentTexts
        :rtype: list[str] or None
        """

        # return
        return [str(combobox.currentText()) for combobox in self.__comboboxes]


class ComboBoxLineEditDialog(BaseDialog):
    """dialog with combobox selection and lineEdit filling
    """

    # INIT #

    def __init__(self, 
                 title, 
                 label, 
                 items, 
                 defaultItem=None, 
                 icons=None, 
                 iconSize=None, 
                 text=None, 
                 comboSeparator=None,
                 separator=None, 
                 concatenateResult=True, 
                 size=None, 
                 parent=None, 
                 isFrameless=False):
        """ComboBoxLineEditDialog class initialization

        :param title: the title of the dialog
        :type title: str

        :param label: the label of the dialog
        :type label: str

        :param icons: the icons used to populate the combobox
        :type icons: list[str]

        :param iconSize: the size of the icons - default is ``[10, 10]``
        :type iconSize: list[int]

        :param items: the item used to populate the combobox
        :type items: list[str]

        :param defaultItem: the selected default item at the opening of the dialog
        :type defaultItem: str

        :param text: the text that will be displayed in the lineEdit at initialization
        :type text: str

        :param comboSeparator: the separator used to split comboBox content if specified
        :type comboSeparator: str

        :param separator: the separator used when merging current comboBox item with lineEdit text
        :type separator: str

        :param concatenateResult: ``True`` : result will be concatenated between comboBox and lineEdit - 
                                  ``False`` : result will not be concatenated between comboBox and lineEdit
        :type concatenateResult: bool

        :param size: the size of the dialog - ``[width, height]`` - default is ``[None, None]``
        :type size: list[int]

        :param parent: the QWidget to parent the dialog to
        :type parent: :class:`PySide2.QtWidgets.QWidget`

        :param isFrameless: ``True`` : the dialog is frameless - ``False`` : the dialog has a frame
        :type isFrameless: bool
        """

        # init
        iconSize = iconSize or [10, 10]
        size = size or [None, None]

        super(ComboBoxLineEditDialog, self).__init__(title,
                                                     label,
                                                     size=size,
                                                     parent=parent,
                                                     isFrameless=isFrameless,
                                                     orientation=cgp_generic_utils.constants.Orientation.VERTICAL)

        self.__items = items
        self.__icons = icons
        self.__iconSize = iconSize
        self.__concatenateResult = concatenateResult

        # define separator
        self.__separator = separator or ''

        # define comboSeparator
        self.__comboSeparator = comboSeparator or None

        # layout
        self.__layout = PySide2.QtWidgets.QHBoxLayout(self)
        self.contentLayout().addLayout(self.__layout)

        # combobox
        self.__combobox = cgp_generic_utils.qt.ComboBox(self)
        self.setItems(items=self.__items)
        self.__layout.addWidget(self.__combobox)

        if self.__icons:
            self.setIcons(self.__icons)

        if defaultItem and defaultItem in items:
            self.__combobox.goTo(defaultItem)

        # line Edit
        self.__lineEdit = PySide2.QtWidgets.QLineEdit(self)
        self.setText(text=text)
        self.__layout.addWidget(self.__lineEdit)

        # set ok button status
        self._setOkStatus()

        # setup connections
        self._setupConnections()

    def _setupConnections(self):
        """setup the connections of the widgets
        """

        # execute
        self.__lineEdit.textChanged.connect(self._setOkStatus)

    # COMMANDS #

    def lineEdit(self):
        """get the lineEdit of the dialog

        :return: the lineEdit of the dialog
        :rtype: :class:`PySide2.QtWidgets.QLineEdit`
        """

        # return
        return self.__lineEdit

    def setIcons(self, icons):
        """set the items icons of the comboBox

        :param icons: the icons used to set the comboBox
        :type icons: list[str]
        """

        # errors
        if not len(self.__items) == len(self.__icons):
            raise RuntimeError('The number of icons doesn\'t match the number of items')

        # set icons
        for index, icon in enumerate(icons):
            if icon:
                self.__combobox.setItemIcon(index, _qtGui.Icon(icon))

        # set icon size
        self.__combobox.setIconSize(PySide2.QtCore.QSize(*self.__iconSize))

    def setItems(self, items=None):
        """set the items of the comboBox

        :param items: the items used to set the comboBox
        :type items: list[str]
        """

        # clear
        self.__combobox.clear()

        # execute
        if items:
            for item in items:
                self.__combobox.addItem(str(item))

        # update
        self.__items = items

    def setText(self, text=None):
        """set the text of the lineEdit

        :param text: the text used to set the lineEdit
        :type text: str
        """

        # set text
        self.__lineEdit.setText(text or '')

    # PRIVATE COMMANDS #

    def _setOkStatus(self):
        """set the status of the okButton
        """

        # get text of the lineEdit
        text = str(self.__lineEdit.text())

        # execute
        self.setStatus(okEnabled=bool(text))

    def _validation(self):
        """get the result of the dialog when ``ok`` is pressed

        :return: ``Cancel`` : None -
                 ``Ok`` : if comboSeparator ``[{combobox.split(comboSeparator)[0]}{separator}{lineEdit} ...]``
                          else ``{combobox}{separator}{lineEdit}``
        :rtype: None or str or list[str]
        """

        # get content
        comboboxContent = str(self.__combobox.currentText())
        lineEditContent = str(self.__lineEdit.text())

        # return
        if not self.__concatenateResult:
            if not self.__comboSeparator:
                return [comboboxContent, lineEditContent]
            else:
                return [[content, lineEditContent]
                        for content in comboboxContent.split(self.__comboSeparator)]

        else:
            if not self.__comboSeparator:
                return '{0}{1}{2}'.format(comboboxContent, self.__separator, lineEditContent)
            else:
                return ['{0}{1}{2}'.format(content, self.__separator, lineEditContent)
                        for content in comboboxContent.split(self.__comboSeparator)]


class LineEditDialog(BaseDialog):
    """dialog with lineEdit filling
    """

    # INIT #

    def __init__(self, 
                 title, 
                 label,
                 data=None, 
                 entryLabelWidth=35,
                 size=None,
                 parent=None, 
                 isFrameless=False):
        """LineEditDialog class initialization

        :param title: the title of the dialog
        :type title: str

        :param label: the label of the dialog
        :type label: str

        :param data: the data used to create the lineEdits - ``[[label1, text1], ...]`` -
                     default is ``[[None, None]]``
        :type data: list[list[str]]

        :param entryLabelWidth: the with of the label of the lineEdit entries
        :type entryLabelWidth: int

        :param size: the size of the dialog - ``[width, height]`` - default is ``[None, None]``
        :type size: list[int]

        :param parent: the QWidget to parent the dialog to
        :type parent: :class:`PySide2.QtWidgets.QWidget`

        :param isFrameless: ``True`` : the dialog is frameless - ``False`` : the dialog has a frame
        :type isFrameless: bool
        """

        # init
        data = data or [[None, None]]
        size = size or [None, None]

        super(LineEditDialog, self).__init__(title, label, size=size, parent=parent, isFrameless=isFrameless)
        self.__lineEdits = []
        self.__entryLabelWidth = entryLabelWidth

        # create lineEdits
        for entryLabel, entryText in data:
            self.addLineEdit(entryLabel, entryText)

        # set ok button status
        self._setOkStatus()

        # setup connections
        self._setupConnections()

    def _setupConnections(self):
        """setup the connections of the widgets
        """

        # execute
        for lineEdit in self.__lineEdits:
            lineEdit.textChanged.connect(self._setOkStatus)

    # COMMANDS #

    def addLineEdit(self, label, text):
        """add a new lineEdit to the dialog

        :param label: label of the lineEdit
        :type label: str

        :param text: text of the lineEdit
        :type text: str
        """

        # content layout
        contentLayout = PySide2.QtWidgets.QHBoxLayout(self)
        contentLayout.setContentsMargins(0, 0, 0, 0)
        contentLayout.setSpacing(6)
        self.contentLayout().addLayout(contentLayout)

        # label
        if label:
            entryLabel = PySide2.QtWidgets.QLabel(self)
            entryLabel.setAlignment(PySide2.QtCore.Qt.AlignRight | PySide2.QtCore.Qt.AlignVCenter)
            entryLabel.setText(label)
            entryLabel.setFixedWidth(self.__entryLabelWidth)
            contentLayout.addWidget(entryLabel)

        # combobox
        entryLineEdit = PySide2.QtWidgets.QLineEdit(self)
        entryLineEdit.setText(text)
        contentLayout.addWidget(entryLineEdit)

        # update
        self.__lineEdits.append(entryLineEdit)

    # PRIVATE COMMANDS #

    def _setOkStatus(self):
        """set the status of the okButton
        """

        # init
        status = True

        # get status
        for lineEdit in self.__lineEdits:
            if not str(lineEdit.text()):
                status = False

        # execute
        self.setStatus(okEnabled=status)

    def _validation(self):
        """get the result of the dialog when ``ok`` is pressed

        :return: ``Cancel`` : None - ``Ok`` : lineEdit contents
        :rtype: None or list[str]
        """

        # execute
        return [str(lineEdit.text()) for lineEdit in self.__lineEdits]


class ProgressBarDialog(BaseDialog):
    """dialog displaying a progressBar
    """

    # INIT #

    def __init__(self, title, label, size=None, parent=None, isFrameless=False, barWidth=None, hasBarText=True):
        """ProgressBarDialog class initialization

        :param title: the title of the dialog
        :type title: str

        :param label: the label of the dialog
        :type label: str

        :param size: the size of the dialog - ``[width, height]`` - default is ``[None, None]``
        :type size: list[int]

        :param parent: the QWidget to parent the TextEdit dialog to
        :type parent: :class:`PySide2.QtWidgets.QWidget`

        :param isFrameless: ``True`` : the dialog is frameless - ``False`` : the dialog has a frame
        :type isFrameless: bool

        :param barWidth: the width of the bar
        :type barWidth: int

        :param hasBarText: ``True`` : the progressBar has a text - ``False`` : the progressBar doesn't have a text
        :type hasBarText: bool
        """

        # init
        super(ProgressBarDialog, self).__init__(title, label, size=size, parent=parent, isFrameless=isFrameless)

        # hide buttons
        self.setButtonDisplayed(isOkDisplayed=False, isCancelDisplayed=False)

        # set focus policy
        self.setFocusPolicy(PySide2.QtCore.Qt.NoFocus)

        # progress bar
        self.progressBar = _qtWidgets.ProgressBar(barWidth=barWidth, hasText=hasBarText, parent=self)
        self.contentLayout().addWidget(self.progressBar)

    # COMMANDS #

    def load(self):
        """load the progressBar dialog
        """

        # return
        self.show()

    def setText(self, text):
        """set the text of the progressBar

        :param text: the text to set on the progressBar
        :type text: str
        """

        # execute
        self.progressBar.setText(text)

    def setValue(self, value):
        """set the value of the progressBar

        :param value: value to set on the progressBar
        :type value: float
        """

        # execute
        self.progressBar.setValue(value)


class StatusDialog(BaseDialog):
    """dialog displaying current status
    """

    # SIGNALS #

    statusChanged = PySide2.QtCore.Signal(str)

    # INIT #

    def __init__(self, title, size=None, parent=None, isFrameless=False):
        """StatusDialog class initialization

        :param title: the title of the dialog
        :type title: str

        :param size: the size of the dialog - ``[width, height]`` - default is ``[None, None]``
        :type size: list[int]

        :param parent: the QWidget to parent the TextEdit dialog to
        :type parent: :class:`PySide2.QtWidgets.QWidget`

        :param isFrameless: ``True`` : the dialog is frameless - ``False`` : the dialog has a frame
        :type isFrameless: bool
        """

        # init
        super(StatusDialog, self).__init__(title,
                                           '',
                                           size=size,
                                           parent=parent,
                                           isFrameless=isFrameless,
                                           orientation=cgp_generic_utils.constants.Orientation.HORIZONTAL)

        # hide buttons
        self.setButtonDisplayed(isOkDisplayed=False, isCancelDisplayed=False)

        # set focus policy
        self.setFocusPolicy(PySide2.QtCore.Qt.NoFocus)

        # label
        self.descriptionLabel = PySide2.QtWidgets.QLabel(self)
        self.descriptionLabel.setAlignment(PySide2.QtCore.Qt.AlignCenter)

        # add widgets
        for widget in [self.descriptionLabel]:
            self.contentLayout().addWidget(widget)

        # setup connections
        self._setupConnections()

    def _setupConnections(self):
        """setup the connections of the widgets
        """

        # execute
        self.statusChanged.connect(self._setDescription)

    # COMMANDS #

    def close(self, description, closeTime=1):
        """close the statusDialog

        :param description: the description to set before the dialog closes
        :type description: str

        :param closeTime: the time in seconds before the dialog closes
        :type closeTime: float
        """

        # emit
        self.statusChanged.emit(description)

        # time sleep
        time.sleep(0.1)
        PySide2.QtWidgets.QApplication.processEvents()
        time.sleep(closeTime)

        # close
        super(StatusDialog, self).close()

    def keyPressEvent(self, event):
        """override keyPressEvent
        """

        # this event is overwriten to avoid escape key to close the dialog 
        pass

    def load(self, description):
        """load the statusDialog

        :param description: the description to set when the dialog is loaded
        :type description: str
        """

        # show dialog
        self.show()

        # emit
        self.statusChanged.emit(description)

        # refresh
        time.sleep(0.1)
        PySide2.QtWidgets.QApplication.processEvents()

    # PROTECTED COMMANDS #

    @PySide2.QtCore.Slot(str)
    def _setDescription(self, description):
        """set description of the dialog

        :param description: the the description to set on the dialog
        :type description: str
        """

        # execute
        self.descriptionLabel.setText(description)


class TextEditDialog(BaseDialog):
    """dialog with textEdit filling
    """

    # INIT #

    def __init__(self, title, label, text=None, size=None, parent=None, isFrameless=False):
        """TextEditDialog class initialization

        :param title: the title of the dialog
        :type title: str

        :param label: the label of the dialog
        :type label: str

        :param text: the text that will be displayed in the TextEdit at initialization
        :type text: str

        :param size: the size of the dialog - ``[width, height]`` - default is ``[None, None]``
        :type size: list[int]

        :param parent: the QWidget to parent the TextEdit dialog to
        :type parent: :class:`PySide2.QtWidgets.QWidget`

        :param isFrameless: ``True`` : the dialog is frameless - ``False`` : the dialog has a frame
        :type isFrameless: bool
        """

        # init
        size = size or [None, None]
        super(TextEditDialog, self).__init__(title, label, size=size, parent=parent, isFrameless=isFrameless)

        # textEdit
        self.__textEdit = PySide2.QtWidgets.QTextEdit(self)
        self.setText(text=text)
        self.contentLayout().addWidget(self.__textEdit)

        # set ok button status
        self._setOkStatus()

        # setup connections
        self._setupConnections()

    def _setupConnections(self):
        """setup the connections of the widgets
        """

        # execute
        self.__textEdit.textChanged.connect(self._setOkStatus)

    # COMMANDS #

    def setText(self, text=None):
        """set the text of the lineEdit

        :param text: text used to set the lineEdit
        :type text: str
        """

        # execute
        if text:
            self.__textEdit.setPlainText(text)
        else:
            self.__textEdit.clear()

    # PRIVATE COMMANDS #

    def _setOkStatus(self):
        """set the status of the okButton
        """

        # get text of the lineEdit
        text = str(self.__textEdit.toPlainText())

        # execute
        if not text:
            self.setStatus(okEnabled=False)
        else:
            self.setStatus(okEnabled=True)

    def _validation(self):
        """get the result of the dialog when ``ok`` is pressed

        :return: ``Cancel`` : None - ``Ok`` : the content of the textEdit
        :rtype: None or str
        """

        # return
        return str(self.__textEdit.toPlainText())
