from recallops.eval.metrics import mean_reciprocal_rank, recall_at_k, reciprocal_rank


def test_recall_at_k() -> None:
    assert recall_at_k(["a", "b", "c"], {"b", "d"}, 2) == 0.5


def test_reciprocal_rank() -> None:
    assert reciprocal_rank(["a", "b", "c"], {"c"}) == 1 / 3


def test_mean_reciprocal_rank() -> None:
    assert mean_reciprocal_rank([["a", "b"], ["c", "d"]], [{"b"}, {"x"}]) == 0.25
