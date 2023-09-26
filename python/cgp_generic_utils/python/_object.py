"""
object library
"""

# imports python
import sys
import inspect
import six.moves.collections_abc


# BASE OBJECTS #


class BaseObject(object):
    """object that represent any king of object of our API
    """

    # INIT #

    def __repr__(self):
        """get the representation of the BaseObject

        :return: the representation of the BaseObject
        :rtype: str
        """

        # return
        return self._representationTemplate()

    # PROTECTED COMMANDS #

    def _representationTemplate(self, withVarArgs=False, withVarKwargs=False):
        """get the representation template of the BaseObject

        :param withVarArgs: ``True`` : template includes varArgs - ``False`` : template excludes varArgs
        :type withVarArgs: bool

        :param withVarKwargs: ``True`` : template includes varKwargs - ``False`` : template excludes varKwargs
        :type withVarKwargs: bool

        :return: the representation template of the BaseObject
        :rtype: str
        """

        # init
        cls = self.__class__
        modules = tuple(subModule for subModule in cls.__module__.split('.') if not subModule.startswith('_'))
        arguments = []

        # inspect init arguments
        try:
            argSpec = (inspect.getargspec(self.__init__)
                       if sys.version_info < (3, 0)
                       else inspect.getfullargspec(self.__init__))
        except TypeError:
            argSpec = None

        # built arguments
        if argSpec:
            positionalCount = len(argSpec.args) - (len(argSpec.defaults or []))
            for index, name in enumerate(argSpec.args):

                # bypass self
                if not index:
                    continue

                # format argument
                argument = '{%s!r}' % name if index < positionalCount else '%s={%s!r}' % (name, name)
                arguments.append(argument)

            # add *args and **kwargs
            if withVarArgs and argSpec.varargs:
                arguments.append('*{%s!r}' % argSpec.varargs)
            if withVarKwargs and argSpec.keywords:
                arguments.append('**{%s!r}' % argSpec.keywords)

        # return
        return '{}({})'.format('.'.join(modules + (cls.__name__,)), ', '.join(arguments))


class BaseEnum(BaseObject):
    """object that represent any king of enum of our API
    """

    # OBJECT COMMANDS #

    @classmethod
    def all(cls, withSingles=True, withIterables=False):
        """get the values of the BaseEnum

        :param withSingles: ``True`` : single values are included - ``False`` : single values are excluded
        :type withSingles: bool

        :param withIterables: ``True`` : iterable values are included - ``False`` : iterable values are excluded
        :type withIterables: bool

        :return: the values of the BaseEnum
        :rtype: tuple[any]
        """

        # init
        values = tuple()

        # execute
        for value in cls.asDict().values():
            isIterable = not isinstance(value, str) and isinstance(value, six.moves.collections_abc.Iterable)

            # append iterables
            if isIterable and withIterables:
                values += (value,)

            # append singles
            elif not isIterable and withSingles:
                values += (value,)

        # return
        return values

    @classmethod
    def asDict(cls):
        """get the dictionary representation of the BaseEnum

        :return: the dictionary representation of the BaseEnum
        :rtype: dict
        """

        # return
        return {key: value for key, value in cls.__dict__.items()
                if not callable(value)                                  # ignore callable
                and type(value) not in (staticmethod, classmethod)      # ignore static/class methods
                and not (key.startswith('__') and key.endswith('__'))}  # ignore magic methods
