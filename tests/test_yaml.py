import pytest

from sqlexpress.exceptions import YamlParsingFailed
from sqlexpress.parsers import YamlParser

from . import TEST_DATA_DIR


@pytest.mark.parametrize('file', ['bulk1.yaml', 'bulk2.yaml'])
def test_yaml_parser(file: str):
    _ = YamlParser(TEST_DATA_DIR / file)


@pytest.mark.parametrize('file', ['fail1.yaml'])
def test_yaml_parser_fail(file: str):
    with pytest.raises(YamlParsingFailed):
        _ = YamlParser(TEST_DATA_DIR / file)
