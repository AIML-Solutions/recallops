from __future__ import annotations


def recall_at_k(retrieved: list[str], relevant: set[str], k: int) -> float:
    if not relevant:
        return 0.0
    hits = set(retrieved[:k]) & relevant
    return len(hits) / len(relevant)


def reciprocal_rank(retrieved: list[str], relevant: set[str]) -> float:
    for index, item in enumerate(retrieved, start=1):
        if item in relevant:
            return 1.0 / index
    return 0.0


def mean_reciprocal_rank(rankings: list[list[str]], relevant_sets: list[set[str]]) -> float:
    if not rankings:
        return 0.0
    scores = [
        reciprocal_rank(ranking, relevant)
        for ranking, relevant in zip(rankings, relevant_sets, strict=True)
    ]
    return sum(scores) / len(scores)
