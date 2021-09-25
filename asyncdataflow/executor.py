from typing import Callable

import asyncio
import inspect

from .definition import DataFlowExecutor
from .exceptions import DataFlowMergeResultError


class AsyncDataFlow(DataFlowExecutor):
    ''' Define executor of coroutine functions and sync function in async-data-flow
    '''

    def __init__(self, args_visibility):
        self._add_initial_args = False
        self._add_args = False
        self._init_args = dict()
        if args_visibility == 'Initial':
            self._add_initial_args = True
        elif args_visibility == 'All':
            self._add_args = True

    async def run(self, dataflow: tuple, **kwargs):
        ''' Run Data Flow
        '''
        if self._add_initial_args:
            self._init_args = kwargs
        return await self._run_sequence(dataflow, **kwargs)
    
    async def _run_sequence(self, dataflow: tuple, **kwargs):
        ''' Run function in Data Flow sequentially
        '''
        loop = asyncio.get_event_loop()
        for task in dataflow:
            _input_args = dict()
            if self._add_args:
                _input_args = kwargs

            if isinstance(task, tuple):
                kwargs = await self._run_concurrent(task, **kwargs)
            elif isinstance(task, Callable):
                kw = _map_kwargs(task, kwargs)
                if kw:
                    if inspect.iscoroutinefunction(task):
                        kwargs = await task(**kw)
                    else:          
                        args = _map_kwargs_to_args(task, kw)
                        kwargs = await loop.run_in_executor(None, task, *args)

            _merge_kwargs(kwargs, self._init_args, _input_args)

        return kwargs   

    async def _run_concurrent(self, dataflow: tuple, **kwargs):
        ''' Run function in Data Flow concurrently
        '''
        _input_args = dict()
        if self._add_args:
            _input_args = kwargs

        loop = asyncio.get_event_loop()
        tasks = list()
        for task in dataflow:
            if isinstance(task, tuple):
                kwargs = await self._run_sequence(task, **kwargs)
            elif isinstance(task, Callable):
                kw = _map_kwargs(task, kwargs)
                if kw:
                    if inspect.iscoroutinefunction(task):
                        tasks.append(loop.create_task(task(**kw)))
                    else:          
                        args = _map_kwargs_to_args(task, kw)
                        tasks.append(loop.run_in_executor(None, task, *args))

        if tasks:
            kwargs = dict()
            for task in tasks:
                kw = await task
                _merge_kwargs(kwargs, kw)

        _merge_kwargs(kwargs, self._init_args, _input_args)

        return kwargs


def _merge_kwargs(origin: dict, *to_add: dict) -> dict:
    ''' Merge collection of dictionaries. Raise error when keys are the same in both merged dictionaries but values are different
    '''
    if not origin:
        origin = dict()
    for dict_ in to_add:
        if dict_:
            if origin:
                intersection_ = set(origin.keys()).intersection(dict_.keys())
                if intersection_:
                    a = {k: v for k, v in origin.items() if k in intersection_}
                    b = {k: v for k, v in dict_.items() if k in intersection_}
                    if a != b:
                        raise DataFlowMergeResultError(dict_.keys(), origin.keys())
            origin.update(dict_)  
    return origin      


def _map_kwargs(func: Callable, kwargs) -> dict:
    ''' Map dictioanry to argumetns of called function
    '''
    f_args = inspect.getfullargspec(func).args
    try:
        result = {k: kwargs[k] for k in f_args}
    except KeyError:
        result = None
    return result
        

def _map_kwargs_to_args(func: Callable, kwargs) -> list:
    ''' Map kwargs (dictionary) to list in order defined by functions arguments
    '''
    f_args = inspect.getfullargspec(func).args
    return [x[1] for x in sorted(kwargs.items(), key=lambda x:f_args.index(x[0]))]  









