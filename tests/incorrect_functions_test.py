import pytest

from asyncdataflow import DataFlow
from asyncdataflow.exceptions import DataFlowFunctionArgsError


def foo(*args):
    pass


def bar(*args, **kwargs):
    pass


def baz(*, a, b):
    pass

INCORRECT_FUNCTION = [
    (foo,),
    (bar,),
    (baz,),
]

@pytest.mark.asyncio
@pytest.mark.parametrize("dataflow", INCORRECT_FUNCTION)
async def test_incorrect_function(dataflow):
    with pytest.raises(DataFlowFunctionArgsError):
        df = DataFlow(dataflow)



