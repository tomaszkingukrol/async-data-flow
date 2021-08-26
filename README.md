# async-data-flow
Bundle coroutines into packege which can be executed like single coroutine. Inside package coroutines can be executed sequentially or concurent. Is useful to asynchronous data flow processing. Module depends on asyncio and can co-operate with many async libraries as aiohttp, aiomysql and others. If some process cannot be implemented asynchronously module support execution synchronous functions as separated threads. 

## Introduction
Simple data flow process could be composed from two elements: get data and write data. Both can be implemented as async functions but must be executed sequencally. Lets see simple example:

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

        for endpoint in (endpoint1, endpoint2, endpoint3):
            asyncio.create_task(dataflow(endpoint=endpoint))

    asyncio.run(main())

Initial parameters are passed to first function in data flow. In this example three concurent package are running. This can be usefull for getting data from multiple sources and store them in one db. 

### args_mapper

In data flow returned paarmeters from first element must be passed to next. This is given by unpacking dictionary to kwargs. So functions used in data flow should return dictionary with keys coresponding to argument of next functions. If we have function and want to implement this we can use args.mapper:

    from asyncdataflow import args_mapper

    async def foo(a):
        ...
        return data

    bar = args_mapper(foo, input={'a': 'endpoint'}, output='data')  

In python function can return multile outputs as tuple:

    async def foo(a):
        ...
        return source, data

    bar = args_mapper(foo, input={'a': 'endpoint'}, output=['source', 'data'])  

Sometimes we should map returned dictionary to another:

    async def foo(a):
        ...
        return {'source': source, 'data': data}

    bar = args_mapper(foo, input={'a': 'endpoint'}, output={'source': 'source_a', 'data': 'data_a'})  

### passing extra parameters

If we need to pass extra parameter to next function in Data Flow we can use partial function from functools module:

    from functools import partial

    async def foo(creds, data):
        ...

    bar = partial(foo, creds = ...)

e.g. this can be credentials needed to access to destination.

### geting output from package


### infinity_loop

Process defined in DataFlow could be repeated in infinity loop.

    dataflow = DataFlow(dataflow_definition, infinity_loop=True)

This can be usefull e.g. for continous synchronization process.

## More complex use cases

We can configure more complex data flow package. Data flow is defined as tuple which contain pipe of function executed sequencionally (one by one). We can add nested tuple inside which function will be executed concurrently

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

