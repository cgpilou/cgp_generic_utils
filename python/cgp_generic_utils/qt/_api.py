"""
qt management functions
"""

# imports third-parties
import PySide2.QtWidgets


# API COMMANDS #


def scaledSize(size):
    """get the scaled size based on the pixel density of the screen

    :param size: the size
    :type size: int

    :return: the scaled size
    :rtype: int
    """

    # init
    defaultDensity = 100
    pixelDensities = []

    # get pixel density
    for widget in PySide2.QtWidgets.QApplication.topLevelWidgets():

        # get window
        window = widget.windowHandle()
        if not window:
            continue

        # get pixel density
        pixelDensity = window.screen().logicalDotsPerInch()
        pixelDensities.append(pixelDensity)

    # get average density
    pixelDensity = sum(pixelDensities) / len(pixelDensities) if pixelDensities else defaultDensity

    # return
    return int(round(size * (pixelDensity / defaultDensity)))
