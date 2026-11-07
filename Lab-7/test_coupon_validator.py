import math
from datetime import date

from hypothesis import given, strategies as st

from coupon_validator import split_code, most_expensive, expiry_days

# Anything a user (or another program) could realistically hand to the functions:
# text, None, numbers, bytes, lists. The functions must never crash on any of them.
ANY_INPUT = st.one_of(
    st.text(),
    st.none(),
    st.integers(),
    st.floats(),
    st.binary(),
    st.lists(st.integers()),
)


# ---------------------------------------------------------------------------
# 1. "Does not crash" tests (the three starter tests, completed)
# ---------------------------------------------------------------------------

@given(st.text() | st.none())
def test_split_code_no_crash(s):
    try:
        split_code(s)
    except Exception as e:
        assert False, f"split_code crashed with: {e!r}"


@given(st.text() | st.none())
def test_most_expensive_no_crash(s):
    try:
        most_expensive(s)
    except Exception as e:
        assert False, f"most_expensive crashed with: {e!r}"


@given(st.text() | st.none())
def test_expiry_days_no_crash(s):
    try:
        expiry_days(s)
    except Exception as e:
        assert False, f"expiry_days crashed with: {e!r}"


# ---------------------------------------------------------------------------
# 2. Non-string inputs (None, numbers, bytes, lists) must not crash either
# ---------------------------------------------------------------------------

@given(ANY_INPUT)
def test_split_code_any_type_no_crash(x):
    try:
        split_code(x)
    except Exception as e:
        assert False, f"split_code crashed on {x!r} with: {e!r}"


@given(ANY_INPUT)
def test_most_expensive_any_type_no_crash(x):
    try:
        most_expensive(x)
    except Exception as e:
        assert False, f"most_expensive crashed on {x!r} with: {e!r}"


@given(ANY_INPUT)
def test_expiry_days_any_type_no_crash(x):
    try:
        expiry_days(x)
    except Exception as e:
        assert False, f"expiry_days crashed on {x!r} with: {e!r}"


# ---------------------------------------------------------------------------
# 3. Output-shape properties: invalid input -> None, valid input -> right type
# ---------------------------------------------------------------------------

@given(st.text() | st.none())
def test_split_code_returns_none_or_valid_pair(s):
    result = split_code(s)
    if result is not None:
        prefix, value = result
        assert isinstance(prefix, str) and prefix != ""
        assert isinstance(value, int) and value >= 0


@given(st.text() | st.none())
def test_most_expensive_returns_none_or_finite_non_negative_float(s):
    result = most_expensive(s)
    if result is not None:
        assert isinstance(result, float)
        assert math.isfinite(result) and result >= 0


@given(st.text() | st.none())
def test_expiry_days_returns_none_or_int(s):
    result = expiry_days(s)
    assert result is None or isinstance(result, int)


# ---------------------------------------------------------------------------
# 4. Valid input must still give the right answer (hardening must not break it)
# ---------------------------------------------------------------------------

@given(
    st.text(alphabet="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", min_size=1),
    st.integers(min_value=0, max_value=10**9),
    st.sampled_from(["", " ", "  ", "\t"]),
)
def test_split_code_valid_roundtrip(prefix, value, pad):
    assert split_code(f"{pad}{prefix.lower()}-{value}{pad}") == (prefix.upper(), value)


@given(
    st.lists(
        st.floats(min_value=0, max_value=1e9, allow_nan=False, allow_infinity=False),
        min_size=1,
    )
)
def test_most_expensive_valid_is_the_maximum(prices):
    csv = ",".join(repr(p) for p in prices)
    assert most_expensive(csv) == max(prices)


@given(st.dates(min_value=date(2000, 1, 1), max_value=date(2100, 12, 28)))
def test_expiry_days_valid_date_matches_formula(d):
    expected = (d.year - 2024) * 365 + (d.month - 1) * 30 + d.day
    assert expiry_days(d.isoformat()) == expected


@given(st.integers(min_value=2000, max_value=2099),
       st.integers(min_value=1, max_value=12),
       st.integers(min_value=1, max_value=27))
def test_expiry_days_later_day_is_larger(year, month, day):
    earlier = expiry_days(f"{year}-{month:02d}-{day:02d}")
    later = expiry_days(f"{year}-{month:02d}-{day + 1:02d}")
    assert later == earlier + 1


# ---------------------------------------------------------------------------
# 5. Specific edge cases that Hypothesis tends to find, kept as regression tests
# ---------------------------------------------------------------------------

def test_split_code_known_bad_inputs():
    for bad in ["", "save", "save-", "-20", "save-20-30", "save--20",
                "save-abc", "save-2.5", "save-+5", "save-1_0", "-", "--",
                "sa ve-20", "save-٢٠"]:
        assert split_code(bad) is None, bad
    assert split_code(None) is None


def test_most_expensive_known_bad_inputs():
    for bad in ["", ",", "1,,3", "1,2,", ",1", "abc", "1,two", "nan", "inf",
                "-inf", "1e999", "-5", "1,-5", "1_0"]:
        assert most_expensive(bad) is None, bad
    assert most_expensive(None) is None


def test_expiry_days_known_bad_inputs():
    for bad in ["", "2025", "2025-06", "2025-06-15-01", "2025-13-01", "2025-00-10",
                "2025-02-30", "2025-06-31", "0000-01-01", "10000-01-01",
                "abcd-ef-gh", "2025-6-+5", "２０２５-06-15"]:
        assert expiry_days(bad) is None, bad
    assert expiry_days(None) is None
