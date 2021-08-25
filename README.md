# async-data-flow
Bundle coroutines into packege which can be executed like single coroutine. Inside package coroutines can be executed sequentially or concurent. Is useful to asynchronous data flow processing. Module depends on asyncio and can co-operate with many async libraries as aiohttp, aiomysql and others. If some process cannot be implemented asynchronously module support execution synchronous functions as separated threads. 

## Introduction
Simple data flow process could be composed from two elements: get data and write data. Both can be implemented as async functions but must be executed sequencally. Lets see simple example:

    import asyncio
    import time
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
            params = {'endpoint': endpoint}
            asyncio.create_task(dataflow(params))

    asyncio.run(main())

Initial parameters are passed to first function in data flow. In this example three concurent package are running. This can be usefull for getting data from multiple sources and store them in one db. 

## args_mapper

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

    bar = args_mapper(foo, input={'a': 'endpoint'}, output={'source': 'sourceA', 'data': 'dataA'})  

## passing extra parameters

If we need to pass extra parameter to next function in Data Flow we can use partial function:

    from functools import partial

    async def foo(creds, data):
        ...

    bar = partial(foo, creds = ...)

## infinity_loop

Process defined in DataFlow could be repeated in infinity loop.

    dataflow = DataFlow(dataflow_definition, infinity_loop=True)

This can be usefull e.g. for continous synchronization process

# More complex use cases





As an example, common data flow process is devided to three components:
- Data Flow Source - get data from one or more sources
- Data Flow Transformation - e.g: transform data, merge data from multiple sources, split data to multiple destinations
- Data Flow Destination - write data to one or more destinations

You can configure this by defining tuples:

    data_flow_source = source_1, source_2, source_3
    data_flow_transform = data_transformation_function,
    data_flow_destination = destination_1, destination_2

    data_flow_definition = (data_flow_source,) + data_flow_transform + (data_flow_destination,)

- data_flow_source is a tuple defining concurrent Data Flow Source components, commonly resposible for data reading operations
- data_flow_transform is a tuple defining sequence Data Flow Transformation components (data transformation commonly do not need I/O operations)
- data_flow_destination is a tuple defining concurrent Data Flow Destination components, commonly resposible for data writing operations

Each element of tuple must be Callable object, asynchronous or synchronous. Synchronous objects are callable in separated threads. 
To execute DataFlow and pass initial parameters:

    from asyncdataflow import DataFlow
    
    dataflow = DataFlow(data_flow_definition)
    params = {'param_1': ..., 'param_2': ...}
    result = await dataflow(params)

If you do not want to run data_transformation_function as separated thred define them as coroutine function (async).   

## Example

    import asyncio
    import time
    from asyncdataflow import DataFlow

    async def sourceA(endpointA):
        await asyncio.sleep(0.500)
        return {'sourceA': endpointA, 'dataA': [1,2,3,4,5,6]}

    def sourceB(endpointB):
        time.sleep(0.500)
        return {'sourceB': endpointA, 'dataB': [1,2,3,4,5,6]}     

    async def data_merge(sourceA: str, dataA: list, sourceB: str, dataB: list):
        return {'source': f'zip({sourceA},{sourceB})', 'data': zip(dataA, dataB)}

    async def destination(source, data):
        await asyncio.sleep(0.500)
        return {'status': 0}

    async def main():

        data_flow_source = sourceA, sourceB
        data_flow_transform = data_merge,
        data_flow_destination = destination,

        data_flow_definition = (data_flow_source,) + data_flow_transform + (data_flow_destination,)

        dataflow = DataFlow(data_flow_definition)
        params = {'sourcaA': 'A', 'sourceB': 'B'}
        return await dataflow(params)

    asyncio.run(main())

You can also run many cuncurrent async Data Flows:

    ...

        dataflow = DataFlow(data_flow_definition)
        flows = list()
        for p1, p2 in (('A', 'B'),('C', 'D'),('E', 'F'),('G', 'H')):
            params = {'sourcaA': p1, 'sourceB': p2}
            flow = asyncio.create_task(dataflow(params))
            flows.append(flow)

        asyncio.gather(*flows)

Using Data Flow functions must return a dictionary suits to arguments of next executed functions (dictionary is unpacked to kwargs). Next functions do not must have all arguments returnet by previous function but all arguments of next functions must be covered by returned dictionary from previous function.

## args_mapper

We can use args_mapper to conver input and output from given function:

    from asyncdataflow import args_mapper

    async def source(endpoint):
        await asyncio.sleep(0.500)
        return {'source': endpointA, 'data': [1,2,3,4,5,6]}

    sourceA = args_mapper(source, input={'enpoint': 'endpointA'}, output={'source': 'sourceA', 'data': 'dataA'})

args_mapper can also convert returned tuple or single value to dictionary so you can write:

    from asyncdataflow import args_mapper

    async def source(endpoint):
        await asyncio.sleep(0.500)
        return endpoint, [1,2,3,4,5,6]

    sourceA = args_mapper(source, input={'enpoint': 'endpointA'}, output=['sourceA', 'dataA'])

## DataFlow

We can define DataFlow passing tuple:

    data_flow_source = sourceA, sourceB
    data_flow_transform = data_merge, data_split
    data_flow_destination = destinationA, destinationB,

    data_flow_definition = (data_flow_source,) + data_flow_transform + (data_flow_destination,)

We can also define this tuple directly:

    data_flow_definition = ((sourceA, sourceB), data_merge, data_split, (destinationA, destinationB))

In first tuple all elements are executed sequentialy:
- (sourceA, sourceB)
- data_merge
- data_split
- (destinationA, destinationB)

In nested tuples:
- (sourceA, sourceB)
- (destinationA, destinationB)

each elements are executed cuncurently.

We also configure more complex Data Flow. FIrst tuple define sequentional execution, nested tuples defines concurent execution, but next nested tuple define again sequentional execution, next concurrent, mext sequentional, and so on:

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

In this example we have:
- two concurrent processes resposible for getting data (A and C) and data transformation (B, D)
- getting data and data transformation works sequentionally
- also we have two concurrent processes which can be resposoble for completelly different bussines functionalities but works on the same set of input data
- each of them analize data (E and G) and save data in destinations (F and H)

## infinity_loop

Process defined in DataFlow could be repeated in infinity loop.

    dataflow = DataFlow(data_flow_definition, infinity_loop=True)

