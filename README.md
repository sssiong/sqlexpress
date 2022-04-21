# SQL Express

## Introduction

Too often we find ourselves with tons of SQLs to maintain and with query
outputs that do not make sense due to issues with upstream dependencies. 
Wouldn't it be nice if there is a package that helps us identify all 
upstream dependencies from our SQLs without the need to manually look
through them?

Given a SQL file, this package is designed to perform the following:

1. **Parse Query Structure**
   1. Identify the start of clauses / keywords
   2. Helps to organize the query for other functionalities
2. **Parse Source Tables**
   1. Identify source tables required
   2. Helps to identify required tables
3. *< more to come > ...*

Bulk processing of multiple SQLs is also possible. Create a yaml file 
and provide details of the SQL files + save location of parsed output
([example](tests/data/bulk.yaml)). The parsed output is saved as a json file 
([example](tests/data/bulk.json)).


## Getting Started

Using command line:

```bash
# print query structure
python3 -m sqlexpress structure -f tests/data/example1.sql

# print source tables
python3 -m sqlexpress sources -f tests/data/example1.sql

# bulk processing
python3 -m sqlexpress bulk -f tests/data/bulk.yaml
```

Using python:

```python
from sqlexpress.parsers import QueryParser

query = open('tests/data/example1.sql', 'r').read()
parser = QueryParser(query)

# print query structure
parser.print()

# get source tables
source_tables = parser.extract_sources()  # ['`project.dataset.raw1`', ...]
```


## Under The Hood

Want to identify the structure of the query first so that it is easier
to identify other things (e.g. source tables). This is done in 2 steps:

![parse_logic](docs/parse_logic.png)

With the parsed structure, we can construct a directed table graph (below) 
even with long, complicated queries. The source tables can be easily 
identified from the table graph (nodes with only outward arrows).

![table_graph](docs/table_graph.png)



