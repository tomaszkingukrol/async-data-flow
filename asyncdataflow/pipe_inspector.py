from collections.abc import Iterable
from typing import Callable

import inspect

from pipe_def import PipeInspector
from pipe_errors import PIPEERRORROUTINE, PIPEERRORARGS, PIPEERRORCONARGS


class PipeInspect(PipeInspector):
  
    def check_pipe_args(self, pipe: tuple, is_sequence=True) -> set:
        args = set()

        for p in pipe:
            if isinstance(p, Iterable):
                a = self.check_pipe_args(p, is_sequence=(is_sequence+1)%2)
            elif isinstance(p, Callable):
                if not self._is_positional_or_keyword_only(p):
                    raise TypeError(PIPEERRORARGS)
                a = self._get_args_as_set(p)
            else:
                raise TypeError(PIPEERRORROUTINE)

            args = args or a
            if not is_sequence and args and args != a:
                raise TypeError(PIPEERRORCONARGS)
        
        return args

    @staticmethod
    def _is_positional_or_keyword_only(func: Callable) -> bool:
        inspect_args = inspect.signature(func).parameters.values()
        return all([str(p.kind) == 'POSITIONAL_OR_KEYWORD' for p in inspect_args])

    @staticmethod
    def _get_args_as_set(func: Callable) -> set:
        return set(inspect.signature(func).parameters)