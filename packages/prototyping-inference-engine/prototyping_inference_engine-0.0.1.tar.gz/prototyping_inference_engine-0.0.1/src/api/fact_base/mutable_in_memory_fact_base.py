from src.api.atom.atom import Atom
from src.api.atom.set.mutable_atom_set import MutableAtomSet
from src.api.fact_base.in_memory_fact_base import InMemoryFactBase
from src.api.fact_base.mutable_fact_base import MutableFactBase


class MutableInMemoryFactBase(InMemoryFactBase, MutableFactBase):
    def __init__(self):
        InMemoryFactBase.__init__(MutableAtomSet())

    def add(self, atom: Atom):
        self.atom_set.add(atom)

    @property
    def atom_set(self) -> MutableAtomSet:
        return self._atom_set  # type: ignore
