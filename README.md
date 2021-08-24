# async-data-flow
Asynchronous data flow processing, support both async coroutines and sync functions called as separated threads

## Introduction
As an example, common data flow process is devided to three components:
- Data Flow Source - get data from one or more sources
- Data Flow Transformation - e.g: merge data from multiple sources, transform data, split data to multiple destinations
- Data Flow Destination - write data to one or more destinations

You can configure this by defining tuples:

    data_flow_source = source_1, source_2, source_3
    data_flow_transform = data_transformation_function,
    data_flow_destination = destination_1, destination_2

    data_flow_definition = (data_flow_source,) + data_flow_transform + (data_flow_destination,)

- data_flow_source is a tuple defining concurrent Data Flow Source components, commonly resposible for data reading operations
- data_flow_transform is a tuple defining sequence Data Flow Transform components (data transformation commonly do not need I/O operations)
- data_flow_destination is a tuple defining concurrent Data Flow Destination components, commonly resposible for data writing operations

Each element of tuble must be Callable object, asynchronous or synchronous. Synchronous objects are callable in separated threads. 
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
        return {'sourceA': [1,2,3,4,5,6]}

    def sourceB(endpointB):
        time.sleep(0.500)
        return {'sourceA': [1,2,3,4,5,6]}       

    async def data_merge(sourceA: tuple, sourceB: tuple):
        return {'data': zip(sourceA, sourceB)}

    async def destination(data):
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


## extended usage
source, target | compare | s3_logger, notify
((source, target), compare, (s3_logger, notify))

[{source, target}, compose, {s3_logger, notify}]

get | transform | put
(get, transform, put)

discovery | save, log
(discovery, (save, log))


dataflow = source, target | compare | s3_logger, notify

dataflowsources -> dataflowtask -> dataflowdestinations


one source -> split -> many outputs

many source -> merge -> one output


source | split | out1, out2

sources = source
task = split
outputs = set(out1, out2)

(source, split, (out1, out2))


sources = set(src1, src2)
task = merge
outputs = out

((src1, src2), merge, out)

