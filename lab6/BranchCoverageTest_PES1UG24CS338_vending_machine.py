# Lab 6 - Branch Coverage Tests
# Name : Pranavi Sistla
# SRN  : PES1UG24CS338
# Repo : L6_L7_30_vending_machine
#
# Goal: make every decision (if / for / while) in vending_machine.py
# evaluate to both True and False (target >= 90% branch coverage).
# Also checks boundary values for each comparison.

import pytest
from vending_machine import select_item, make_change, purchase, PRICES


# ---------- select_item ----------
# Decision 1: item not in PRICES      -> True / False
# Decision 2: stock.get(item,0) == 0  -> True / False
# Decision 3: credit < PRICES[item]   -> True / False

def test_item_not_in_prices_true():
    assert select_item("water", {"water": 5}, 500) == "invalid"


def test_item_missing_from_stock_dict_is_sold_out():
    # Decision 1 False, Decision 2 True via default value 0
    assert select_item("candy", {}, 500) == "sold_out"


def test_item_stock_zero_is_sold_out():
    assert select_item("chips", {"chips": 0}, 500) == "sold_out"


def test_credit_one_below_price_is_insufficient():
    # Decision 3 True (boundary: price - 1)
    assert select_item("candy", {"candy": 1}, PRICES["candy"] - 1) == "insufficient"


def test_credit_equal_to_price_is_ok():
    # Decision 3 False (boundary: exactly price)
    assert select_item("candy", {"candy": 1}, PRICES["candy"]) == "ok"


def test_credit_above_price_is_ok():
    assert select_item("cola", {"cola": 10}, 1000) == "ok"


# ---------- make_change ----------
# Decision 4: amount < 0            -> True / False
# Loop 5:     for coin in COINS     -> enters / exits
# Loop 6:     while amount >= coin  -> True / False
# Decision 7: amount > 0            -> True / False

def test_negative_amount_raises():
    with pytest.raises(ValueError):
        make_change(-1)


def test_zero_amount_while_never_true():
    # Decision 4 False, while loop False for every coin, Decision 7 False
    assert make_change(0) == []


def test_single_coin_each_denomination():
    assert make_change(100) == [100]
    assert make_change(50) == [50]
    assert make_change(25) == [25]
    assert make_change(10) == [10]
    assert make_change(5) == [5]


def test_while_loop_repeats_same_coin():
    # while loop True more than once for the same coin
    assert make_change(300) == [100, 100, 100]


def test_all_denominations_used():
    assert make_change(190) == [100, 50, 25, 10, 5]


def test_remainder_left_returns_none():
    # Decision 7 True: leftover amount that no coin can pay
    assert make_change(7) is None
    assert make_change(1) is None


# ---------- purchase ----------
# Decision 8: status != "ok"   -> True / False
# Decision 9: change is None   -> True / False

@pytest.mark.parametrize(
    "item, stock, credit, expected_status",
    [
        ("water", {}, 500, "invalid"),
        ("cola", {"cola": 0}, 500, "sold_out"),
        ("cola", {"cola": 3}, 100, "insufficient"),
    ],
)
def test_purchase_status_not_ok(item, stock, credit, expected_status):
    before = dict(stock)
    assert purchase(item, stock, credit) == (expected_status, [])
    assert stock == before  # nothing dispensed


def test_purchase_no_exact_change():
    # Decision 8 False, Decision 9 True
    stock = {"candy": 4}
    assert purchase("candy", stock, 77) == ("no_exact_change", [])
    assert stock["candy"] == 4


def test_purchase_exact_credit_no_change():
    # Decision 9 False with empty change list
    stock = {"chips": 1}
    assert purchase("chips", stock, 100) == ("dispensed", [])
    assert stock["chips"] == 0


def test_purchase_with_change():
    stock = {"candy": 2}
    assert purchase("candy", stock, 200) == ("dispensed", [100, 25])
    assert stock["candy"] == 1


def test_purchase_until_sold_out():
    # last item dispensed, next attempt reports sold_out
    stock = {"cola": 1}
    assert purchase("cola", stock, 150) == ("dispensed", [])
    assert purchase("cola", stock, 150) == ("sold_out", [])
