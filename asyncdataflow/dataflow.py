from abc import ABC, abstractmethod
import asyncio
import inspect

from .executor import DataFlowExecutor, AsyncDataFlow
from .inspector import DataFlowInspector, DataFlowInspect


class DataFlow:
    ''' Callable class defining async-data-flow. DataFlwo is defined as tuple.
Args:
dataflow: tuple - tuple defining DataFlow
is_permanent: bool (default False) - True run DataFlow in infinity loop
args_publish: str (default 'None') - Initial arguments re passed only to first function, 
'Inintial' - iniatial argumets are passed to all functions in DataFlow
'All' - all returned dictionaries by functions are conveted to args and passed to next functions in DataFlow
    '''
    def __init__(self, 
                 dataflow: tuple, 
                 *, 
                 executor: DataFlowExecutor = AsyncDataFlow(),
                 inspector: DataFlowInspector = DataFlowInspect(),
                 is_permanent = False,
                 args_publish = 'None' # 'Initial', 'All'
                ):
        self.dataflow = dataflow
        self.executor = executor
        self.inspector = inspector
        self.is_permanent = is_permanent
        self.inspector.check_dataflow_args(self.dataflow) 
        
    async def __call__(self, **kwargs):
        while True:
            result = await self.executor.run(self.dataflow, **kwargs)
            if not self.is_permanent:
                break
        return result

    