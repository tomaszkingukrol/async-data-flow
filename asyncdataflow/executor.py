from typing import Callable

import asyncio
import inspect

from .definition import DataFlowExecutor
from .errors import DATAFLOW_MERGE_ERROR


class AsyncDataFlow(DataFlowExecutor):

    async def run(self, dataflow: tuple, **kwargs):
        return await self._run_sequence(dataflow, **kwargs)
    
    async def _run_sequence(self, dataflow: tuple, **kwargs):
        loop = asyncio.get_event_loop()

        for task in dataflow:
            if isinstance(task, tuple):
                kwargs = await self._run_concurrent(task, **kwargs)
            elif isinstance(task, Callable):
                kw = self._map_kwargs(task, kwargs)
                if kw:
                    if inspect.iscoroutinefunction(task):
                        kwargs = await task(**kw)
                    else:          
                        args = self._map_kwargs_to_args(task, kw)
                        kwargs = await loop.run_in_executor(None, task, *args)

        return kwargs        

    async def _run_concurrent(self, dataflow: tuple, **kwargs):
        loop = asyncio.get_event_loop()
        tasks = list()

        for task in dataflow:
            if isinstance(task, tuple):
                kwargs = await self._run_sequence(task, **kwargs)
            elif isinstance(task, Callable):
                kw = self._map_kwargs(task, kwargs)
                if kw:
                    if inspect.iscoroutinefunction(task):
                        tasks.append(loop.create_task(task(**kw)))
                    else:          
                        args = self._map_kwargs_to_args(task, kw)
                        tasks.append(loop.run_in_executor(None, task, *args))

        if tasks:
            kwargs = dict()
            for task in tasks:
                kw = await task
                if kw:
                    if set(kwargs.keys()).intersection(kw.keys()):
                        raise TypeError(DATAFLOW_MERGE_ERROR.format(task.__name__))
                    kwargs.update(kw)

        return kwargs

    @staticmethod
    def _map_kwargs (func: Callable, kwargs) -> dict:
        f_args = inspect.getfullargspec(func).args
        return {k: kwargs[k] for k in f_args}
            
    @staticmethod
    def _map_kwargs_to_args(func: Callable, kwargs) -> list:
        f_args = inspect.getfullargspec(func).args
        return [x[1] for x in sorted(kwargs.items(), key=lambda x:f_args.index(x[0]))]  









