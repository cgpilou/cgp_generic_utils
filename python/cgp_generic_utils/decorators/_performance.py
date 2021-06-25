"""
performance decorator library
"""

# imports python
import cProfile
import pstats
import StringIO
import sys
import time

# imports local
from . import _abstract


# PERFORMANCE DECORATORS #


class Timer(_abstract.Decorator):
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

    def __exit__(self, *args, **kwargs):
        """exit Timer decorator
        """

        # execute
        finalTime = time.time() - self._initialTime

        # return
        print '{0} : {1} seconds'.format(self._label or 'Timer', finalTime)


class Profiler(_abstract.Decorator):
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

    def __exit__(self, *args, **kwargs):
        """exit Profiler decorator
        """

        # init
        stream = StringIO.StringIO()

        # execute
        self.profiler.disable()
        pstats.Stats(self.profiler, stream=stream).sort_stats(self._sortBy).print_stats()

        # return
        sys.stdout.write(stream.getvalue())
