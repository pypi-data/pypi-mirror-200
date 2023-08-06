from functools import cache

from src.api.query.containment.conjunctive_query_containment import ConjunctiveQueryContainment
from src.api.query.containment.query_containment import QueryContainment
from src.api.query.union_conjunctive_queries import UnionConjunctiveQueries


class UnionConjunctiveQueriesContainment(QueryContainment[UnionConjunctiveQueries]):
    def __init__(self, cq_containment: ConjunctiveQueryContainment = None):
        if cq_containment:
            self._cq_containment: ConjunctiveQueryContainment = cq_containment
        else:
            self._cq_containment: ConjunctiveQueryContainment = ConjunctiveQueryContainment.instance()

    @staticmethod
    @cache
    def instance(cq_containment: ConjunctiveQueryContainment = None) -> "UnionConjunctiveQueriesContainment":
        return UnionConjunctiveQueriesContainment(cq_containment)

    def is_contained_in(self, ucq1: UnionConjunctiveQueries, ucq2: UnionConjunctiveQueries) -> bool:
        if len(ucq1.answer_variables) != len(ucq2.answer_variables):
            return False

        return all(any(self._cq_containment.is_contained_in(q1, q2) for q2 in ucq2) for q1 in ucq1)
