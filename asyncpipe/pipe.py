from abc import ABC, abstractmethod
import asyncio
import inspect

from pipe_executor import PipeExecutor, AsyncPipe
from pipe_inspector import PipeInspector, PipeInspect

class Pipe():
    def __init__(self, 
                 pipe: tuple, 
                 *, 
                 pipe_executor: PipeExecutor = AsyncPipe(),
                 pipe_inspector: PipeInspector = PipeInspect(),
                 infinity_loop=False
                ):
        self.pipe = pipe
        self.pipe_executor = pipe_executor
        self.pipe_inspector = pipe_inspector
        self.infinity_loop = infinity_loop
        
        self.pipe_inspector.check_pipe_args(self.pipe) 
        

    async def __call__(self, **kwargs):
        while True:
            res = await self.pipe_executor.run(self.pipe, **kwargs)
            if not self.infinity_loop:
                break
        
        return res

    