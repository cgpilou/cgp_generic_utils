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


# BASE OBJECTS #


class BaseDialog(PySide2.QtWidgets.QDialog):
    """basic dialog with ok and cancel button
    """

    # INIT #

    def __init__(self, title, label, size=None, parent=None, isFrameless=False, orientation=None):
        """BaseDialog class initialization

        :param title: the title of the dialog
        :type title: str

        :param label: the content of the label to set
        :type label: str

        :param size: values of the width and the height  ``[width - height]`` - default is ``[None, None]``
        :type size: list[int]

        :param parent: QWidget to parent the TextEdit dialog to
        :type parent: :class:`PySide2.QtWidgets.QWidget`

        :param isFrameless: ``True`` : dialog is frameless - ``False`` : dialog has a frame
        :type isFrameless: bool

        :param orientation: orientation of the content layout -
                            default is ``cgp_generic_utils.constants.Orientation.VERTICAL``
        :type orientation: str
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
        sizePolicy = PySide2.QtWidgets.QSizePolicy(PySide2.QtWidgets.QSizePolicy.Preferred,
                                                   PySide2.QtWidgets.QSizePolicy.Fixed)
        self.__label.setSizePolicy(sizePolicy)
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
        self.__horizontalLayout = PySide2.QtWidgets.QHBoxLayout()
        self.__verticalLayout.addLayout(self.__horizontalLayout)

        # spacer 02
        spacerItem_02 = PySide2.QtWidgets.QSpacerItem(40, 20,
                                                      PySide2.QtWidgets.QSizePolicy.Expanding,
                                                      PySide2.QtWidgets.QSizePolicy.Minimum)
        self.__horizontalLayout.addItem(spacerItem_02)

        # ok button
        self.__ok_b = PySide2.QtWidgets.QPushButton(self)
        self.__ok_b.setMinimumSize(PySide2.QtCore.QSize(0, 30))
        self.__horizontalLayout.addWidget(self.__ok_b)
        self.setOkButton()

        # cancel button
        self.__cancel_b = PySide2.QtWidgets.QPushButton(self)
        self.__cancel_b.setMinimumSize(PySide2.QtCore.QSize(0, 30))
        self.__horizontalLayout.addWidget(self.__cancel_b)
        self.setCancelButton()

        # spacer 03
        spacerItem_03 = PySide2.QtWidgets.QSpacerItem(40, 20,
                                                      PySide2.QtWidgets.QSizePolicy.Expanding,
                                                      PySide2.QtWidgets.QSizePolicy.Minimum)
        self.__horizontalLayout.addItem(spacerItem_03)

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

    def contentLayout(self):
        """the content layout

        :return: the content layout
        :rtype: :class:`PySide2.QtWidgets.QBoxLayout`
        """

        # return
        return self.__contentLayout

    def isValid(self):
        """check if the dialog is valid

        :return: ``True`` it is valid - ``False`` it is not valid
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
        elif event.key() in [PySide2.QtCore.Qt.Key_Return, PySide2.QtCore.Qt.Key_Enter] and self.isValid:
            self.accept()

    def load(self):
        """load base dialog

        :return: ``cancel`` : self.rejection - ``ok`` : self.validation
        :rtype: any
        """

        # return
        return self.validation() if self.exec_() else self.rejection()

    def rejection(self):
        """result of the dialog when ``cancel`` is pressed

        :return: the rejection of the dialog
        :rtype: any
        """

        # execute
        return None

    def setCancelButton(self, text=None):
        """set the text of the cancel button

        :param text: text to set on the cancel button
        :type text: str
        """

        # get text
        text = text or 'Cancel'

        # set text
        self.__cancel_b.setText(text)

    def setOkButton(self, text=None):
        """set the text ok the ok button

        :param text: text to set on the ok button
        :type text: str
        """

        # get text
        text = text or 'Ok'

        # set text
        self.__ok_b.setText(text)

    def setStatus(self, okEnabled=True):
        """set the status of the ok button

        :param okEnabled: ``True`` : the ok button is enabled - ``False`` the ok button is disabled
        :type okEnabled: bool
        """

        # execute
        self._isValid = okEnabled
        self.__ok_b.setEnabled(okEnabled)

    def setSize(self, size):
        """set the size of the dialog

        :param size: values of the width and the height  ``[width - height]``
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

    def validation(self):
        """result of the dialog when ``ok`` is pressed

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

        :param label: the content of the label to set
        :type label: str

        :param data: data used to labels and states to populate the checkBoxes - ``{label1: True, label2: False}``
        :type data: dict

        :param size: values of the width and the height  ``[width - height]`` - default is ``[None, None]``
        :type size: list[int]

        :param parent: QWidget to parent the line edit dialog to
        :type parent: :class:`PySide2.QtWidgets.QWidget`

        :param isFrameless: ``True`` : dialog is frameless - ``False`` : dialog has a frame
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
        """add a new check box to the dialog

        :param label: label of the checkbox
        :type label: str

        :param isChecked: ``True`` checkbox is checked - ``False`` checkbox is not checked
        :type isChecked: bool

        :return: the added checkbox
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

    def validation(self):
        """validation of the dialog

        :return: ``Cancel`` : None - ``Ok`` : {checkBoxLabel1: isChecked1, checkBoxLabel2: isChecked2 ...}
        :rtype: None or dict
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

        :param label: the content of the label to set
        :type label: str

        :param data: data used to build the comboBoxes - ``[[label1, [itemA, itemB ...]], [label2, [...]], ...]``
        :type data: list[list[str, list[str]]]

        :param entryLabelWidth: with of the label of the combobox entries
        :type entryLabelWidth: int

        :param size: values of the width and the height  ``[width - height]`` - default is ``[None, None]``
        :type size: list[int]

        :param parent: QWidget to parent the line edit dialog to
        :type parent: :class:`PySide2.QtWidgets.QWidget`

        :param isFrameless: ``True`` : dialog is frameless - ``False`` : dialog has a frame
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

    # PRIVATE COMMANDS #

    def validation(self):
        """validation of the dialog

        :return: ``Cancel`` : None - ``Ok`` : list of combobox currentTexts
        :rtype: None or list[str]
        """

        # return
        return [str(combobox.currentText()) for combobox in self.__comboboxes]


