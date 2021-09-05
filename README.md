# async-data-flow
Bundle coroutines into package which can be executed as a single coroutine. In the package, coroutines can be executed sequentially or concurrently. Module depends on asyncio and can co-operate with many async libraries as aiohttp, aiomysql and others. If some process cannot be implemented asynchronously, the module supports the execution of synchronous functions as separated threads. 

## Introduction
Simple data flow process could be composed from two elements: get data and write data. Both can be implemented as async functions but must be executed sequentially:

    import asyncio
    from asyncdataflow import DataFlow

    async def source(endpoint):
        ...
        return {'source': endpoint, 'data': [1,2,3,4,5,6]}

    async def destination(source, data):
        ...
        return {'status': 0}

    async def main():
        dataflow_definition = (source, destination)
        dataflow = DataFlow(dataflow_definition)
        result = await dataflow(endpoint=endpoint)

    asyncio.run(main())

In this example, we call single package grabbing data from source and put them to destination. Of course we can execute many of these packages using asyncio.create_task() function.

### passing arguments and retrieving results in DataFlow

DataFlow class is Callable. When we create them we define elements of DataFlow as a tuple containing functions:

    (source, destination)

We pass initial arguments to DataFlow when we call DataFlow class object. We must use only keyword arguments:

    await dataflow(endpoint=endpoint) 
    
Initial arguments are passed to the first element in DataFlow. All functions used in DataFlow must use only POSITIONAL_OR_KEYWORD arguments. Returned values from functions must be a dictionary which is unpacked as keyword arguments passing to the next element in DataFlow. Next element checks if it can pass arguments to its own function, if yes, it executes this function, if not, it passes arguments to the next element. This process continues until the end of DataFlow package. The package returns the dictionary from the last executed function.

### args_mapper

We can use in DataFlow functions which return other values than the dictionary. We can transform passed arguments and returned values using args_mapper:

    from asyncdataflow import args_mapper

    async def foo(a):
        ...
        return data

    bar = args_mapper(foo, input={'a': 'endpoint'}, output='data')  

    bar(endpoint=...) -> {'data': data}

Python function can return multile outputs as tuple:

    async def foo(a):
        ...
        return source, data

    bar = args_mapper(foo, input={'a': 'endpoint'}, output=('source', 'data'))  

    bar(endpoint=...) -> {'source': source, 'data': data}

Sometimes we should map returned dictionary to another one:

    async def foo(a):
        ...
        return {'source': source, 'data': data}

    bar = args_mapper(foo, input={'a': 'endpoint'}, output={'source': 'source_a', 'data': 'data_a'})  

    bar(endpoint=...) -> {'source'_a: source, 'data_a': data}

### passing extra parameters

If we need to pass extra parameters to not the first function in DataFlow, we must do that before DataFlow is defined. We can use partial function from the functools module:

    from functools import partial

    async def foo(endpoint, data):
        ...

    bar = partial(foo, endpoint = ...)

and in example above configure DataFlow using bar function instead of foo function. 

## More complex use cases

We can configure more complex DataFlow package. DataFlow is defined as a tuple which contains pipe of functions executed sequentially (one by one). We can add nested tuple inside which functions will be executed concurrently:

    import asyncio
    from functools import partial
    from asyncdataflow import DataFlow, args_mapper

    async def source(endpoint, query):
        ...
        return {'data': [1,2,3,4,5,6]}

    async def merge(data_a, data_b):
        data = zip(data_a, data_b)
        return {'data': data}

    async def destination(endpoint, data):
        ...
        return {'status': 0}

    source_a = args_mapper(partial(source, endpoint='endpoint_a'), output={'data': 'data_a'})  
    source_b = args_mapper(partial(source, endpoint='endpoint_b'), output={'data': 'data_b'})  
    dest = partial(destinatiom, endpoint='endpoint_c')

    async def main():
        dataflow_definition = ((source_a, source_b), merge, dest)
        dataflow = DataFlow(dataflow_definition)

        queries = [...]
        tasks = list()
        for query in queries:
            task = asyncio.create_task(dataflow(query=query))
            tasks.append(task)

        asyncio.gather(*tasks)

    asyncio.run(main())

In this example two source functions are executed concurrently, data returned from them are merged to one dictionary. Args_mapper is used to change returned value to different keys correspondig with arguments of next function merge. Partial function is used to pass endpoint parameter to source and destination functons.

DataFlow is defined by a tuple. The first tuple defines sequential execution, nested tuples define concurrent execution, but next nested tuples define again sequential execution, next concurrent, next sequential, and so on:

    (sequentional: 
        (concurrent: 
            (sequentional: A, B), 
            (sequentional: C, D)
        ), 
        (concurrent: 
            (sequentional: E, F), 
            (sequentional: G, H)
        )
    )

For example:

    (sequentional: 
        check_cache,
        dispatch_request,
        (concurrent: 
            (sequentional: 
                get_data_from_a,
                transform_data_from_a
            ), 
            (sequentional: 
                get_data_from_b,
                transform_data_from_b
            )
        ), 
        prepare_response,
        save_to_cache
    )

## Error handling

DataFlow exception hierarchy:

    +-- DataFlowException:
         +-- DataFlowError:
              +-- DataFlowDefinitionError:
                   +-- DataFlowFunctionArgsError
                   +-- DataFlowNotCallableError
                   +-- DataFlowEmptyError
              +-- DataFlowRuntimeError:
                   +-- DataFlowMergeResultError  
         +-- ArgsMapperError:
              +-- ArgsMapperInputKeyError
              +-- ArgsMapperOutputKeyError
              +-- ArgsMapperArgsError

- DataFlowFunctionArgsError: raised when function used in DataFlow has another arguments that POSITIONAL_OR_KEYWORD arguments
- DataFlowNotCallableError: raised when DataFlow contain not callable objects
- DataFlowEmptyError: Raised when DataFlow or sub-DataFlow is empty - tuple or nested tuple defined DataFlow is empty
- DataFlowMergeResultError: raised when returned dictionary from function shoudn't be merged with returned dictionary by other functions
- ArgsMapperInputKeyError: Raised when mapping defined in input argument do not correspond to initial function arguments
- ArgsMapperOutputKeyError: Raised when mapping defined in output argument do not correspond to returned from function dictionary
- ArgsMapperArgsError: Raised when passed arguments to functions do not fit to origin arguments

### Examples for error handling from DataFlow definition:



### Examples for error handling from DataFlow runtime:



### Examples for error handling from args_mapper functions:

    from asyncdataflow import args_mapper
    from asyncdataflow.exceptions import ArgsMapperInputKeyError, ArgsMapperOutputKeyError, ArgsMapperArgsError

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

