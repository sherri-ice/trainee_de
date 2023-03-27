import abc
import re
from typing import Optional


class PrefixSolver(abc.ABC):
    def get_prefix(self, input_str: str) -> Optional[str]:
        ...


class YearPrefixSolver(PrefixSolver):
    def get_prefix(self, input_str: str) -> Optional[str]:
        year_match = re.match(r'([1-2][0-9]{3})', input_str)
        if year_match is not None:
            return year_match.group(1)


class DummyPrefixSolver(PrefixSolver):
    def get_prefix(self, input_str: str) -> Optional[str]:
        # Just returns 'common' prefix for stand-alone files
        return 'common'
