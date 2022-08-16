import pytest

from sqlexpress.parsers import QueryParser
from sqlexpress.exceptions import InvalidStructure

from . import TEST_DATA_DIR, TEST_FILES, ANSWERS


@pytest.mark.parametrize('file', TEST_FILES)
def test_query_parser_clauses(file: str):
    query = open(TEST_DATA_DIR / file, "r").read()
    parser = QueryParser(query)
    clauses = [c.__class__.__name__ for c in parser.clauses]
    assert clauses == ANSWERS[file]["clauses"]


@pytest.mark.parametrize('file', TEST_FILES)
def test_query_parser_basics(file: str):
    query = open(TEST_DATA_DIR / file, "r").read()
    parser = QueryParser(query)
    clauses = [b.__class__.__name__ for b in parser.basics]
    assert clauses == ANSWERS[file]["basics"]


@pytest.mark.parametrize('file', TEST_FILES)
def test_query_parser_sources(file: str):
    query = open(TEST_DATA_DIR / file, "r").read()
    parser = QueryParser(query)
    assert parser.extract_sources() == ANSWERS[file]["sources"]


@pytest.mark.parametrize('file', ['invalid1.sql'])
def test_query_parser_invalid_structure(file: str):
    with pytest.raises(InvalidStructure):
        query = open(TEST_DATA_DIR / file, 'r').read()
        _ = QueryParser(query)
