from functools import wraps

from .errors import ARGS_MAPPER_IN_KEY_ERROR, ARGS_MAPPER_ARGS_ERROR, ARGS_MAPPER_OUT_KEY_ERROR


def _input_mapper_previous(input: dict, kwargs: dict):
    return {k: kwargs[v] for k, v in input.items()}


def _input_mapper(input: dict, kwargs: dict):
    try:
        for k, v in input.items():
            value = kwargs[v]
            del kwargs[v]
            kwargs[k] = value
    except KeyError:
        raise TypeError(ARGS_MAPPER_IN_KEY_ERROR.format(v))
    return kwargs


def _output_mapper(output: dict or tuple or object, result: dict or tuple or object):
        if isinstance(output, dict):
            try:
                res = {k: result[v] for k, v in output.items()}
            except KeyError:
                raise TypeError(ARGS_MAPPER_OUT_KEY_ERROR)
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
            kwargs = _input_mapper(input, kwargs)
        try:
            result = func(**kwargs)
        except TypeError:
            raise TypeError(ARGS_MAPPER_ARGS_ERROR.format(func))  
        if output:
            result = _output_mapper(output, result)
        return result
    return wrapper