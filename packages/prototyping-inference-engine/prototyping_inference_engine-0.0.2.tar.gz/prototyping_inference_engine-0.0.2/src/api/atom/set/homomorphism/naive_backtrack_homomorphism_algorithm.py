from functools import cache
from typing import Iterator

from src.api.atom.atom import Atom
from src.api.atom.set.atom_set import AtomSet
from src.api.atom.set.homomorphism.homomorphism_algorithm import HomomorphismAlgorithm
from src.api.atom.set.index.index_by_predicate import IndexByPredicate
from src.api.atom.set.index.indexed_by_predicate_atom_set import IndexedByPredicateAtomSet
from src.api.substitution.substitution import Substitution


class NaiveBacktrackHomomorphismAlgorithm(HomomorphismAlgorithm):
    @staticmethod
    @cache
    def instance() -> "NaiveBacktrackHomomorphismAlgorithm":
        return NaiveBacktrackHomomorphismAlgorithm()

    def compute_homomorphisms(self, from_atom_set: AtomSet, to_atom_set: AtomSet, sub: Substitution = None) \
            -> Iterator[Substitution]:
        if sub is None:
            sub = Substitution()

        if not from_atom_set.predicates.issubset(to_atom_set.predicates):
            return iter([])

        if isinstance(to_atom_set, IndexedByPredicateAtomSet):
            index = to_atom_set.index_by_predicate
        else:
            index = IndexByPredicate(to_atom_set)

        from_atom_list = list(from_atom_set)

        return self._compute_homomorphisms(from_atom_list, index, sub)

    def _compute_homomorphisms(self, from_atom_list: list[Atom],
                               predicate_index: IndexByPredicate,
                               sub: Substitution,
                               position: int = 0) \
            -> Iterator[Substitution]:
        if position == len(from_atom_list):
            yield sub
        else:
            next_atom = from_atom_list[position]
            for new_sub in predicate_index.extend_substitution(next_atom, sub):
                yield from self._compute_homomorphisms(from_atom_list, predicate_index, new_sub, position+1)
