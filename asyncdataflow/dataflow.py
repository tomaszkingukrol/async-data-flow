from abc import ABC, abstractmethod
import asyncio
import inspect

from dataflow_executor import DataFlowExecutor, AsyncDataFlow
from dataflow_inspector import DataFlowInspector, DataFlowInspect


class DataFlow():
    def __init__(self, 
                 dataflow: tuple, 
                 *, 
                 dataflow_executor: DataFlowExecutor = AsyncDataFlow(),
                 dataflow_inspector: DataFlowInspector = DataFlowInspect(),
                ):
        self.dataflow = dataflow
        self.dataflow_executor = dataflow_executor
        self.dataflow_inspector = dataflow_inspector
        self.dataflow_inspector.check_dataflow_args(self.dataflow) 
        
    async def __call__(self, **kwargs):
        return await self.dataflow_executor.run(self.dataflow, **kwargs)


    