from functools import wraps
import asyncio
import inspect

from .exceptions import DispatchError


def sdispatch(fn):
    '''Dispatch function in step of DataFlow definiotion. Function return previously registered function.
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


def ddispatch(fn):
    '''Dispatch function in running DataFlow. Function run previously registered function.
    '''
    registry = dict()
    registry[''] = fn
    
    def register(key_):
        def inner(fn):
            registry[key_] = fn
        return inner
   
    @wraps(fn)
    async def wrapper(*args, _dispatch_key, **kwargs):
        if _dispatch_key not in registry:
            raise DispatchError(_dispatch_key)
        fn = registry[_dispatch_key]
        if inspect.iscoroutinefunction(fn):
            result = await fn(*args, **kwargs)
        else:
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(None, fn, *args)
        return result
    
    wrapper.register = register
    wrapper.registry = registry.keys()

    return wrapper












