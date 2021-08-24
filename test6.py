from functools import wraps


def arg_mapper(func, input: dict = None, output: dict = None):
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
    

def foo(a, b):
    return {'a': a, 'b': b}


c = arg_mapper(foo, input={'a': 'input', 'b': 'd'}, output={'input': 'a', 'f': 'b'})(input=3, d=5)

print(c)