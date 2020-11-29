"""
abstract decorator library
"""

# imports python
import functools


# ABSTRACT DECORATORS #


class Decorator(object):
    """decorator handling decoration and context behavior through subclass inheritance
    """

    def __call__(self, function):
        """override call

        :param function: function to decorate
        :type function: python

        :return: the function wrapper
        :rtype: python
        """

        # execute
        @functools.wraps(function)
        def functionWrapper(*args, **kwargs):
            """get the function wrapper

            :return: the result of the wrapped function
            :rtype: python
            """

            # execute
            with self:
                return function(*args, **kwargs)

        # return
        return functionWrapper
