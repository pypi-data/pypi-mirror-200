from abc import abstractmethod
from typing import Iterable

from src.api.atom.term.term import Term
from src.api.fact_base.fact_base import FactBase
from src.api.query.query import Query
from src.api.query.query_support import QuerySupport


class QueryProcessing(QuerySupport):
    @abstractmethod
    def execute_query(self, target: FactBase, query: Query) -> Iterable[tuple[Term]]:
        pass
