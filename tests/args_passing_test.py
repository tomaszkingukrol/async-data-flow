import pytest
from src.asyncdataflow import DataFlow
from src.asyncdataflow.exceptions import DataFlowMergeResultError


async def foo(a): return {'a': a}
async def bar(a): return {'a': a*2}
async def fuu(a): return {'b': a}
async def baz(a, b): return {'c': a+b}


CORRECT_CONFIG= [
    ((foo, bar), 'None', {'a': 1}, {'a': 2}),
    ((fuu, baz), 'Initial', {'a': 1}, {'a': 1, 'c': 2}),
    ((fuu, baz), 'All', {'a': 1}, {'a': 1, 'b': 1, 'c': 2}),
]

@pytest.mark.asyncio
@pytest.mark.parametrize("dataflow, args_visibility, input, output", CORRECT_CONFIG)
async def test_correct_args_visibily_none(dataflow, args_visibility, input, output):
    df = DataFlow(dataflow, args_visibility=args_visibility)
    result = await df(**input)
    assert result == output


INCORRECT_CONFIG= [
    ((foo, bar), 'Initial', {'a': 1}, {'a': 2}),
    ((foo, bar), 'All', {'a': 1}, {'a': 2}),
]

@pytest.mark.asyncio
@pytest.mark.parametrize("dataflow, args_visibility, input, output", INCORRECT_CONFIG)
async def test_incorrect_args_visibily_none(dataflow, args_visibility, input, output):
    df = DataFlow(dataflow, args_visibility=args_visibility)
    with pytest.raises(DataFlowMergeResultError):
        await df(**input)
