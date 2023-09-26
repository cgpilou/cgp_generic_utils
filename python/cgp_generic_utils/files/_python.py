"""
python file object library
"""

# imports python
import json
import imp
import pickle

# imports local
import cgp_generic_utils.python
from . import _generic
from . import _api


# PYTHON FILE OBJECTS #


class JsonFile(_generic.File):
    """file object that manipulate a ``.json`` file on the file system
    """

    # ATTRIBUTES #

    _extension = 'json'

    # OBJECT COMMANDS #

    @classmethod
    def create(cls, path, content=None, **kwargs):
        """create a json file

        :param path: path of the jsonFile
        :type path: str

        :param content: content to set into the jsonFile
        :type content: Any

        :return: the created jsonFile
        :rtype: :class:`cgp_generic_utils.files.JsonFile`
        """

        # errors
        if not _api.getExtension(path) == cls._extension:
            raise ValueError('{0} is not a JsonFile path'.format(path))

        # get content
        content = content or {}

        # execute
        with open(path, 'w') as toWrite:
            json.dump(content, toWrite, indent=4)

        # return
        return cls(path)

    # COMMANDS #

    def read(self):
        """read the jsonFile

        :return: the content of the jsonFile
        :rtype: any
        """

        # get state form config file
        with open(self.path(), 'r') as toRead:
            data = json.load(toRead)

        # return
        return data


class PklFile(_generic.File):
    """file object that manipulate a ``.pkl`` file on the file system
    """

    # ATTRIBUTES #

    _extension = 'pkl'

    # OBJECT COMMANDS #

    @classmethod
    def create(cls, path, content=None, **kwargs):
        """create a pklFile

        :param path: path of the pklFile
        :type path: str

        :param content: content to set into the pklFile
        :type content: Any

        :return: the created pklFile
        :rtype: :class:`cgp_generic_utils.files.PklFile`
        """

        # errors
        if not _api.getExtension(path) == cls._extension:
            raise ValueError('{0} is not a PklFile path'.format(path))

        # get content
        content = content or {}

        # execute
        with open(path, 'wb') as toWrite:
            pickle.dump(content, toWrite, protocol=2)  # using protocol=2 to ensure compatibility py2/py3

        # return
        return cls(path)

    # COMMANDS #

    def read(self):
        """read the file

        :return: the content of the pklFile
        :rtype: any
        """

        # get state form config file
        with open(self.path(), 'rb') as toRead:
            data = pickle.load(toRead)

        # return
        return data


class PyFile(_generic.File):
    """file object that manipulates a ``.py`` file on the file system
    """

    # ATTRIBUTES #

    _extension = 'py'

    # COMMANDS #

    def importAsModule(self):
        """import the pyFile as module

        :return: the module object
        :rtype: python
        """

        # import as module
        module = imp.load_source(self.baseName(withExtension=False), self.path())

        # return
        return module
