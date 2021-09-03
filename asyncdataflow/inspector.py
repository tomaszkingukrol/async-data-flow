from collections.abc import Iterable
from typing import Callable, Tuple

import inspect

from .definition import DataFlowInspector
from .exceptions import DataFlowFunctionArgsError, DataFlowNotCallableError, DataFlowEmptyError


class DataFlowInspect(DataFlowInspector):
  
    def check_dataflow_args(self, dataflow: tuple) -> set:
        if isinstance(dataflow, tuple) and dataflow:
            for task in dataflow:
                if isinstance(task, tuple):
                    task_args = self.check_dataflow_args(task)
                elif isinstance(task, Callable):
                    self._check_positional_or_keyword_args(task)
                else:
                    raise DataFlowNotCallableError(task)
        else:
            raise DataFlowEmptyError()

    @staticmethod
    def _check_positional_or_keyword_args(func: Callable) -> bool:
        inspect_args = inspect.signature(func).parameters.values()
        for arg in inspect_args:
            if str(arg.kind) != 'POSITIONAL_OR_KEYWORD':
                raise DataFlowFunctionArgsError(arg, func.__name__)
