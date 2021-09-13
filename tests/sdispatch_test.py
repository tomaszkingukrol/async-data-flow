import pytest
from asyncdataflow import DataFlow, sdispatch
from asyncdataflow.exceptions import DataFlowException

@sdispatch
def foo(_dispatch_key):
    pass

@foo.register('a')
async def _1(a):
    return {'a': a}

@foo.register('b')
async def _2(a):
    return {'a': a}


@pytest.mark.asyncio
async def test_correct_run_dispatched_coroutines():
    df = DataFlow((foo('a'),foo('b')))
    result = await df(a=1)
    assert result == {'a': 1}


