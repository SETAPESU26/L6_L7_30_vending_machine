# Lab 6 - Code (Line) Coverage Tests
# Name : Pranavi Sistla
# SRN  : PES1UG24CS338
# Repo : L6_L7_30_vending_machine
#
# Goal: execute every statement in vending_machine.py at least once
# (target >= 90% line coverage).

import pytest
from vending_machine import select_item, make_change, purchase, PRICES


# ---------- select_item ----------

def test_invalid_item():
    # line 7: item not in PRICES
    assert select_item("water", {}, 100) == "invalid"


def test_sold_out_item():
    # line 9: item exists but stock is 0
    assert select_item("cola", {"cola": 0}, 200) == "sold_out"


def test_insufficient_credit():
    # line 11: credit lower than price
    assert select_item("cola", {"cola": 5}, 100) == "insufficient"


def test_valid_selection():
    # line 12: everything ok
    assert select_item("chips", {"chips": 3}, 100) == "ok"


# ---------- make_change ----------

def test_no_change_needed():
    assert make_change(0) == []


def test_negative_amount_raises():
    # line 17: negative amount -> ValueError
    with pytest.raises(ValueError):
        make_change(-10)


def test_change_with_coins():
    # lines 20-22: loop picks coins greedily
    assert make_change(185) == [100, 50, 25, 10]


def test_change_not_possible():
    # line 24: remainder that no coin can pay (not a multiple of 5)
    assert make_change(3) is None


# ---------- purchase ----------

def test_purchase_rejected_status():
    # lines 29-30: select_item did not return "ok"
    assert purchase("water", {}, 500) == ("invalid", [])


def test_purchase_no_exact_change():
    # lines 31-33: change cannot be made
    stock = {"chips": 2}
    assert purchase("chips", stock, 103) == ("no_exact_change", [])
    assert stock["chips"] == 2  # stock untouched


def test_purchase_dispensed():
    # lines 34-35: successful purchase, stock decremented, change returned
    stock = {"cola": 2}
    assert purchase("cola", stock, 200) == ("dispensed", [50])
    assert stock["cola"] == 1
