"""
library of functions for python module management
"""

# imports python
import sys


def deleteModules(*args):
    """delete modules that contain the arguments
    """

    # execute
    for module in sorted(sys.modules):
        if any([True for arg in args if arg in module]):
            del sys.modules[module]


def importCommand(moduleName, commandName=None):
    """import the module from a string - return ``module.command`` if command is specified

    :param moduleName: name of the module to import
    :type moduleName: str

    :param commandName: name of the command to import
    :type commandName: str

    :return: the imported command
    :rtype: python
    """

    # get module
    module = __import__(moduleName, fromlist=[''])

    # return
    return getattr(module, commandName) if commandName else module
