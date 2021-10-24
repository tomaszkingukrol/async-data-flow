from functools import wraps
from .exceptions import ArgsMapperInputKeyError, ArgsMapperOutputKeyError, ArgsMapperArgsError


def _input_mapper(func_name: str, input: dict, kwargs: dict):
    '''Map input arguments
    '''
    for k, v in input.items():
        try:
            value = kwargs[v]
            del kwargs[v]
            kwargs[k] = value
        except KeyError:
            raise ArgsMapperInputKeyError(func_name, kwargs, v) from None
    return kwargs


def _output_mapper(func_name: str, output: dict or tuple or object, result: dict or tuple or object):
    ''' Map returned values:
    - single value
    - tuple
    - dictionary
    '''
    if isinstance(output, dict):
        res = dict()
        for k, v in output.items():
            try:
                res[k] = result[v]
            except KeyError:
                raise ArgsMapperOutputKeyError(func_name, result, v) from None
    elif isinstance(output, tuple):
        res = {k: v for k, v in zip(output, result)}
    elif output:
        res = {output: result}
    else:
        res = result
    return res


def amapper(func, input: dict = None, output: dict = None):
    ''' A function decorator. Can do two things:
    - map input arguments to origin set of function arguments 
    - map returned value to dictionary required by Data Flow.
    
    Usage:
        async def foo(a):
            return a
        bar = amapper(foo, input={'a': 'input'}, output='a')  
        avait DataFlow((bar,))(input = 1) -> {'a': 1}

        async def foo(a):
            return a, a*2
        bar = args_mapper(foo, input={'a': 'input'}, output=('a', '2a')) 
        avait DataFlow((bar,))(input = 1) -> {'a': 1, '2a': 2}

        async def foo(a):
            return {'a': a, '2a': 2*a}
        bar = args_mapper(foo, input={'a': 'input'}, output={'a': 'A', '2a': '2A'})  
        avait DataFlow((bar,))(input = 1) -> {'A': 1, '2A': 2}
    '''
    input, output = input, output
    @wraps(func)
    def wrapper(**kwargs):
        if input: 
            kwargs = _input_mapper(func.__name__, input, kwargs)
        try:
            result = func(**kwargs)
        except TypeError:
            raise ArgsMapperArgsError(func.__name__, kwargs) from None
        if output:
            result = _output_mapper(func.__name__, output, result)
        return result
    return wrapper