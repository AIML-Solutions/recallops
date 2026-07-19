from recallops.ids import stable_id


def test_stable_id_is_repeatable() -> None:
    assert stable_id("doc", "source", "text") == stable_id("doc", "source", "text")


def test_stable_id_changes_with_payload() -> None:
    assert stable_id("doc", "source", "a") != stable_id("doc", "source", "b")
