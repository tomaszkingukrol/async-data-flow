from collections.abc import Iterable
from typing import Callable

import asyncio
import inspect

from dataflow_definition import DataFlowExecutor
from dataflow_error import DATAFLOWERRORPASSARGS, DATAFLOWERRORARGSMERGE


class AsyncDataFlow(DataFlowExecutor):

    async def run(self, dataflow: tuple, **kwargs):
        return await self._run_sequence(dataflow, **kwargs)
    
    async def _run_sequence(self, dataflow: tuple, **kwargs):
        loop = asyncio.get_event_loop()

        for task in dataflow:
            if isinstance(task, Iterable):
                kwargs = await self._run_concurrent(task, **kwargs)
            elif isinstance(task, Callable):
                if not self._check_kwargs(task, **kwargs):
                    raise TypeError(DATAFLOWERRORPASSARGS.format(task.__name__))
                if inspect.iscoroutinefunction(task):
                    kwargs = await task(**kwargs)
                else:          
                    args = self._map_kwargs_to_args(task, **kwargs)
                    kwargs = await loop.run_in_executor(None, task, *args)

        return kwargs        

    async def _run_concurrent(self, dataflow: tuple, **kwargs):
        loop = asyncio.get_event_loop()
        tasks = list()

        for task in dataflow:
            if isinstance(task, Iterable):
                kwargs = await self._run_sequence(task, **kwargs)
            elif isinstance(task, Callable):
                if not self._check_kwargs(task, **kwargs):
                    raise TypeError(DATAFLOWERRORPASSARGS.format(task.__name__))
                if inspect.iscoroutinefunction(task):
                    tasks.append(loop.create_task(task(**kwargs)))
                else:          
                    args = self._map_kwargs_to_args(task, **kwargs)
                    tasks.append(loop.run_in_executor(None, task, *args))

        kwargs = dict()
        for task in tasks:
            kw = await task
            if kw:
                if set(kwargs.keys()).intersection(kw.keys()):
                    raise TypeError(DATAFLOWERRORARGSMERGE.format(task.__name__))
                kwargs.update(kw)

        return kwargs
            
    @staticmethod
    def _map_kwargs_to_args(func: Callable, **kwargs) -> list:
        f_args = inspect.getfullargspec(func).args
        return [x[1] for x in sorted(kwargs.items(), key=lambda x:f_args.index(x[0]))]  

    @staticmethod
    def _check_kwargs(func: Callable, **kwargs) -> bool:
        return set(inspect.signature(func).parameters) == set(kwargs.keys())










