from functools import wraps


def _input_mapper(input: dict, kwargs: dict):
    return {k: kwargs[v] for k, v in input.items()}


def _output_mapper(output: dict or tuple or object, result: dict or tuple or object):
        if isinstance(output, dict):
            res = {k: result[v] for k, v in output.items()}
        elif isinstance(output, list):
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
        result = func(**kwargs)
        if output:
            result = _output_mapper(output, result)
        return result
    return wrapper