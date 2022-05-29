import copy
import glob
import json
import os

import yaml
from flask import render_template, redirect, request, url_for

from sqlexpress.parsers import YamlParser
from sqlexpress.web import app
from sqlexpress.web.utils import (
    extract_project,
    extract_nodes_edges_from_output,
)


FOLDER = os.environ.get('WEBSERVER_FOLDER')

PROJECTS = {
    p['filename']: p for p in [
        extract_project(f) for f in sorted(glob.glob(f'{FOLDER}/*.yaml'))
    ]
}


@app.route('/')
def home():
    projects = []
    for filename, project in PROJECTS.items():
        tmp = {'name': project['name'], 'filename': filename}
        if project['output']:
            nodes, _ = extract_nodes_edges_from_output(project['output'])
            tmp['n_jobs'] = len(project['output']['jobs'])
            tmp['n_tables'] = len(nodes)
        projects.append(tmp)
    return render_template('home.html', projects=projects)


@app.route('/project/<string:filename>/extract/', methods=['POST'])
def project_extract(filename: str):
    filepath = PROJECTS[filename]['filepath']
    bulk = YamlParser(filepath)
    bulk.parse_jobs()
    bulk.save_output()
    PROJECTS[filename] = extract_project(filepath)
    return redirect(url_for('home'))


@app.route('/project/<string:filename>/input/', methods=['GET'])
def project_input(filename: str):
    p = copy.deepcopy(PROJECTS[filename])
    p['input'] = yaml.safe_dump(p['input'], sort_keys=False)
    p['input'] = p['input'].replace('\njobs', '\n\njobs')
    p['input'] = p['input'].replace('\n- ', '\n\n- ')
    return render_template(f'project_input.html', project=p)


@app.route('/project/<string:filename>/output/', methods=['GET'])
def project_output(filename: str):
    p = copy.deepcopy(PROJECTS[filename])
    p['output'] = json.dumps(p['output'], indent=4)
    return render_template(f'project_output.html', project=p)


@app.route('/project/<string:filename>/graph/', methods=['GET', 'POST'])
def project_graph(filename: str):
    p = copy.deepcopy(PROJECTS[filename])
    q = request.form.get('query', '')
    p['nodes'], p['edges'] = extract_nodes_edges_from_output(p['output'], q)
    return render_template(f'project_graph.html', project=p, query=q)


@app.route('/project/<string:filename>/tables/', methods=['GET', 'POST'])
def project_tables(filename: str):
    p = copy.deepcopy(PROJECTS[filename])
    p['nodes'], _ = extract_nodes_edges_from_output(p['output'])
    q = request.form.get('query', '')
    if q != '':
        p['nodes'] = [n for n in p['nodes'] if q in n]
    return render_template(f'project_tables.html', project=p, query=q)
