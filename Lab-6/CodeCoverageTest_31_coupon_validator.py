import pytest
from coupon_validator import coupon_discount, best_discount, is_expired


def test_welcome_new_user():
    assert coupon_discount("WELCOME10", 200, True, "mon") == 20


def test_welcome_existing_user():
    assert coupon_discount("WELCOME10", 200, False, "mon") == 0


def test_weekend20_saturday_large_cart():
    assert coupon_discount("WEEKEND20", 600, True, "sat") == 120


def test_weekend20_sunday_small_cart():
    assert coupon_discount("WEEKEND20", 400, False, "sun") == 50


def test_weekend20_weekday():
    assert coupon_discount("WEEKEND20", 600, True, "mon") == 0


def test_flat100_above_threshold():
    assert coupon_discount("FLAT100", 400, False, "mon") == 100


def test_flat100_at_threshold():
    assert coupon_discount("FLAT100", 300, False, "mon") == 0


def test_unknown_coupon():
    assert coupon_discount("INVALID", 400, False, "mon") == 0


@pytest.mark.parametrize("amount", [0, -1])
def test_invalid_cart(amount):
    with pytest.raises(ValueError, match="empty cart"):
        coupon_discount("WELCOME10", amount, True, "mon")


def test_best_discount_empty_list():
    assert best_discount([], 500, True, "sat") == 0


def test_best_discount_selects_highest():
    assert best_discount(
        ["WELCOME10", "WEEKEND20", "FLAT100"], 1000, True, "sat"
    ) == 200


def test_best_discount_keeps_previous_best():
    assert best_discount(
        ["WEEKEND20", "WELCOME10"], 1000, True, "sat"
    ) == 200


def test_best_discount_cap_not_exceeded():
    assert best_discount(["WELCOME10"], 1000, True, "mon") == 100


def test_zero_validity_expired():
    assert is_expired(10, 5, 0) is True


def test_negative_validity_expired():
    assert is_expired(10, 5, -1) is True


def test_expiry_before_boundary():
    assert is_expired(9, 5, 5) is False


def test_expiry_at_boundary():
    assert is_expired(10, 5, 5) is False


def test_expiry_after_boundary():
    assert is_expired(11, 5, 5) is True
def test_best_discount_cap_return_line():
    assert best_discount([], -1, True, "mon") == -0.4