from abc import ABC, abstractmethod
from typing import TypeVar

from src.api.ontology.rule.rule import Rule
from src.api.query.query import Query
from src.api.query.union_conjunctive_queries import UnionConjunctiveQueries


BodyQueryType = TypeVar("BodyQueryType", bound=Query)
HeadQueryType = TypeVar("HeadQueryType", bound=Query)


class UcqRewritingAlgorithm(ABC):
    @abstractmethod
    def rewrite(self,
                ucq: UnionConjunctiveQueries,
                rule_set: set[Rule[BodyQueryType, HeadQueryType]]) -> UnionConjunctiveQueries:
        pass
