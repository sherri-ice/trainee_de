import abc
import re
from typing import Optional


class PrefixSolver(abc.ABC):
    """
    Abstract class for resolving S3 bucket prefixes depending on type of incoming file name.
    """

    def get_prefix(self, filename_str: str) -> Optional[str]:
        """
        The get_prefix function takes in a filename (string) and returns the prefix of
        requested file depends on abstract class implementation.

        :param self: Represent the instance of the class
        :param filename_str: str: Specify the filename to get prefix
        :return: The prefix of the input filename.
        """
        ...


class YearPrefixSolver(PrefixSolver):
    """
    Class which implements abstract PrefixSolver, returns year prefix.
    """
    def get_prefix(self, filename_str: str) -> Optional[str]:
        """
        The get_prefix function takes a filename string as input and returns the year.
        The function uses regular expressions to match a four-digit year format at the beginning of
        the filename string, which is assumed to be in YYYY format. If no match is found,
        None is returned.

        :param self: Refer to the instance of the class
        :param filename_str: str: Specify the name of the file that is being passed in
        :return: The year from the filename or None
    """
        year_match = re.match(r'([1-2][0-9]{3})', filename_str)
        if year_match is not None:
            return year_match.group(1)


class PredefinedPrefixSolver(PrefixSolver):
    """
        Class which implements abstract PrefixSolver, returns the predefined name as a prefix.
    """
    def __init__(self, predefined_prefix: str):
        """
        It sets up the instance of the class and sets predefined name for the prefixes.

        :param self: Represent the instance of the class
        :param predefined_prefix: str: Set the _actual_name attribute
        :return: Nothing
        """
        self._predefined_prefix = predefined_prefix

    def get_prefix(self, filename_str: str) -> Optional[str]:

        """
        Returns predefined prefix for file.

        :param self: Refer to the object itself
        :param filename_str: str
        :return: Predefined prefix
        """
        return self._predefined_prefix
