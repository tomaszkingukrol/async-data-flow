import pytest
from asyncdataflow import DataFlow


def foo():
    pass

async def bar():
    pass


CORRECT_FUNCTION = [
    (foo,),
    (bar,),
]

@pytest.mark.asyncio
@pytest.mark.parametrize("dataflow", CORRECT_FUNCTION)
async def test_correct_function(dataflow):
    try:
        df = DataFlow(dataflow)
        await df()
    except:
        assert False
    else:
        assert True
