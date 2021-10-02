from functools import wraps
import asyncio
import inspect

from .exceptions import DispatchError


def fdispatch(fn):
    '''A function factory decorator. Any coroutine function and sync function can be registered and dispatched 
    using first positional argument.

    Usage:
        @fdispatch
        def foo(key): ...

        @foo.register('a')
        async def _a(): ...

        df = DataFlow((foo('a'),))
    '''
    registry = dict()
    registry[''] = fn
    
    def register(key_):
        def inner(fn):
            registry[key_] = fn
        return inner
   
    @wraps(fn)
    def wrapper(_dispatch_key):
        if _dispatch_key not in registry:
            raise DispatchError(_dispatch_key)
        return registry[_dispatch_key]

    wrapper.register = register
    wrapper.registry = registry.keys()

    return wrapper












