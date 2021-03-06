"""
python file object library
"""

# imports python
import json
import imp
import cPickle

# imports local
from . import _generic


# PYTHON FILE OBJECTS #


class JsonFile(_generic.File):
    """file object that manipulate a ``.json`` file on the file system
    """

    # ATTRIBUTES #

    _extension = 'json'

    # OBJECT COMMANDS #

    @classmethod
    def create(cls, path, content=None, **__):
        """create a json file

        :param path: path of the json file
        :type path: str

        :param content: content of the json file
        :type content: any

        :return: the created json file
        :rtype: :class:`cgp_generic_utils.files.JsonFile`
        """

        # errors
        if not _generic.Path(path).extension() == cls._extension:
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
        """read the json file

        :return: the content of the json file
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
    def create(cls, path, content=None, **__):
        """create a pkl file

        :param path: path of the pkl file
        :type path: str

        :param content: content of the pkl file
        :type content: any

        :return: the created pkl file
        :rtype: :class:`cgp_generic_utils.files.PklFile`
        """

        # errors
        if not _generic.Path(path).extension() == cls._extension:
            raise ValueError('{0} is not a PklFile path'.format(path))

        # get content
        content = content or {}

        # execute
        with open(path, 'wb') as toWrite:
            cPickle.dump(content, toWrite)

        # return
        return cls(path)

    # COMMANDS #

    def read(self):
        """read the pkl file

        :return: the content of the pkl file
        :rtype: any
        """

        # get state form config file
        with open(self.path(), 'rb') as toRead:
            data = cPickle.load(toRead)

        # return
        return data


class PyFile(_generic.File):
    """file object that manipulates a ``.py`` file on the file system
    """

    # ATTRIBUTES #

    _extension = 'py'

    # COMMANDS #

    def importAsModule(self):
        """import the python file as module

        :return: the module object
        :rtype: python
        """

        # import as module
        module = imp.load_source(self.baseName(withExtension=False), self.path())

        # return
        return module
