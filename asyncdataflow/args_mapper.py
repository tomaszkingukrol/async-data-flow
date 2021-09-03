from functools import wraps
from .exceptions import ArgsMapperInputKeyError, ArgsMapperOutputKeyError, ArgsMapperArgsError


def _input_mapper(func_name: str, input: dict, kwargs: dict):
    try:
        for k, v in input.items():
            value = kwargs[v]
            del kwargs[v]
            kwargs[k] = value
    except KeyError:
        raise ArgsMapperInputKeyError(v, kwargs, func_name)
    return kwargs


def _output_mapper(func_name: str, output: dict or tuple or object, result: dict or tuple or object):
    if isinstance(output, dict):
        try:
            res = dict()
            for k, v in output.items():
                res[k] = result[v]
        except KeyError:
            raise ArgsMapperOutputKeyError(v, result, func_name)
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
            raise ArgsMapperArgsError(kwargs, func.__name__)  
        if output:
            result = _output_mapper(func.__name__, output, result)
        return result
    return wrapper