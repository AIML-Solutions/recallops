from __future__ import annotations

from typing import Any


def metadata_matches(metadata: dict[str, Any], filters: dict[str, Any]) -> bool:
    for key, expected in filters.items():
        actual = _nested_get(metadata, key)
        if isinstance(expected, dict):
            if not _compare(actual, expected):
                return False
        elif isinstance(expected, list):
            actual_values = actual if isinstance(actual, list) else [actual]
            if not all(item in actual_values for item in expected):
                return False
        elif actual != expected:
            return False
    return True


def _nested_get(payload: dict[str, Any], dotted_key: str) -> Any:
    current: Any = payload
    for part in dotted_key.split("."):
        if not isinstance(current, dict) or part not in current:
            return None
        current = current[part]
    return current


def _compare(actual: Any, operators: dict[str, Any]) -> bool:
    for op, expected in operators.items():
        if op == "gte" and not (actual is not None and actual >= expected):
            return False
        if op == "gt" and not (actual is not None and actual > expected):
            return False
        if op == "lte" and not (actual is not None and actual <= expected):
            return False
        if op == "lt" and not (actual is not None and actual < expected):
            return False
        if op == "eq" and actual != expected:
            return False
        if op not in {"gte", "gt", "lte", "lt", "eq"}:
            raise ValueError(f"unsupported filter operator: {op}")
    return True


def to_qdrant_filter(filters: dict[str, Any]) -> dict[str, Any] | None:
    if not filters:
        return None
    must: list[dict[str, Any]] = []
    for key, expected in filters.items():
        if isinstance(expected, dict):
            range_filter = {
                op: value for op, value in expected.items() if op in {"gt", "gte", "lt", "lte"}
            }
            if range_filter:
                must.append({"key": key, "range": range_filter})
            elif "eq" in expected:
                must.append({"key": key, "match": {"value": expected["eq"]}})
            else:
                raise ValueError(f"unsupported qdrant filter operators for {key}")
        elif isinstance(expected, list):
            for item in expected:
                must.append({"key": key, "match": {"value": item}})
        else:
            must.append({"key": key, "match": {"value": expected}})
    return {"must": must}
