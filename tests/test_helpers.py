import pytest
from sqlexpress import helpers as hp


@pytest.mark.parametrize('input_str,answer', [
    ('-- test', ''),              # standard comment line
    ('  # test', ''),             # with spaces in front
    ('--test \n  --test', ''),    # multiple comment line
    ('hello -- test', 'hello'),   # comment starts middle of line
    ('hello   # test', 'hello'),  # comment starts middle of line
])
def test_remove_comments(input_str: str, answer: str) -> None:
    output = hp.remove_comments(input_str)
    assert output == answer


@pytest.mark.parametrize('input_str,answer', [
    ('c1, c2', 2),                    # no brackets
    ('c1, func1(c2,1)', 2),           # single bracket
    ('c1, func1(func2(c2,1),2)', 2),  # double brackets
])
def test_split_with_brackets(input_str: str, answer: int) -> None:
    output = hp.split_with_brackets(input_str)
    assert len(output) == answer