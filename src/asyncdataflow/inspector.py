from collections.abc import Iterable
from typing import Callable

import inspect

from .definition import DataFlowInspector
from .exceptions import DataFlowFunctionArgsError, DataFlowNotCallableError, DataFlowEmptyError, DataFlowNotTupleError


class DataFlowInspect(DataFlowInspector):
    ''' Function inspection defined in DataFlow
    '''
  
    def check_dataflow_args(self, dataflow: tuple):
        if isinstance(dataflow, tuple): 
            if dataflow:
                for task in dataflow:
                    if isinstance(task, Iterable):
                        self.check_dataflow_args(task)
                    elif isinstance(task, Callable):
                        _check_positional_or_keyword_args(task)
                    else:
                        raise DataFlowNotCallableError(task)
            else:
                raise DataFlowEmptyError()
        else:
            raise DataFlowNotTupleError(dataflow)


def _check_positional_or_keyword_args(func: Callable) -> bool:
    ''' Check that function has only POSITIONAL_OR_KEYWORD arguments.
    '''
    inspect_args = inspect.signature(func).parameters.values()
    for arg in inspect_args:
        if str(arg.kind) != 'POSITIONAL_OR_KEYWORD':
            raise DataFlowFunctionArgsError(func.__name__, arg)