class ComboBoxLineEditDialog(BaseDialog):
    """dialog with combobox selection and lineEdit filling
    """

    # INIT #

    def __init__(self, title, label, items, icons=None, iconSize=None, text=None, comboSeparator=None,
                 separator=None, concatenateResult=True, size=None, parent=None, isFrameless=False):
        """ComboBoxLineEditDialog class initialization

        :param title: the title of the dialog
        :type title: str

        :param label: the content of the label to set
        :type label: str

        :param icons: icons used to populate the combobox
        :type icons: list[str]

        :param iconSize: size of the icons - default is ``[10, 10]``
        :type iconSize: list[int]

        :param items: item used to populate the combobox
        :type items: list[str]

        :param text: the text that will be displayed in the lineEdit at initialization
        :type text: str

        :param comboSeparator: separator used to split combobox content if specified
        :type comboSeparator: str

        :param separator: separator used when merging current combobox item with lineEdit text
        :type separator: str

        :param concatenateResult: defines whether or not the result will be concatenated between combobox and lineEdit
        :type concatenateResult: bool

        :param size: values of the width and the height  ``[width - height]`` - default is ``[None, None]``
        :type size: list[int]

        :param parent: QWidget to parent the line edit dialog to
        :type parent: :class:`PySide2.QtWidgets.QWidget`

        :param isFrameless: ``True`` : dialog is frameless - ``False`` : dialog has a frame
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
                                                     orientation=cgp_generic_utils.constants.Orientation.HORIZONTAL)

        self.__items = items
        self.__icons = icons
        self.__iconSize = iconSize
        self.__concatenateResult = concatenateResult

        # define separator
        self.__separator = separator or ''

        # define comboSeparator
        self.__comboSeparator = comboSeparator or None

        # combobox
        self.__combobox = PySide2.QtWidgets.QComboBox(self)
        self.setItems(items=self.__items)
        self.contentLayout().addWidget(self.__combobox)

        if self.__icons:
            self.setIcons(self.__icons)

        # line Edit
        self.__lineEdit = PySide2.QtWidgets.QLineEdit(self)
        self.setText(text=text)
        self.contentLayout().addWidget(self.__lineEdit)

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

    def setIcons(self, icons):
        """set the items icons of the combobox

        :param icons: icons used to set the combobox
        :type icons: list[str]
        """

        # errors
        if not len(self.__items) == len(self.__icons):
            raise RuntimeError('The number of icons does not match the number of items')

        # set icons
        for index, icon in enumerate(icons):
            if icon:
                self.__combobox.setItemIcon(index, _qtGui.Icon(icon))

        # set icon size
        self.__combobox.setIconSize(PySide2.QtCore.QSize(*self.__iconSize))

    def setItems(self, items=None):
        """set the items of the combobox

        :param items: items used to set the combobox
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
        """set the text of the line edit

        :param text: text used to set the line edit
        :type text: str
        """

        # execute
        if text:
            self.__lineEdit.setText(text)

    # PRIVATE COMMANDS #

    def _setOkStatus(self):
        """set the status of the okButton
        """

        # get text of the lineEdit
        text = str(self.__lineEdit.text())

        # execute
        self.setStatus(okEnabled=bool(text))

    def validation(self):
        """validation of the dialog

        :return: ``Cancel`` : None -
                 ``Ok`` : if comboSeparator ``[{combobox.split(comboSeparator)[0]}{separator}{lineEdit} ...]``
                          else ``{combobox}{separator}{lineEdit}``
        :rtype: None or list[str] or str
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

    def __init__(self, title, label, data=None, entryLabelWidth=35,
                 size=None, parent=None, isFrameless=False):
        """LineEditDialog class initialization

        :param title: the title of the dialog
        :type title: str

        :param label: the content of the label to set
        :type label: str

        :param data: data used to create the entry lineEdits - ``[[label1, text1], ...]`` -
                     default is ``[[None, None]]``
        :type data: list[list[str]]

        :param entryLabelWidth: with of the label of the lineEdit entries
        :type entryLabelWidth: int

        :param size: values of the width and the height ``[width - height]`` - default is ``[None, None]``
        :type size: list[int]

        :param parent: QWidget to parent the line edit dialog to
        :type parent: :class:`PySide2.QtWidgets.QWidget`

        :param isFrameless: ``True`` : dialog is frameless - ``False`` : dialog has a frame
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

    def validation(self):
        """validation of the dialog

        :return: ``Cancel`` : None - ``Ok`` : lineEdit contents
        :rtype: None or list[str]
        """

        # execute
        return [str(lineEdit.text()) for lineEdit in self.__lineEdits]


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

        :param size: values of the width and the height ``[width - height]`` - default is ``[None, None]``
        :type size: list[int]

        :param parent: QWidget to parent the line edit dialog to
        :type parent: :class:`PySide2.QtWidgets.QWidget`

        :param isFrameless: ``True`` : dialog is frameless - ``False`` : dialog has a frame
        :type isFrameless: bool
        """

        # init
        super(StatusDialog, self).__init__(title,
                                           '',
                                           size=size,
                                           parent=parent,
                                           isFrameless=isFrameless,
                                           orientation=cgp_generic_utils.constants.Orientation.HORIZONTAL)

        # hide buttons and label
        self.setButtonDisplayed(False)

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
        """setup connections
        """

        # execute
        self.statusChanged.connect(self._setDescription)

    # COMMANDS #

    def close(self, description, closeTime=1):
        """close status dialog

        :param description: description to set before the dialog closes
        :type description: str

        :param closeTime: time in seconds before the dialog closes
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

        # execute
        pass

    def load(self, description):
        """load status dialog

        :param description: description to set when the dialog is loaded
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

        :param description: set the description of the dialog
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

        :param label: the content of the label to set
        :type label: str

        :param text: the text that will be displayed in the TextEdit at initialization
        :type text: str

        :param size: values of the width and the height ``[width - height]`` - default is ``[None, None]``
        :type size: list[int]

        :param parent: QWidget to parent the TextEdit dialog to
        :type parent: :class:`PySide2.QtWidgets.QWidget`

        :param isFrameless: ``True`` : dialog is frameless - ``False`` : dialog has a frame
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
        """set the text of the line edit

        :param text: text used to set the line edit
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

    def validation(self):
        """validation of the dialog

        :return: ``Cancel`` : None - ``Ok`` : textEdit content
        :rtype: None or str
        """

        # return
        return str(self.__textEdit.toPlainText())
