from collections.abc import Iterable
from typing import Callable

import inspect

from dataflow_definition import DataFlowInspector
from dataflow_error import DATAFLOWERRORROUTINE, DATAFLOWERRORARGS, DATAFLOWERRORCONARGS


class DataFlowInspect(DataFlowInspector):
  
    def check_dataflow_args(self, dataflow: tuple, is_sequence=True) -> set:
        dataflow_args = set()

        for task in dataflow:
            if isinstance(task, Iterable):
                task_args = self.check_dataflow_args(task, is_sequence=(is_sequence+1)%2)
            elif isinstance(task, Callable):
                if not self._is_positional_or_keyword_only(task):
                    raise TypeError(DATAFLOWERRORARGS)
                task_args = self._get_args_as_set(task)
            else:
                raise TypeError(DATAFLOWERRORROUTINE)

            dataflow_args = dataflow_args or task_args
            if not is_sequence and dataflow_args and dataflow_args != task_args:
                raise TypeError(DATAFLOWERRORCONARGS)
        
        return dataflow_args

    @staticmethod
    def _is_positional_or_keyword_only(func: Callable) -> bool:
        inspect_args = inspect.signature(func).parameters.values()
        return all([str(arg.kind) == 'POSITIONAL_OR_KEYWORD' for arg in inspect_args])

    @staticmethod
    def _get_args_as_set(func: Callable) -> set:
        return set(inspect.signature(func).parameters)