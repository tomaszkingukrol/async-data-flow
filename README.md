# async-data-flow
Module allow to bundle coroutine functions and synchronous functions into single package inside which functions are executed sequentially (one-by-one). DataFlow package is executed as coroutine. Synchronous function inside package are executed in separated threads. Functions inside package must use only keyword arguments (technically POSITIONAL_OR_KEYWORD arguments) and must return dictionary which can be unpacked and passed to next fuction in package as the arguments. 
Module depends on asyncio module. 

    import asyncio
    from asyncdataflow import DataFlow

    async def foo(a, b):
        return {'c': a, 'd': b}

    async def bar(c, d):
        return {'e': c+d}

    async def main():
        dataflow = DataFlow((foo, bar))
        result = await dataflow(a=1, b=1)

    asyncio.run(main())

DataFlow package is defined as tuple (foo, bar) during DataFlow class instantiation. Initial argumets are passed to DataFlow package during calling DataFlow class instance. Dictionary returned by first function is unpacked and passed as argumetns to next function. Package return dictionary which was returned by last function.

### argument visibility

During defining DataFlow object we can specify argumets visibility (args_visibility: str): 
- 'None': initial arguments are visible only by first function in Data Flow, returned values are visible only by next functions in Data Flow
- 'Initial': initial arguments are visible by all function in Data Flow, returned values are visible only by next functions in Data Flow
- 'All': initial arguments and returned values are visible by all next functions in Data Flow

Example:

    import asyncio
    from asyncdataflow import DataFlow

    async def foo(a):
        return {'c': a}

    async def bar(b, c):
        return {'e': b+c}

    async def main():
        dataflow = DataFlow((foo, bar), args_visibility = 'Initial')
        result = await dataflow(a=1, b=1)

    asyncio.run(main())

### amapper

To use in DataFlow package function which do not return dictionary or we want to map keyword arguments to another key we can use amapper decorator:

    from asyncdataflow import amapper

    async def foo(a):
        return a
    foo = amapper(foo, input={'a': 'in'}, output='out')  
    foo(in=...) -> {'out': a}

    async def bar(a):
        return a, a*2
    bar = args_mapper(bar, input={'a': 'in'}, output=('out1', 'out2'))  
    bar(int=...) -> {'out1': a, 'out2': a*2}

    async def baz(a):
        return {'o1': a, 'o2': a*2}
    baz = args_mapper(baz, input={'a': 'in'}, output={'o1': 'out1', 'o2': 'out2'})  
    baz(int=...) -> {'out1': a, 'out2': a*2}

### fdispatch

To dispatch function in DataFlow packare we can use fdispatch decorator:

    import asyncio
    from asyncdataflow import DataFlow, fdispatch

    @fdispatch
    def foo(key): pass

    @foo.register('bar')
    async def _(a): return {'b': a}

    @foo.register('baz')
    async def _(b): return {'c': b}

    dataflow = DataFlow((foo('bar'),foo('baz')))

## Concurrent execution inside DataFlow package

DataFlow package is defined as a tuple inside which functions are executed sequentially (one by one). We can add nested tuple inside which functions will be executed concurrently:

    import asyncio
    from asyncdataflow import DataFlow

    async def foo(a):
        return {'foo': a}

    async def bar(a):
        return {'bar': a}

    async def merge(foo, bar):
        return {'merged': foo+bar}

    dataflow = DataFlow(((foo, bar), merge))

foo and bar functions are executed concurrently, returned dictionary by them are merged to one. When we add next nested tuple, inside them - function will be executed sequencially, and so on.

## Error handling

DataFlow exception hierarchy:

    +-- DataFlowException(Exception):
        +-- DataFlowError:
            +-- DataFlowRunItemError:
                +-- DataFlowMergeResultError:
                +-- DataFlowFunctionResultError:
            +-- DataFlowDefinitionError:
                +-- DataFlowFunctionArgsError:
                +-- DataFlowNotCallableError:
                +-- DataFlowNotTupleError:
                +-- DataFlowEmptyError:
            +-- ArgsMapperError:
                +-- ArgsMapperInputKeyError:
                +-- ArgsMapperOutputKeyError:
                +-- ArgsMapperArgsError:
        +-- DispatchError:

Desciption:
- DataFlowMergeResultError: raised when returned dictionaries cannot be merged 
- DataFlowFunctionResultError: raised when function return other value than dictionary
- DataFlowFunctionArgsError: raised when function has another arguments than POSITIONAL_OR_KEYWORD arguments
- DataFlowNotCallableError: raised when DataFlow contain not callable objects
- DataFlowNotTupleError: raised when DataFlow is defined not as tuple
- DataFlowEmptyError: raised when DataFlow or sub-DataFlow is empty
- ArgsMapperInputKeyError: raised when mapping defined in input argument do not correspond to initial function arguments
- ArgsMapperOutputKeyError: raised when mapping defined in output argument do not correspond to returned from function dictionary
- ArgsMapperArgsError: raised when passed arguments to functions do not corespond to origin arguments
- DispatchError: raised when dispatched function wasn't registered

