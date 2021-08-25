from functools import wraps


def args_mapper(func, input: dict = None, output: dict = None):
    input_, output_ = input, output
    @wraps(func)
    def wrapper(**kwargs):
        if input_:
            kw = {k: kwargs[v] for k, v in input_.items()}
        else:
            kw = kwargs
        result = func(**kw)
        if output_:
            res = {k: result[v] for k, v in output_.items()}
        else:
            res = result
        return res
    return wrapper