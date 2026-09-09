"""Number coercion and display, shared by the format-driven validators.

Spec and plan fields are free text (``- Total sessions: 30``, ``- Variance (nominal - delivered): -6``),
so a validator doing arithmetic has to pull a number out of a sentence. Both functions were duplicated
verbatim across the delivery-plan and cluster-spec validators, with a third divergent ``num()`` in
``validate_topic_breakdown.py`` (which still carries its own copy); this is the one copy.

Cases: HNUM-01 .. HNUM-07 in factory/docs/test-plan.md.
"""
from __future__ import annotations

import re

# Documents are written with a unicode minus in prose ("nominal - delivered"), which int()/float()
# will not accept - normalise it before matching.
_UNICODE_MINUS = "−"


def num(value):
    """First number in ``value`` as a float, or None if there is none (or value is None)."""
    if value is None:
        return None
    m = re.search(r"[-+]?\d+(?:\.\d+)?", value.replace(_UNICODE_MINUS, "-"))
    return float(m.group(0)) if m else None


def fmt(x) -> str:
    """Display ``x`` without a trailing ``.0`` when it is integral."""
    return str(int(x)) if x is not None and float(x).is_integer() else str(x)
