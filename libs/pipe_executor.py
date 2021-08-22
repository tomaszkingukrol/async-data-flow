from collections.abc import Iterable
from typing import Callable

import asyncio
import inspect

from lib.pipe_def import PipeExecutor
from lib.pipe_errors import PIPEERRORPASSARGS, PIPEERRORARGSMERGE


class AsyncPipe(PipeExecutor):

    async def run(self, pipe: tuple, **kwargs):
        return await self._run_sequence(pipe, **kwargs)
    
    async def _run_sequence(self, pipe: tuple, **kwargs):
        loop = asyncio.get_event_loop()

        for p in pipe:
            if isinstance(p, Iterable):
                kwargs = await self._run_concurrent(p, **kwargs)
            elif isinstance(p, Callable):
                if not self._check_kwargs(p, **kwargs):
                    raise TypeError(PIPEERRORPASSARGS.format(p.__name__))
                if inspect.iscoroutinefunction(p):
                    kwargs = await p(**kwargs)
                else:          
                    args = self._map_kwargs_to_args(p, **kwargs)
                    kwargs = await loop.run_in_executor(None, p, *args)

        return kwargs        

    async def _run_concurrent(self, pipe: tuple, **kwargs):
        loop = asyncio.get_event_loop()
        tasks = list()

        for p in pipe:
            if isinstance(p, Iterable):
                kwargs = await self._run_sequence(p, **kwargs)
            elif isinstance(p, Callable):
                if not self._check_kwargs(p, **kwargs):
                    raise TypeError(PIPEERRORPASSARGS.format(p.__name__))
                if inspect.iscoroutinefunction(p):
                    tasks.append(loop.create_task(p(**kwargs)))
                else:          
                    args = self._map_kwargs_to_args(p, **kwargs)
                    tasks.append(loop.run_in_executor(None, p, *args))

        kwargs = dict()
        for task in tasks:
            kw = await task
            if kw:
                if set(kwargs.keys()).intersection(kw.keys()):
                    raise TypeError(PIPEERRORARGSMERGE.format(p.__name__))
                kwargs.update(kw)

        return kwargs
            
    @staticmethod
    def _map_kwargs_to_args(func: Callable, **kwargs) -> list:
        f_args = inspect.getfullargspec(func).args
        return [x[1] for x in sorted(kwargs.items(), key=lambda x:f_args.index(x[0]))]  

    @staticmethod
    def _check_kwargs(func: Callable, **kwargs) -> bool:
        return set(inspect.signature(func).parameters) == set(kwargs.keys())










