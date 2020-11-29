"""
Constants used to manipulate naming data
"""

# imports python
import collections


class Side(object):

    LEFT = 'L'
    RIGHT = 'R'
    MIDDLE = 'M'
    MIRROR = collections.OrderedDict([(LEFT, RIGHT), (MIDDLE, None), (RIGHT, LEFT)])
    ALL = [LEFT, MIDDLE, RIGHT]


class TypoStyle(object):

    BOLD = 'bold'
    ITALIC = 'italic'
    UNDERLINE = 'underline'
    ALL = [BOLD, ITALIC, UNDERLINE]
