from abc import abstractmethod

from src.api.atom.set.atom_set import AtomSet
from src.api.atom.set.index.index_by_predicate import IndexByPredicate


class IndexedByPredicateAtomSet(AtomSet):
    @property
    @abstractmethod
    def index_by_predicate(self) -> IndexByPredicate:
        pass
