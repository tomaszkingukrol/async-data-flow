from collections.abc import Iterable
from typing import Callable, Tuple

import inspect

from .definition import DataFlowInspector
from .errors import DATAFLOW_ARGS_ERROR, DATAFLOW_DEFINITION_ERROR, DATAFLOW_EMPTY_ERROR


class DataFlowInspect(DataFlowInspector):
  
    def check_dataflow_args(self, dataflow: tuple) -> set:
        if isinstance(dataflow, tuple) and dataflow:
            for task in dataflow:
                if isinstance(task, tuple):
                    task_args = self.check_dataflow_args(task)
                elif isinstance(task, Callable):
                    if not self._is_positional_or_keyword_only(task):
                        raise TypeError(DATAFLOW_ARGS_ERROR.format(task.__name__))
                else:
                    raise TypeError(DATAFLOW_DEFINITION_ERROR.format(task))
        else:
            raise TypeError(DATAFLOW_EMPTY_ERROR)

    @staticmethod
    def _is_positional_or_keyword_only(func: Callable) -> bool:
        inspect_args = inspect.signature(func).parameters.values()
        return all([str(arg.kind) == 'POSITIONAL_OR_KEYWORD' for arg in inspect_args])