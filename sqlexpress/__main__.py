import argparse
import logging
import os

from .parsers import QueryParser, YamlParser
from .helpers import print_basics

parser = argparse.ArgumentParser(description='Extract info from your SQLs')
parser.add_argument('command', help='command to execute', type=str, nargs=1)
parser.add_argument('-f', '--file', help='SQL/YAML file')
parser.add_argument('-l', '--loglevel', help='logging level', default='INFO')
args = parser.parse_args()

fmt = '%(asctime)s | %(levelname)s | %(module)s | %(funcName)s | %(message)s'
lvl = getattr(logging, args.loglevel.upper())
logging.basicConfig(format=fmt, level=lvl)


def get_parser(file: str, target: str = None) -> QueryParser:
    _, ext = os.path.splitext(file)
    assert ext == '.sql', 'Not SQL file'
    query = open(file, 'r').read()
    parser = QueryParser(query, target=target)
    return parser


def main():

    command = args.command[0]

    if command == 'bulk':
        _, ext = os.path.splitext(args.file)
        assert ext == '.yaml', 'Input file not yaml'
        bulk = YamlParser(args.file)
        bulk.parse_jobs()
        bulk.save_output()
        return

    if command == 'structure':
        parser = get_parser(args.file)
        print_basics(parser.basics)
        return

    if command == 'sources':
        parser = get_parser(args.file)
        for table in parser.extract_sources():
            print(table)
        return

    raise Exception(f'Unknown command: {command}')


if __name__ == '__main__':
    main()

