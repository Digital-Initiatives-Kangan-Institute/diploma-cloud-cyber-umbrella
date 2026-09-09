"""Cases HNUM-01 .. HNUM-07 — factory/docs/test-plan.md.

Covers common/helpers/numeric.py: pulling a number out of a free-text field value, and displaying it
back without a spurious decimal point.
"""
import numeric as N


def test_integer_is_parsed_from_a_string():
    """HNUM-01"""
    assert N.num("Total sessions: 24") == 24.0


def test_decimal_is_parsed_from_a_string():
    """HNUM-02"""
    assert N.num("2.5 sessions per topic") == 2.5


def test_unicode_minus_is_read_as_negative():
    """HNUM-03 — specs write variance as e.g. `−6`, not `-6`."""
    assert N.num("Variance (nominal − delivered): −6") == -6.0


def test_string_without_a_number_returns_none():
    """HNUM-04"""
    assert N.num("yes — a short re-orientation") is None


def test_none_input_returns_none():
    """HNUM-05"""
    assert N.num(None) is None


def test_integral_value_displays_without_a_decimal_point():
    """HNUM-06"""
    assert N.fmt(24.0) == "24"


def test_non_integral_value_keeps_its_decimal_part():
    """HNUM-07"""
    assert N.fmt(2.5) == "2.5"
