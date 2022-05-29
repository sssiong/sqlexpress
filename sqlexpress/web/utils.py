import json
import os
from typing import Tuple

from sqlexpress.parsers import YamlParser


def extract_project(filepath: str) -> dict:
    filename = os.path.basename(filepath)
    yaml = YamlParser(filepath=filepath)
    try:
        output = json.load(open(yaml.params.output, 'r'))
    except:
        output = None
    project = {
        'name': os.path.splitext(filename)[0],
        'filepath': filepath,
        'filename': filename,
        'input': yaml.raw,
        'output': output,
    }
    return project


def extract_nodes_edges_from_output(output: dict, query: str = None) -> Tuple[list, list]:

    edges = []
    for job in output['jobs']:
        edges += [[src, job['target']] for src in job['sources']]

    if query is not None and query != '':
        edges = [e for e in edges if query in e[0] or query in e[1]]

    nodes = []
    for edge in edges:
        nodes += edge
    nodes = list(sorted(set(nodes)))

    return nodes, edges