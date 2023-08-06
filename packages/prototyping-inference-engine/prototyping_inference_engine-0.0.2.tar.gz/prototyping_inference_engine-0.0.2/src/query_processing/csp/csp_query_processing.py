from typing import Tuple, Type, Iterable

from src.api.atom.term.term import Term
from src.api.fact_base.fact_base import FactBase
from src.api.query.atomic_query import AtomicQuery
from src.api.query.conjunctive_query import ConjunctiveQuery

from src.api.query.query import Query
from src.api.substitution.substitution import Substitution
from src.query_processing.query_processing import QueryProcessing


class CSPQueryProcessing(QueryProcessing):
    def execute_query(self, target: FactBase, query: Query, sub: Substitution, filter_out_nulls: bool = True)\
            -> Iterable[tuple[Term]]:
        pass

    @classmethod
    def get_supported_query_types(cls) -> Tuple[Type[Query]]:
        return ConjunctiveQuery, AtomicQuery
