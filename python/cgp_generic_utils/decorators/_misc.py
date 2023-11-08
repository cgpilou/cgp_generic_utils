"""
misc decorator library
"""

# imports python
import sys
import ast
import inspect


# MISC DECORATORS #


class Deprecated(object):
    """decorator to warn the user the command is deprecated
    """

    def __init__(self, useInstead=None):
        """initialization of the Deprecated decorator

        :param useInstead: the callable to use instead of the deprecated one - will be printed (not called) to help user
        :type useInstead: callable
        """

        # init
        self._called = None
        self._useInstead = useInstead

    def __call__(self, callable_):
        """override call

        :param callable_: callable_ to decorate
        :type callable_: callable

        :return: the callable_
        :rtype: callable
        """

        # init
        self._called = callable_

        # alert the user
        sys.stdout.write('[WARNING] {}\n'.format(self._message()))
        sys.stdout.flush()

        # return
        return callable_

    # PROTECTED COMMAND #

    @staticmethod
    def _callablePublicName(callable_):
        """get the public name of a callable

        :param callable_: the callable to get public name of
        :type callable_: callable

        :return: the public name of a callable
        :rtype: str
        """

        # add module name in name parts
        nameParts = [subModule for subModule in callable_.__module__.split('.') if not subModule.startswith('_')]

        # get source and line
        lineNumber = inspect.getsourcelines(callable_)[-1]
        sourcePath = inspect.getsourcefile(callable_)
        with open(sourcePath, 'r') as sourceFile:
            source = sourceFile.read()

        # get classes in source
        classData = {node.name: [subNode.lineno for subNode in node.body if isinstance(subNode, ast.FunctionDef)]
                     for node in ast.walk(ast.parse(source)) if isinstance(node, ast.ClassDef)}

        # add class name in name parts
        for className, methodLines in classData.items():
            if lineNumber in methodLines:
                nameParts.append(className)
                break

        # add callable name in name parts
        nameParts.append(callable_.__name__)

        # differentiate properties from methods
        if not isinstance(callable_, property):
            nameParts[-1] += '()'

        # return
        return '.'.join(nameParts)

    def _message(self):
        """get the message to display

        :return: the message to display
        :rtype: str
        """

        # init
        message = 'Deprecated call of {}'.format(self._callablePublicName(self._called))

        # specify the callable that should be used instead
        if self._useInstead:
            message += '. Please use {} instead.'.format(self._callablePublicName(self._useInstead))

        # return
        return message
