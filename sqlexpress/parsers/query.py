import copy
import re
from dataclasses import dataclass, field
from typing import List

import networkx as nx

from .. import helpers as hp
from ..structures import clauses as cl, basics as bs

CLAUSE_LIST = [
    cl.SelectClause(),
    cl.FromClause(),
    cl.WhereClause(),
    cl.LeftJoinClause(),
    cl.RightJoinClause(),
    cl.FullJoinClause(),
    cl.InnerJoinClause(),
    cl.JoinClause(),
    cl.OnClause(),
    cl.GroupByClause(),
    cl.OrderByClause(),
    cl.HavingClause(),
    cl.UnionClause(),
    cl.CreateTempFuncClause(),
    cl.WithClause(),
    cl.CteStartClause(),
    cl.CteEndClause(),
    cl.SubqueryStartClause(),
    cl.SubqueryEndClause(),
]


@dataclass
class QueryParser:
    raw: str
    target: str = None

    processed: str = field(init=False)
    clauses: List[cl.Clause] = field(init=False)
    basics: List[bs.BasicQuery] = field(init=False)
    G_table: nx.DiGraph = field(init=False)

    def __post_init__(self) -> None:
        self.preprocess()
        self.parse_clauses()
        self.parse_basics()
        self.parse_table_graph()

    def preprocess(self) -> None:
        processed = self.raw
        processed = hp.remove_comments(processed)
        replace = [
            (r'\(', ' ( '),  # add blanks before & after open bracket
            (r'\)', ' ) '),  # add blanks before & after close bracket
            (r'\,', ' , '),  # add blanks before & after comma
            (r'\n', ' '),  # remove next line
            (r' +', ' '),  # remove multiple blanks
        ]
        for frm, to in replace:
            processed = re.sub(frm, to, processed)
        self.processed = processed

    def parse_clauses(self) -> None:
        self.clauses: List[cl.Clause] = []
        tokens: List[str] = self.processed.split(' ')
        n_tokens: int = len(tokens)

        # loop through tokens
        for i, token in enumerate(tokens):

            # to speed up for loop in next step
            shortlisted_clauses = [
                c for c in CLAUSE_LIST
                if c.match_first_pattern(token)
            ]

            # confirm if start of new clause
            for cls in shortlisted_clauses:

                # check if clause's patterns & pre_patterns match tokens
                is_pattern_match = False
                upper_idx = i+cls.n_patterns
                lower_idx = i-cls.n_pre_patterns
                if upper_idx <= n_tokens and lower_idx >= 0:
                    is_pattern_match = cls.match_patterns(
                        tokens=tokens[i: upper_idx],
                        pre_tokens=tokens[lower_idx: i],
                    )

                # check if previous clause is expecting token
                is_pending_token = False if len(self.clauses) == 0 \
                    else self.clauses[-1].pending_token()

                # if patterns match & not expecting token, add new clause
                if is_pattern_match and not is_pending_token:
                    self.clauses.append(copy.deepcopy(cls))
                    break

            # add current token to most recent clause
            self.clauses[-1].add_token(token)

    def parse_basics(self) -> None:
        self.basics: List[bs.BasicQuery] = []

        # loop through clauses
        for i, clause in enumerate(self.clauses):
            is_pending = False if len(self.basics) == 0 \
                else self.basics[-1].pending_clause()

            # start of new clause
            if isinstance(clause, cl.CteStartClause):
                self.basics.append(bs.CteBasicQuery())
            if isinstance(clause, cl.SelectClause) and not is_pending:
                self.basics.append(bs.BasicQuery())

            # add clause to last basic query
            if len(self.basics) > 0:
                self.basics[-1].add_clause(clause)

        assert isinstance(self.basics[-1], bs.BasicQuery)
        self.basics[-1].target = self.target

    def parse_table_graph(self) -> None:
        rships = [r for b in self.basics for r in b.extract_table_to_table()]
        names = [(r.source.name, r.target.name) for r in rships]
        self.G_table = nx.DiGraph()
        self.G_table.add_edges_from(names)

    def extract_sources(self) -> List[str]:
        nodes = self.G_table.nodes
        return [n for n in nodes if self.G_table.in_degree(n) == 0]

    def print(self) -> None:
        hp.print_basics(self.basics)
