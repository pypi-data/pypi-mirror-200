from abc import ABC
from typing import Tuple, Type, Iterator

from src.api.atom.set.atom_set import AtomSet
from src.api.atom.term.term import Term
from src.api.fact_base.fact_base import FactBase
from src.api.query.atomic_query import AtomicQuery
from src.api.query.query import Query
from src.api.substitution.substitution import Substitution
from src.api.query.unsupported_query import UnsupportedQuery


class InMemoryFactBase(FactBase, ABC):
    def __init__(self, atom_set):
        self._atom_set = atom_set

    @classmethod
    def get_supported_query_types(cls) -> Tuple[Type[Query]]:
        return AtomicQuery,

    @property
    def atom_set(self) -> AtomSet:
        return self._atom_set

    def execute_query(self, query: Query, sub: Substitution, filter_out_nulls: bool = True) -> Iterator[Tuple[Term]]:
        match query:
            case AtomicQuery() as aq:
                for t in self.atom_set.match(aq.atom):
                    yield t.terms
            case _:
                raise UnsupportedQuery()
