"""
performance decorator library
"""

# imports python
import cProfile
import pstats
import sys
import time

if sys.version_info < (3, 0):
    import StringIO
else:
    from io import StringIO

# imports local
from . import _generic


# PERFORMANCE DECORATORS #


class Timer(_generic.Decorator):
    """decorator returning the execution time of the encapsulated script block / function
    """

    def __init__(self, label=None):
        """Timer class initialization

        :param label: text that will be attached to the timer result
        :type label: str
        """

        # init
        self._initialTime = None
        self._label = label

    def __enter__(self):
        """enter Timer decorator
        """

        # execute
        self._initialTime = time.time()

    def __exit__(self, *_, **__):
        """exit Timer decorator
        """

        # execute
        finalTime = time.time() - self._initialTime

        # print
        sys.stdout.write('{0} : {1} seconds'.format(self._label or 'Timer', finalTime))


class Profiler(_generic.Decorator):
    """decorator returning the profiling of the encapsulated script block / function
    """

    def __init__(self, sortBy=None):
        """Profiler class initialization

        :param sortBy: defines how the stats will be sorted - default is time
        :type sortBy: str
        """

        # init
        self._profiler = None
        self._sortBy = sortBy or 'time'

    def __enter__(self):
        """enter Profiler decorator
        """

        # execute
        self.profiler = cProfile.Profile()
        self.profiler.enable()

    def __exit__(self, *_, **__):
        """exit Profiler decorator
        """

        # init
        stream = StringIO.StringIO()

        # execute
        self.profiler.disable()
        pstats.Stats(self.profiler, stream=stream).sort_stats(self._sortBy).print_stats()

        # return
        sys.stdout.write(stream.getvalue())
