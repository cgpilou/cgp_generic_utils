"""
handles color operations
"""

# imports python
import colorsys

# imports local
from . import _object


# COLOR OBJECTS #


class Color(_object.BaseObject):
    """object representing any kind of color
    """

    # INIT #

    def __init__(self, red, green, blue, alpha=1.0):
        """initialization of the Color

        :param red: the red value (0.0 to 1.0)
        :type red: float

        :param green: the green value (0.0 to 1.0)
        :type green: float

        :param blue: the blue value (0.0 to 1.0)
        :type blue: float

        :param alpha: the transparency value (0.0 to 1.0)
        :type alpha: float
        """

        # init
        self._rgba = self._validateComponents((red, green, blue, alpha))

    def __repr__(self):
        """get the representation of the Color

        :return: the representation of the Color
        :rtype: str
        """

        # init
        red, green, blue, alpha = self.rgba()

        # return
        return self._representationTemplate().format(red=red, green=green, blue=blue, alpha=alpha)

    # COMMANDS #

    def hex(self):
        """get the hex value of the Color

        :return the hex value of the Color
        :rtype: str
        """

        # init
        red, green, blue, alpha = self.rgba()

        # translate
        red = format(int(red * 255), '02x')
        green = format(int(green * 255), '02x')
        blue = format(int(blue * 255), '02x')
        alpha = format(int(alpha * 255), '02x')

        # return
        return "#{}{}{}{}".format(red, green, blue, alpha if alpha != 'ff' else '')

    def hsl(self):
        """get the hsl value of the Color

        :return the hsl value of the Color
        :rtype: tuple[float]
        """

        # init
        hls = colorsys.rgb_to_hls(*self.rgba()[:3])

        # return
        return hls[0], hls[2], hls[1]

    def hsv(self):
        """get the hsv value of the Color

        :return the hsv value of the Color
        :rtype: tuple[float]
        """

        # return
        return colorsys.rgb_to_hsv(*self.rgba()[:3])

    def rgba(self):
        """get the rgba value of the Color

        :return the rgba value of the Color
        :rtype: tuple[float]
        """

        # return
        return self._rgba

    def setHex(self, value):
        """set the hex value of the Color

        :param value: the hex value of the Color
        :type value: str
        """

        # extract hex components
        hexColor = value.strip('#')
        components = [hexColor[i:i + 2] for i in range(0, len(hexColor), 2)]

        # translate to rgb components
        components = [int(component, base=16) / 255.0 for component in components]

        # set the color
        self.setRgba(*components)

    def setHsl(self, hue=None, saturation=None, lightness=None):
        """set the hsv value of the Color

        :param hue: the hue value
        :type hue: float

        :param saturation: the saturation value
        :type saturation: float

        :param lightness: the lightness value
        :type lightness: float
        """

        # init
        hsl = self.hsl()
        hue = hsl[0] if hue is None else hue
        saturation = hsl[1] if saturation is None else saturation
        lightness = hsl[2] if lightness is None else lightness

        # execute
        hls = self._validateComponents((hue, lightness, saturation))
        rgb = colorsys.hls_to_rgb(*hls)
        self.setRgba(*rgb)

    def setHsv(self, hue=None, saturation=None, value=None):
        """set the hsv value of the Color

        :param hue: the hue value
        :type hue: float

        :param saturation: the saturation value
        :type saturation: float

        :param value: the value value
        :type value: float
        """

        # init
        hsv = self.hsv()
        hue = hsv[0] if hue is None else hue
        saturation = hsv[1] if saturation is None else saturation
        value = hsv[2] if value is None else value

        # execute
        hsv = self._validateComponents((hue, saturation, value))
        rgb = colorsys.hsv_to_rgb(*hsv)
        self.setRgba(*rgb)

    def setRgba(self, red=None, green=None, blue=None, alpha=None):
        """set the rgba value of the Color

        :param red: the red value
        :type red: float

        :param green: the green value
        :type green: float

        :param blue: the blue value
        :type blue: float

        :param alpha: the alpha/transparency value
        :type alpha: float
        """

        # init
        red = self._rgba[0] if red is None else red
        green = self._rgba[1] if green is None else green
        blue = self._rgba[2] if blue is None else blue
        alpha = self._rgba[3] if alpha is None else alpha

        # execute
        self._rgba = self._validateComponents((red, green, blue, alpha))

    # PROTECTED COMMANDS #

    @staticmethod
    def _validateComponents(components):
        """validate that the component are in 0.0 to 1.0 range

        :param components: the color components values
        :type components: tuple

        :return: the color components values
        :rtype components: tuple
        """

        # error
        for index, value in enumerate(components):
            if not 0.0 <= value <= 1.0:
                raise ValueError('Color component at index {} is not in a 0.0 to 1.0 range, '
                                 'got {}'.format(index, value))

        # return
        return components
