from functools import wraps
from .exceptions import ArgsMapperInputKeyError, ArgsMapperOutputKeyError, ArgsMapperArgsError


def _input_mapper(func_name: str, input: dict, kwargs: dict):
    for k, v in input.items():
        try:
            value = kwargs[v]
            del kwargs[v]
            kwargs[k] = value
        except KeyError:
            raise ArgsMapperInputKeyError(func_name, kwargs, v)
    return kwargs


def _output_mapper(func_name: str, output: dict or tuple or object, result: dict or tuple or object):
    if isinstance(output, dict):
        res = dict()
        for k, v in output.items():
            try:
                res[k] = result[v]
            except KeyError:
                raise ArgsMapperOutputKeyError(func_name, result, v)
    elif isinstance(output, tuple):
        res = {k: v for k, v in zip(output, result)}
    elif output:
        res = {output: result}
    else:
        res = result
    return res


def args_mapper(func, input: dict = None, output: dict = None):
    input, output = input, output
    @wraps(func)
    def wrapper(**kwargs):
        if input: 
            kwargs = _input_mapper(func.__name__, input, kwargs)
        try:
            result = func(**kwargs)
        except TypeError:
            raise ArgsMapperArgsError(func.__name__, kwargs)  
        if output:
            result = _output_mapper(func.__name__, output, result)
        return result
    return wrapper