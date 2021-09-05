from asyncdataflow import DataFlow
from asyncdataflow.exceptions import DataFlowFunctionArgsError, DataFlowNotCallableError, DataFlowEmptyError

def foo(a, b):
    return {'a': a, 'b': b}



bar = args_mapper(func=foo, input={'a': 'd'})
try:
    bar(c=1, b=2)
except ArgsMapperInputKeyError as e:
    print(e)

bar = args_mapper(func=foo, output={'a': 'd'})
try:
    bar(a=1, b=2)
except ArgsMapperOutputKeyError as e:
    print(e)

bar = args_mapper(func=foo, input={'c': 'd'})
try:
    bar(d=1, b=2)
except ArgsMapperArgsError as e:
    print(e)
