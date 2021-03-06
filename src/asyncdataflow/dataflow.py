from abc import ABC, abstractmethod
import asyncio
import inspect

from .executor import DataFlowExecutor, AsyncDataFlow
from .inspector import DataFlowInspector, DataFlowInspect


class DataFlow:
    ''' Callable class defining async-data-flow.

    Usage:
        DataFlow((foo, bar, baz))()
    '''

    def __init__(self, dataflow: tuple, *, run_forever = False, args_visibility = 'None'):
        ''' Initiate and validate Data Flow

        Args:
            dataflow: tuple - defining coroutine functions flow
            run_forever: bool - if true DataFlow is runnig in infinity loop (default False)
            max_sleep: float - max sleep time in seconds when DataFlow return empty dictionary (default 0)
            args_visibility: str 
                'None'    - initial arguments are visible only by first function in Data Flow, returned values are visible only 
                            by next functions in Data Flow
                'Initial' - initial arguments are visible by all function in Data Flow, returned values are visible only
                            by next functions in Data Flow
                'All'     - initial arguments and returned values are visible by all next functions in Data Flow
        '''
        self.dataflow = dataflow
        self.run_forever = run_forever

        self.executor = AsyncDataFlow(args_visibility)
        self.inspector = DataFlowInspect()
        self.inspector.check_dataflow_args(self.dataflow) 
        
    async def __call__(self, **kwargs):
        ''' Execute Data Flow
        '''
        while True:
            result = await self.executor.run(self.dataflow, **kwargs)
            if not self.run_forever:
                break
        return result

