import json
import logging
import os
from dataclasses import dataclass, field
from typing import List

import yaml

from . import QueryParser


@dataclass
class Params:
    output: str
    folder: str = None
    env: dict = None

    def to_dict(self) -> dict:
        output = {'output': self.output}
        if self.folder:
            output['folder'] = self.folder
        if self.env:
            output['env'] = self.env
        return output


@dataclass
class Job:
    target: str
    sql: str
    env: dict = None
    parser: QueryParser = None

    def parse(self, folder: str, env: dict = None) -> None:
        fullpath = os.path.join(folder, self.sql) if folder else self.sql
        _, ext = os.path.splitext(fullpath)
        assert ext == '.sql', f'Not a SQL file: {self.sql}'
        query = open(fullpath, 'r').read()
        combined_env = {**self.env, **env} if self.env and env \
            else self.env or env
        self.parser = QueryParser(query, env=combined_env)

    def to_dict(self) -> dict:
        output = {'target': self.target, 'sql': self.sql}
        if self.env:
            output['env'] = self.env
        if self.parser:
            output['sources'] = self.parser.extract_sources()
        return output


@dataclass
class YamlParser:
    filepath: str
    raw: dict = field(init=False)
    params: Params = field(init=False)
    jobs: List[Job] = field(init=False)

    def __post_init__(self) -> None:
        parsed = yaml.safe_load(open(self.filepath, 'r').read())
        assert 'parameters' in parsed.keys(), 'Missing parameters'
        assert 'jobs' in parsed.keys(), 'Missing jobs'
        self.raw = parsed
        self.params = Params(**parsed['parameters'])
        self.jobs = [Job(**j) for j in parsed['jobs']]

    def parse_jobs(self) -> None:
        parsed_jobs = []
        for job in self.jobs:
            logging.debug(job.to_dict())
            job.parse(folder=self.params.folder, env=self.params.env)
            parsed_jobs.append(job)
        self.jobs = parsed_jobs

    def save_output(self) -> None:
        output = {
            'parameters': self.params.to_dict(),
            'jobs': [j.to_dict() for j in self.jobs]
        }
        _, ext = os.path.splitext(self.params.output)
        assert ext == '.json', f'Not a JSON file: {self.params.output}'
        with open(self.params.output, 'w') as f:
            json.dump(output, f, sort_keys=False)
