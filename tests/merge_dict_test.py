import pytest
from asyncdataflow.executor import _merge_kwargs
from asyncdataflow.exceptions import DataFlowMergeResultError


CORRECT_MERGE_2_DICT = [
    (None, {'a': 1}, {'b': 1}, {'a': 1, 'b': 1}),
    (None, {'a': 1}, {'a': 1}, {'a': 1}),
    (None, {}, {'a': 1}, {'a': 1}),
]

@pytest.mark.parametrize("task, dictA, dictB, result", CORRECT_MERGE_2_DICT)
def test_correct_merge_2_dict(task, dictA, dictB, result):
    assert _merge_kwargs(task, dictA, dictB) == result


CORRECT_MERGE_3_DICT = [
    (None, {'a': 1}, {'b': 1}, {'c': 1}, {'a': 1, 'b': 1, 'c': 1}),
    (None, {'a': 1}, {'b': 1}, {'b': 1}, {'a': 1, 'b': 1}),
    (None, {}, {}, {'a': 1}, {'a': 1}),
]

@pytest.mark.parametrize("task, dictA, dictB, dictC, result", CORRECT_MERGE_3_DICT)
def test_correct_merge_3_dict(task, dictA, dictB, dictC, result):
    assert _merge_kwargs(task, dictA, dictB, dictC) == result

