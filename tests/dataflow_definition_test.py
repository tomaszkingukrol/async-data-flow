import pytest

from asyncdataflow import DataFlow


def foo():
    pass


CORRECT_DATAFLOW = [
    (foo,),
    (foo, foo),
    (foo, (foo, foo)),
    ((foo, foo), (foo, foo))
]

@pytest.mark.parametrize("dataflow", CORRECT_DATAFLOW)
def test_dataflow_from_functions(dataflow):
    try:
        df = DataFlow(dataflow)
    except:
        assert False
    else:
        assert True


EMPTY_DATAFLOW = [
    tuple(),
    (foo, tuple()),
    (tuple(), tuple())   
]

@pytest.mark.parametrize("dataflow", EMPTY_DATAFLOW)
def test_dataflow_from_empty(dataflow):
    with pytest.raises(TypeError):
        df = DataFlow(dataflow)


DATAFLOW_NOT_FUNCTIONS = [
    (1),
    (foo, 1),
    (foo, (1, foo)),
    ((foo, 1), (1, foo))
]

@pytest.mark.parametrize("dataflow", DATAFLOW_NOT_FUNCTIONS)
def test_dataflow_from_not_functions(dataflow):
    with pytest.raises(TypeError):
        df = DataFlow(dataflow)


DATAFLOW_NOT_TUPLES = [
    list(),
    set().add,
    dict(),
    [foo],
    {foo},
    [foo, foo],
    {foo, foo},
    (foo, [foo, foo]),
    (foo, {foo, foo}),
    ([foo, foo], {foo, foo})
]

@pytest.mark.parametrize("dataflow", DATAFLOW_NOT_TUPLES)
def test_dataflow_from_not_tuples(dataflow):
    with pytest.raises(TypeError):
        df = DataFlow(dataflow)