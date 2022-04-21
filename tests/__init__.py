import json
from pathlib import Path

TEST_DIR = Path(__file__).absolute().parents[0]
TEST_DATA_DIR = TEST_DIR / "data"

TEST_FILES = [
    'example1.sql',
    'example2.sql',
    'example3.sql',
    'example4.sql',
]

ANSWERS = json.loads(open(TEST_DATA_DIR / "answers.json", 'r').read())