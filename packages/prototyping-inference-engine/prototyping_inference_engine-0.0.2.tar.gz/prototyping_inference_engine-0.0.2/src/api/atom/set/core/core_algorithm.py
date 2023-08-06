from abc import ABC, abstractmethod
from typing import TypeVar

from src.api.atom.set.atom_set import AtomSet
from src.api.atom.term.variable import Variable

AS = TypeVar("AS", bound=AtomSet)


class CoreAlgorithm(ABC):
    @abstractmethod
    def compute_core(self, atom_set: AS, freeze: tuple[Variable] = None) -> AS:
        pass
