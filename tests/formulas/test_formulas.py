import os
import sys

script_dir = os.path.dirname(os.path.abspath(__file__))
# Add Gnosis module to python paths
sys.path.append(os.path.realpath(os.path.join(script_dir, '..', '..')))

from gnosis.formulas.formulas import Formulas


"""
Test capacitor_shield_tick formula.
    capacitor_shield_tick(maximum_amount, current_amount, recharge_rate, end_time=1000, start_time=0):

These are simply some sanity checks to make sure that something doesn't change along the way.
These are not real numbers or validated against in game numbers.

Test name format: capacitor_shield_tick_[maximum]_[current]_[recharge]_[end]_[start]
Where [name] is the number being passed in
[end] and [start] are optional.

Example: test_capacitor_shield_tick_100_0_10000
Example: test_capacitor_shield_tick_100_0_10000_1000_0
"""

def test_capacitor_shield_tick_100_0_10000():
    # Check 1 tick
    expected_return = 15.481812174617549
    tick = Formulas.capacitor_shield_tick(100, 0, 10000)
    assert tick == expected_return

def test_capacitor_shield_tick_100_25_10000():
    # Check 1 tick
    expected_return = 48.543920058022714
    tick = Formulas.capacitor_shield_tick(100, 25, 10000)
    assert tick == expected_return

def test_capacitor_shield_tick_100_50_10000():
    # Check 1 tick
    expected_return = 67.62616322697144
    tick = Formulas.capacitor_shield_tick(100, 50, 10000)
    assert tick == expected_return

def test_capacitor_shield_tick_100_75_10000():
    # Check 1 tick
    expected_return = 84.40837384263237
    tick = Formulas.capacitor_shield_tick(100, 75, 10000)
    assert tick == expected_return
def test_capacitor_shield_tick_100_0_10000_10000():
    # Check 10 ticks
    expected_return = 98.65695059315915
    tick = Formulas.capacitor_shield_tick(100, 0, 10000, 10000)
    assert tick == expected_return

def test_capacitor_shield_tick_100_0_10000_20000_20000():
    # Check 10 ticks, should be same results as above
    expected_return = 98.65695059315915
    tick = Formulas.capacitor_shield_tick(100, 0, 10000, 20000, 10000)
    assert tick == expected_return

def test_capacitor_shield_tick_100000_0_10000000():
    # Check 1 tick
    expected_return = 0.024987503645050178
    tick = Formulas.capacitor_shield_tick(100000, 0, 10000000)
    assert tick == expected_return

def test_capacitor_shield_tick_100000_0_10000000_10000():
    # Check 10 ticks
    expected_return = 2.4875363803426804
    tick = Formulas.capacitor_shield_tick(100000, 0, 10000000, 10000)
    assert tick == expected_return

def test_capacitor_shield_tick_100000_0_10000000_20000_10000():
    # Check 10 ticks, should be same results as above
    expected_return = 2.4875363803426804
    tick = Formulas.capacitor_shield_tick(100000, 0, 10000000, 20000, 10000)
    assert tick == expected_return

def test_capacitor_shield_tick_37337_0_8008135():
    # Check 1 tick
    expected_return = 0.014546064622025907
    tick = Formulas.capacitor_shield_tick(37337, 0, 8008135)
    assert tick == expected_return

def test_capacitor_shield_tick_37337_0_8008135_10000():
    # Check 10 ticks
    expected_return = 1.4464601872474037
    tick = Formulas.capacitor_shield_tick(37337, 0, 8008135, 10000)
    assert tick == expected_return

def test_capacitor_shield_tick_37337_0_8008135_20000_10000():
    # Check 10 ticks, should be same results as above
    expected_return = 1.4464601872474037
    tick = Formulas.capacitor_shield_tick(37337, 0, 8008135, 20000, 10000)
    assert tick == expected_return