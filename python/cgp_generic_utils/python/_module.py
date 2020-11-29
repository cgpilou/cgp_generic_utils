"""
library of functions for python module management
"""


# imports python
import sys


def deleteModules(*args):
    """ delete modules that contain the arguments
    """

    # execute
    for mod in sorted(sys.modules):
        if any([True for t in args if t in mod]):
            del sys.modules[mod]


def import_(module, command=None):
    """import the module. return module.command if command is specified

    :param module: module of the command to import
    :type module: str

    :param command: command to import
    :type command: str

    :return: the imported function
    :rtype: function
    """

    # get module
    mod = __import__(module, fromlist=[''])

    # return
    return getattr(mod, command) if command else mod
