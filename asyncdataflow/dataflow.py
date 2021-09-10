from abc import ABC, abstractmethod
import asyncio
import inspect

from .executor import DataFlowExecutor, AsyncDataFlow
from .inspector import DataFlowInspector, DataFlowInspect


class DataFlow:
    ''' Callable class defining async-data-flow.
    '''
    def __init__(self, 
                 dataflow: tuple, 
                 *, 
                 executor: DataFlowExecutor = AsyncDataFlow(),
                 inspector: DataFlowInspector = DataFlowInspect(),
                 is_permanent = False
                ):
        self.dataflow = dataflow
        self.executor = executor
        self.inspector = inspector
        self.is_permanent = is_permanent
        # self.inspector.check_dataflow_args(self.dataflow) 
        
    async def __call__(self, **kwargs):
        while True:
            result = await self.executor.run(self.dataflow, **kwargs)
            if not self.is_permanent:
                break
        return result

    