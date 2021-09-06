from abc import ABC, abstractmethod
import asyncio
import inspect

from .executor import DataFlowExecutor, AsyncDataFlow
from .inspector import DataFlowInspector, DataFlowInspect


class DataFlow:
    def __init__(self, 
                 dataflow: tuple, 
                 *, 
                 executor: DataFlowExecutor = AsyncDataFlow(),
                 inspector: DataFlowInspector = DataFlowInspect(),
                ):
        self.dataflow = dataflow
        self.executor = executor
        self.inspector = inspector
        self.inspector.check_dataflow_args(self.dataflow) 
        
    async def __call__(self, **kwargs):
        return await self.executor.run(self.dataflow, **kwargs)


    