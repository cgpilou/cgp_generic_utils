"""
qtGui objet library
"""

# imports python
import os

# imports third-parties
import PySide2.QtGui
import PySide2.QtCore

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

        :param styles: styles of the font - ``[bold - italic - underline]``
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

        :param image: name of an image stored in the icon library
        :type image: str
        """

        # init
        self._path = os.path.join(cgp_generic_utils.constants.Environment.ICON_LIBRARY, image)

        # execute
        super(Icon, self).__init__(self._path)

    # PROPERTIES #

    @property
    def path(self):
        """get the path of the image used by the icon

        :return: the path of the image
        :rtype: str
        """

        # execute
        return self._path


class Movie(PySide2.QtGui.QMovie):
    """QMovie with custom functionalities
    """

    # INIT #

    def __init__(self, movie):
        """Movie class initialization

        :param movie: name of a movie stored in the icon library
        :type movie: str
        """

        # init
        self._path = os.path.join(cgp_generic_utils.constants.Environment.ICON_LIBRARY, movie)

        # execute
        super(Movie, self).__init__(self._path)

    # PROPERTIES #

    @property
    def path(self):
        """get the path of the movie used by the movie

        :return: the path of the movie
        :rtype: str
        """

        # execute
        return self._path

    # COMMANDS #

    def setSize(self, size):
        """set the size of the movie

        :param size: size of the movie to set
        :type size: list[int]
        """

        # execute
        self.setScaledSize(PySide2.QtCore.QSize(*size))


class Pixmap(PySide2.QtGui.QPixmap):
    """QPixmap with custom functionalities
    """

    # INIT #

    def __init__(self, image):
        """Pixmap class initialization

        :param image: name of an image stored in the icon library
        :type image: str
        """

        #
        self._path = os.path.join(cgp_generic_utils.constants.Environment.ICON_LIBRARY, image)

        # execute
        super(Pixmap, self).__init__(self._path)

    # PROPERTIES #

    @property
    def path(self):
        """get the path of the image used by the pixmap

        :return: the path of the image
        :rtype: str
        """

        # execute
        return self._path
