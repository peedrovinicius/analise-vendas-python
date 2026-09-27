import pytest

from scripts.validate_published_results import _assert_close


def test_assert_close_accepts_value_inside_tolerance() -> None:
    _assert_close("metric", 10.004, 10.0, 0.005)


def test_assert_close_rejects_value_outside_tolerance() -> None:
    with pytest.raises(AssertionError, match="metric"):
        _assert_close("metric", 10.01, 10.0, 0.005)
