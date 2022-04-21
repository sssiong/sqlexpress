import uuid
from typing import List, Optional

from . import clauses as cl
from ..graph import entities as en, relationships as rs


class BasicQuery:

    def __init__(self) -> None:
        self.clauses: List[cl.Clause] = []
        self._target: Optional[str] = None

    @property
    def target(self) -> Optional[str]:
        return self._target or uuid.uuid4().hex[:5]

    @target.setter
    def target(self, target: str) -> None:
        self._target = target

    def add_clause(self, clause: cl.Clause) -> None:
        self.clauses.append(clause)

    def pending_clause(self) -> bool:
        cls = self.clauses
        no_select = not any([isinstance(c, cl.SelectClause) for c in cls])
        no_from = not any([isinstance(c, cl.FromClause) for c in cls])
        n_sub_start = sum([isinstance(c, cl.SubqueryStartClause) for c in cls])
        n_sub_end = sum([isinstance(c, cl.SubqueryEndClause) for c in cls])
        last_union = isinstance(cls[-1], cl.UnionClause)
        return no_select or no_from \
               or (n_sub_start > n_sub_end) \
               or last_union

    def extract_table_to_table(self) -> List[rs.TableToTable]:
        target = en.Table(name=self.target)
        output = []
        for clause in self.clauses:
            for source in clause.extract_tables():
                rship = rs.TableToTable(source=source, target=target)
                output.append(rship)
        return output


class CteBasicQuery(BasicQuery):

    @property
    def target(self) -> Optional[str]:
        if len(self.clauses) == 0:
            return None
        assert isinstance(self.clauses[0], cl.CteStartClause)
        return self.clauses[0].extract_target()

    def pending_clause(self) -> bool:
        has_start = any([type(c) == cl.CteStartClause for c in self.clauses])
        has_end = any([type(c) == cl.CteEndClause for c in self.clauses])
        return has_start and not has_end

    def extract_table_to_table(self) -> List[rs.TableToTable]:
        assert isinstance(self.clauses[0], cl.CteStartClause)
        target = en.Table(name=self.target)
        output = []
        for clause in self.clauses[1:]:
            for source in clause.extract_tables():
                rship = rs.TableToTable(source=source, target=target)
                output.append(rship)
        return output

