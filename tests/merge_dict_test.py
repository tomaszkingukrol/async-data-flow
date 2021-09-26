import pytest
from asyncdataflow.executor import _merge_kwargs
from asyncdataflow.exceptions import DataFlowMergeResultError


CORRECT_MERGE_2_DICT = [
    ({'a': 1}, {'b': 1}, {'a': 1, 'b': 1}),
    ({'a': 1}, {'a': 1}, {'a': 1}),
    ({}, {'a': 1}, {'a': 1}),
]

@pytest.mark.parametrize("dictA, dictB, result", CORRECT_MERGE_2_DICT)
def test_correct_merge_2_dict(dictA, dictB, result):
    assert _merge_kwargs(dictA, dictB) == result


CORRECT_MERGE_3_DICT = [
    ({'a': 1}, {'b': 1}, {'c': 1}, {'a': 1, 'b': 1, 'c': 1}),
    ({'a': 1}, {'b': 1}, {'b': 1}, {'a': 1, 'b': 1}),
    ({}, {}, {'a': 1}, {'a': 1}),
]

@pytest.mark.parametrize("dictA, dictB, dictC, result", CORRECT_MERGE_3_DICT)
def test_correct_merge_3_dict(dictA, dictB, dictC, result):
    assert _merge_kwargs(dictA, dictB, dictC) == result

# EMPTY_DATAFLOW = [
#     tuple(),
#     (foo, tuple()),
#     (tuple(), tuple())   
# ]

# @pytest.mark.parametrize("dataflow", EMPTY_DATAFLOW)
# def test_dataflow_from_empty(dataflow):
#     with pytest.raises(DataFlowEmptyError):
#         df = DataFlow(dataflow)