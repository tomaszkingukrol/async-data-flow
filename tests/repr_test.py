import pytest
from src.asyncdataflow import DataFlow


async def foo(): pass
async def bar(): pass


CORRECT_FUNCTION = [
    ((foo,),'DataFlow((foo,))'),
    ((foo,bar),'DataFlow((foo,bar))'),
    ((foo,(foo,bar)),'DataFlow((foo,(foo,bar)))'),
]


CORRECT_MERGE_2_DICT = [
    (None, {'a': 1}, {'b': 1}, {'a': 1, 'b': 1}),
    (None, {'a': 1}, {'a': 1}, {'a': 1}),
    (None, {}, {'a': 1}, {'a': 1}),
]


@pytest.mark.parametrize("dataflow, repr", CORRECT_FUNCTION)
def test_correct_function(dataflow, repr):
    df = DataFlow(dataflow)
    assert df.__repr__() == repr

