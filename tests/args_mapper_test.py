import pytest
from asyncdataflow import amapper
from asyncdataflow.exceptions import ArgsMapperError


def foo(a, b): return a + b
def bar(a, b): return a, b
def baz(a, b): return {'a': a, 'b': b}


CORRECT_INPUT_MAPPING= [
    (foo, {'c': 1, 'd': 1}, {'a': 'c', 'b': 'd'}),
    (foo, {'c': 1, 'b': 1}, {'a': 'c'}),
    (foo, {'a': 1, 'd': 1}, {'b': 'd'}),
]

@pytest.mark.parametrize("func, input, input_map", CORRECT_INPUT_MAPPING)
def test_correct_input_mapping(func, input, input_map):
    f = amapper(func=func, input=input_map)
    try:
        f(**input)
    except:
        assert False
    else:
        assert True


INCORRECT_INPUT_MAPPING= [
    (foo, {'c': 1, 'b': 1}, {'a': 'd'}),
    (foo, {'a': 1, 'd': 1}, {'b': 'e'}),
    (foo, {'a': 1, 'd': 1}, {'e': 'c'}),
]

@pytest.mark.parametrize("func, input, input_map", INCORRECT_INPUT_MAPPING)
def test_incorrect_input_mapping(func, input, input_map):
    f = amapper(func=func, input=input_map)
    with pytest.raises(ArgsMapperError):
        f(**input)


CORRECT_OUTPUT_MAPPING= [
    (foo, {'a': 1, 'b': 2}, {'res': 3}, 'res'),
    (bar, {'a': 1, 'b': 2}, {'a': 1, 'b': 2}, ('a', 'b')),
    (baz, {'a': 1, 'b': 2}, {'c': 1, 'd': 2}, {'c': 'a', 'd': 'b'}),
]

CORRECT_PARTIAL_OUTPUT_MAPPING= [
    (bar, {'a': 1, 'b': 2}, {'a': 1}, ('a',)),
    (bar, {'a': 1, 'b': 2}, {'b': 1}, ('b',)),
    (baz, {'a': 1, 'b': 2}, {'c': 1}, {'c': 'a'}),
    (baz, {'a': 1, 'b': 2}, {'d': 2}, {'d': 'b'}),
]

CORRECT_ZERO_OUTPUT_MAPPING= [
    (bar, {'a': 1, 'b': 2}, (1,2), tuple()),
    (baz, {'a': 1, 'b': 2}, {'a': 1, 'b': 2}, {}),
    (bar, {'a': 1, 'b': 2}, {'_non_used': 1}, ('_non_used',)),
    (baz, {'a': 1, 'b': 2}, {'_non_used': 1}, {'_non_used': 'a'}),
]

@pytest.mark.parametrize("func, input, output, output_map", 
                         CORRECT_OUTPUT_MAPPING + 
                         CORRECT_PARTIAL_OUTPUT_MAPPING + 
                         CORRECT_ZERO_OUTPUT_MAPPING)
def test_correct_output_mapping(func, input, output, output_map):
    f = amapper(func=func, output=output_map)
    res = f(**input)
    assert res == output


INCORRECT_OUTPUT_MAPPING= [
    (baz, {'a': 1, 'b': 2}, {'c': 1, 'd': 2}, {'c': 'a', 'd': 'f'}),
    (baz, {'a': 1, 'b': 2}, {'c': 1, 'd': 2}, {'c': 'f', 'd': 'b'}),
]

@pytest.mark.parametrize("func, input, output, output_map", INCORRECT_OUTPUT_MAPPING)
def test_incorrect_output_mapping(func, input, output, output_map):
    f = amapper(func=func, output=output_map)
    with pytest.raises(ArgsMapperError):
        f(**input)


INCORRECT_ARGS_MAPPING= [
    (baz, {'a': 1, 'b': 2}, {'c': 1, 'd': 2}, {'c': 'a', 'd': 'f'}),
    (baz, {'a': 1, 'b': 2}, {'c': 1, 'd': 2}, {'c': 'f', 'd': 'b'}),
]

INCORRECT_ARGS_MAPPING= [
    (baz, {'d': 1, 'b': 1}, {'c': 'd'}),
    (baz, {'a': 1, 'd': 1}, {'e': 'd'})
]

@pytest.mark.parametrize("func, input, input_map", INCORRECT_ARGS_MAPPING)
def test_incorrect_args_mapping(func, input, input_map):
    f = amapper(func=func, input=input_map)
    with pytest.raises(ArgsMapperError):
        f(**input)
