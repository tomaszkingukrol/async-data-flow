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
                 infinity_loop=False
                ):
        self.dataflow = dataflow
        self.dataflow_executor = dataflow_executor
        self.dataflow_inspector = dataflow_inspector
        self.infinity_loop = infinity_loop
        
        self.dataflow_inspector.check_dataflow_args(self.dataflow) 
        

    async def __call__(self, **kwargs):
        while True:
            res = await self.dataflow_executor.run(self.dataflow, **kwargs)
            if not self.infinity_loop:
                break
        
        return res

    