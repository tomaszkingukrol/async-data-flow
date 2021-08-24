# async-data-flow
Asynchronous data flow processing, support bot async coroutines and sync functions called as separated threads

## Introduction
As an example, common data flow process is devided to three components:
> Data Flow Source - get data from sources

> Data Flow Transform - e.g: merge data from multiple sources, transform data, split data to multiple destinations

> Data Flow Destination - write data to destinations

To configure this you can defien tuples:

    from asyncdataflow import DataFlow
    
    data_flow_source = (source_1, source_2, source_3)
    data_flow_transform = data_transformation_function
    data_flow_destination = (destination_1, destination_2)

    data_flow_definition = (data_flow_source, data_flow_transform, data_flow_destination)

data_flow_transform is not a tuple and represent more common situation where data transformation can be processed 
in single synchronous function (do not need I/O operation specyfic to asyncio processing)

To execute DataFlow and pass initial parameters:

    dataflow = DataFlow(data_flow_definition)
    params = {'param_1': ..., 'param_2': ...}
    result = dataflow(params)



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

