import pytest
from coupon_validator import coupon_discount, best_discount, is_expired


def test_cart_validation():
    with pytest.raises(ValueError):
        coupon_discount("WELCOME10", 0, True, "mon")

    assert coupon_discount("WELCOME10", 200, True, "mon") == 20


def test_welcome_user_branches():
    assert coupon_discount("WELCOME10", 200, True, "mon") == 20
    assert coupon_discount("WELCOME10", 200, False, "mon") == 0


def test_weekend_code_and_day_branches():
    assert coupon_discount("WEEKEND20", 600, True, "sat") == 120
    assert coupon_discount("WEEKEND20", 600, True, "sun") == 120
    assert coupon_discount("WEEKEND20", 600, True, "mon") == 0
    assert coupon_discount("WELCOME10", 600, True, "sat") == 60


def test_weekend_cart_threshold_branches():
    assert coupon_discount("WEEKEND20", 500, True, "sat") == 100
    assert coupon_discount("WEEKEND20", 499, True, "sat") == 50


def test_flat100_threshold_branches():
    assert coupon_discount("FLAT100", 301, True, "mon") == 100
    assert coupon_discount("FLAT100", 300, True, "mon") == 0
    assert coupon_discount("WELCOME10", 301, True, "mon") == pytest.approx(30.1)


def test_unknown_coupon_branch():
    assert coupon_discount("UNKNOWN", 200, False, "mon") == 0


def test_best_discount_loop_and_comparison_branches():
    assert best_discount([], 500, True, "sat") == 0
    assert best_discount(["WEEKEND20"], 1000, True, "sat") == 200
    assert best_discount(
        ["WEEKEND20", "WELCOME10"], 1000, True, "sat"
    ) == 200
    assert best_discount(
        ["WELCOME10", "WEEKEND20"], 1000, True, "sat"
    ) == 200


def test_best_discount_cap_false_branch():
    assert best_discount(["WELCOME10"], 1000, True, "mon") == 100


def test_expiry_validity_branches():
    assert is_expired(10, 5, 0) is True
    assert is_expired(10, 5, -1) is True
    assert is_expired(9, 5, 5) is False
    assert is_expired(10, 5, 5) is False
    assert is_expired(11, 5, 5) is True