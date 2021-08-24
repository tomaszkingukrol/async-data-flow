# async-data-flow
asynchronous data flow processing, support bot async coroutines and sync function called as separated thread

## Introduction
As an example, common data flow process is devided to three components:
> Data Flow Source 
> Data Flow Transform
> Data Flow Destination




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

