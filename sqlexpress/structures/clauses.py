import re
from abc import ABC
from typing import Any, List, Optional

from ..graph import entities as en


class Clause(ABC):

    def __init__(
            self, patterns: List[Any],
            pre_patterns: List[Any] = None,
            require_min_tokens: Optional[int] = None,
            require_balanced_brackets: bool = True,
    ) -> None:

        self.patterns = patterns
        self.n_patterns = len(self.patterns)

        self.pre_patterns = pre_patterns or []
        self.n_pre_patterns = len(self.pre_patterns)

        self.require_min_tokens = require_min_tokens or len(self.patterns)
        self.require_balanced_brackets = require_balanced_brackets

        self.tokens = []

    @staticmethod
    def _match_pattern_token(pattern: Any, token: str) -> bool:
        """ Check if pattern & token match """
        p_type = type(pattern)
        if p_type == str and pattern.lower() == token.lower():
            return True
        if p_type == re.Pattern and pattern.match(token.lower()):
            return True
        return False

    def match_first_pattern(self, token: str) -> bool:
        """ Check if token match 1st pattern """
        return self._match_pattern_token(self.patterns[0], token)

    def match_patterns(
            self, tokens: List[str],
            pre_tokens: List[str] = None,
    ) -> bool:
        """ Check if tokens match all patterns """
        pre_tokens = pre_tokens or []

        # flag if token count mismatch
        assert self.n_patterns == len(tokens)
        assert self.n_pre_patterns == len(pre_tokens)

        # false if any tokens do not match
        patterns = self.pre_patterns + self.patterns
        tokens = pre_tokens + tokens
        matches = [
            self._match_pattern_token(p, t)
            for p, t in zip(patterns, tokens)
        ]
        return all(matches)

    def add_token(self, token: str) -> None:
        """ Add token to existing list of tokens """
        self.tokens.append(token)

    def pending_token(self) -> bool:
        """ Check if clause is expecting more tokens """

        if self.require_balanced_brackets:
            n_open = sum([t == '(' for t in self.tokens])
            n_close = sum([t == ')' for t in self.tokens])
            if n_open > n_close:
                return True

        if self.require_min_tokens:
            if len(self.tokens) < self.require_min_tokens:
                return True

        return False

    def extract_tables(self) -> List[en.Table]:
        """ Depending on clause, may need to extract tables """
        return []

    def extract_target(self) -> Optional[str]:
        """ Only has non-None output for CteStartClause """
        return None

    def __repr__(self) -> str:
        """ If tokens too long, cut at 50 characters """
        raw = " ".join(self.tokens)
        raw = raw[:50] + '...' if len(raw) >= 50 else raw
        return f'{self.__class__.__name__}(raw=[{raw}])'


###############################################################################


class SelectClause(Clause):
    def __init__(self) -> None:
        super().__init__(patterns=['select'])


class FromClause(Clause):
    def __init__(self) -> None:
        super().__init__(patterns=['from'])

    def extract_tables(self) -> List[en.Table]:
        return [] if len(self.tokens) <= self.n_patterns \
            else [en.Table(name=self.tokens[self.n_patterns])]


class WhereClause(Clause):
    def __init__(self) -> None:
        super().__init__(patterns=['where'])


class JoinClause(Clause):
    def __init__(self, patterns: List[Any] = None) -> None:
        super().__init__(patterns=patterns or ['join'])

    def extract_tables(self) -> List[en.Table]:
        return [] if len(self.tokens) <= self.n_patterns \
            else [en.Table(name=self.tokens[self.n_patterns])]


class LeftJoinClause(JoinClause):
    def __init__(self) -> None:
        super().__init__(patterns=['left', 'join'])


class RightJoinClause(JoinClause):
    def __init__(self) -> None:
        super().__init__(patterns=['right', 'join'])


class FullJoinClause(JoinClause):
    def __init__(self) -> None:
        super().__init__(patterns=['full', 'join'])


class InnerJoinClause(JoinClause):
    def __init__(self) -> None:
        super().__init__(patterns=['inner', 'join'])


class OnClause(Clause):
    def __init__(self) -> None:
        super().__init__(patterns=['on'])


class GroupByClause(Clause):
    def __init__(self) -> None:
        super().__init__(patterns=['group', 'by'])


class OrderByClause(Clause):
    def __init__(self) -> None:
        super().__init__(patterns=['order', 'by'])


class HavingClause(Clause):
    def __init__(self) -> None:
        super().__init__(patterns=['having'])


class UnionClause(Clause):
    def __init__(self) -> None:
        super().__init__(patterns=['union'])


class CreateTempFuncClause(Clause):
    def __init__(self) -> None:
        super().__init__(patterns=['create', 'temp', 'function'])


class WithClause(Clause):
    def __init__(self) -> None:
        super().__init__(patterns=['with'])


class CteStartClause(Clause):
    def __init__(self) -> None:
        super().__init__(
            patterns=[re.compile('([a-zA-Z0-9]+)'), 'as', '(', 'select'],
            require_min_tokens=3,
            require_balanced_brackets=False,
        )

    def extract_target(self) -> str:
        return self.tokens[0]


class CteEndClause(Clause):
    def __init__(self) -> None:
        super().__init__(
            patterns=[')', re.compile('(,|select){1}')],
            require_min_tokens=1,
        )


class SubqueryStartClause(Clause):
    def __init__(self) -> None:
        super().__init__(
            pre_patterns=[re.compile('(from|join|in){1}')],
            patterns=['(', 'select'],
            require_min_tokens=1,
            require_balanced_brackets=False,
        )


class SubqueryEndClause(Clause):
    def __init__(self) -> None:
        super().__init__(patterns=[')'])
