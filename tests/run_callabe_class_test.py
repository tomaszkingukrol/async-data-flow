import pytest
from src.asyncdataflow import DataFlow

class Foo:
    async def __call__(sefl, a):
        return {'a': a}

class Bar:
    async def __call__(self, a):
        return {'a': a}


CORRECT_CONFIG= [
    ((Foo(), Bar()), {'a': 1}, {'a': 1}),
]

@pytest.mark.asyncio
@pytest.mark.parametrize("dataflow, input, output", CORRECT_CONFIG)
async def test_correct_run_coroutines(dataflow, input, output):
    df = DataFlow(dataflow)
    result = await df(**input)
    assert result == output


