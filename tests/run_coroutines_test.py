import pytest
from asyncdataflow import DataFlow
from asyncdataflow.exceptions import DataFlowMergeResultError


async def foo(a): return {'a': a}
async def bar(a): return {'a': a}
async def bar2(a): return {'a': a*2}
async def baz(a): return {'b': a}
async def buz(a, b): return {'c': a+ b} 
async def fuu(c): return {'c': c}


CORRECT_CONFIG= [
    ((foo, bar), {'a': 1}, {'a': 1}),
    ((foo, (bar, baz)), {'a': 1}, {'a': 1, 'b': 1}),
    ((foo, (bar, baz), buz), {'a': 1}, {'c': 2}),
    ((foo, (bar, baz), buz, fuu), {'a': 1}, {'c': 2}),
    ((foo, fuu), {'a': 1}, {'a': 1}),
    ((foo, buz), {'a': 1}, {'a': 1}),
    ((foo, fuu, (bar, baz), buz, fuu), {'a': 1}, {'c': 2}),
]

@pytest.mark.asyncio
@pytest.mark.parametrize("dataflow, input, output", CORRECT_CONFIG)
async def test_correct_run_coroutines(dataflow, input, output):
    df = DataFlow(dataflow)
    result = await df(**input)
    assert result == output


INCORRECT_CONFIG= [
    ((foo, (bar, bar2)), {'a': 1}, {'a': 1}),
]

@pytest.mark.asyncio
@pytest.mark.parametrize("dataflow, input, output", INCORRECT_CONFIG)
async def test_incorrect_run_coroutines(dataflow, input, output):
    df = DataFlow(dataflow)
    with pytest.raises(DataFlowMergeResultError):
        await df(**input)
