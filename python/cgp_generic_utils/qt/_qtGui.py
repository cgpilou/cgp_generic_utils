"""
qtGui objet library
"""

# imports python
import os

# imports third-parties
import PySide2.QtGui

# imports local
import cgp_generic_utils.python
import cgp_generic_utils.constants


class Font(PySide2.QtGui.QFont):
    """QFont with custom functionalities
    """

    def __init__(self, size, styles=None):
        """Font class initialization

        :param size: size of the font
        :type size: int

        :param styles: styles of the font - [bold - italic - underline]
        :type: list[:class:`cgp_generic_utils.constants.TypoStyle`]
        """

        # init
        super(Font, self).__init__()

        # error
        for style in styles:
            if style not in cgp_generic_utils.constants.TypoStyle.ALL:
                raise ValueError('{0} is not a style - {1}'.format(style, cgp_generic_utils.constants.TypoStyle.ALL))

        # set styles
        for style in styles:
            getattr(self, 'set{0}'.format(style.capitalize()))(True)

        # set sizes
        self.setPointSize(size)


class Icon(PySide2.QtGui.QIcon):
    """QIcon with custom functionalities
    """

    # INIT #

    def __init__(self, image):
        """Icon class initialization
        """

        #
        self._path = os.path.join(cgp_generic_utils.constants.Environment.ICON_LIBRARY, image)

        # execute
        super(Icon, self).__init__(self._path)

    # COMMANDS #

    def path(self):
        """the path of the image used by the icon

        :return: the path of the image
        :rtype: str
        """

        # execute
        return self._path
