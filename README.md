# async-data-flow
Bundle coroutines into packege which can be executed like single coroutine. Inside package coroutines can be executed sequentially or concurent. Is useful to asynchronous data flow processing. Module depends on asyncio and can co-operate with many async libraries as aiohttp, aiomysql and others. If some process cannot be implemented asynchronously module support execution synchronous functions as separated threads. 

## Introduction
Simple data flow process could be composed from two elements: get data and write data. Both can be implemented as async functions but must be executed sequencally:

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

        await dataflow(endpoint=endpoint)

    asyncio.run(main())

In this example we call single package grabbing data from source and put them to destination. Of courde we can execute many of this packages using asyncio.create_task() function.

### passing arguments and retrieving results in DataFlow

DataFlow class is Callable. When we create them we define elemets of DataFlow as a tuple containing functions:

    (source, destination)

We pass initial arguments to Data Flow when we call DataFlow class object. We must use only keyword arguments:

    dataflow(endpoint=endpoint) 
    
Initial arguments are passed to first element in DataFlow. All functions used in DataFlow must use only POSITIONAL_OR_KEYWORD arguments. Returned values from functions must be a dictionary which is unpacked as keyword arguments passing to next element in DataFlow. Next element check if can pass all arguments to own function, if can execute this function, if not pass arguments to next element. This process continues until the end of DataFlow package. Package return dictionary from last executed function.

### args_mapper

We can use in Data Flow functions returned other values that dictionary. We can transform passed argumets and returned values using args_mapper:

    from asyncdataflow import args_mapper

    async def foo(a):
        ...
        return data

    bar = args_mapper(foo, input={'a': 'endpoint'}, output='data')  

    bar(endpoint=...) -> {'data': data}

In python function can return multile outputs as tuple:

    async def foo(a):
        ...
        return source, data

    bar = args_mapper(foo, input={'a': 'endpoint'}, output=['source', 'data'])  

    bar(endpoint=...) -> {'source': source, 'data': data}

Sometimes we should map returned dictionary to another:

    async def foo(a):
        ...
        return {'source': source, 'data': data}

    bar = args_mapper(foo, input={'a': 'endpoint'}, output={'source': 'source_a', 'data': 'data_a'})  

    bar(endpoint=...) -> {'source'_a: source, 'data_a': data}

### passing extra parameters

If we need to pass extra parameters to function in Data Flow we can use partial function from functools module:

    from functools import partial

    async def foo(creds, data):
        ...

    bar = partial(foo, creds = ...)

this is useful to pass e.g. credentials to function responsible for saving data in destination

### geting output from package

The package ending by executing last function/functions. Returned value/values from this function/functions are returned by package.

    task = dataflow(endpoint=endpoint)
    result = await task

### infinity_loop

Process defined in DataFlow could be repeated in infinity loop.

    dataflow = DataFlow(dataflow_definition, infinity_loop=True)

This can be usefull e.g. for continous synchronization process.

## More complex use cases

We can configure more complex data flow package. Data flow is defined as tuple which contain pipe of functions executed sequencionally (one by one). We can add nested tuple inside which function will be executed concurrently

    import asyncio
    from functools import partial
    from asyncdataflow import DataFlow

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

        for query in (query_1, query_2, query_3):
            params = {'query': query}
            asyncio.create_task(dataflow(query=query))

    asyncio.run(main())

In this example two source functions are executed concurrently, data returned of them are merged to one dictionary (that must be renamed by args_mapper function) and passed to merge function. We use partial function from functools module to pass endpoint parameter to source and destination functons.

Data Flow is a tuple. First tuple define sequentional execution, nested tuples defines concurent execution, but next nested tuple define again sequentional execution, next concurrent, mext sequentional, and so on:

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

For example if we want build request broker we can define package:

    (sequentional: 
        receive_request,
        dispatch_request,
        (concurrent: 
            (sequentional: 
                ask_system_a,
                transform_data_a
            ), 
            (sequentional: 
                ask_system_b,
                transform_data_b
            )
        ), 
        compose_response
    )

where:
- first function receive_request() is responsible for getting request
- second function dispatch_request() is resposible for dispatching requests to concurrent sub-processes asking third system. In concurrent processing at least one function or sub-task must get arguments and be executed (function which do not get argument are not executed) so dispatch_request() should prepare arguments for only this functions which want to be executed
- ask_system_x and transform_data_x functions getting responses from third systems
- last compose_response return respons for received request

