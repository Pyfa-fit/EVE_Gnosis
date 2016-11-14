import os
import sys

script_dir = os.path.dirname(os.path.abspath(__file__))
# Add Gnosis module to python paths
sys.path.append(os.path.realpath(os.path.join(script_dir, '..', '..')))

from gnosis.simulations.capacitor import Capacitor


def test_module_reactivation_delay_no_charges():
    # Test that a module with a reactivation delay but no charges (such as a MJD) calculates correctly.
    expected_capacitor_tick_0_percent = 0.92
    expected_capacitor_tick_0_time = 0
    expected_capacitor_tick_191_percent = 0.9
    expected_capacitor_tick_191_time = 191000
    expected_capacitor_tick_192_percent = 0.82
    expected_capacitor_tick_192_time = 192000
    expected_capacitor_tick_300_percent = 0.81
    expected_capacitor_tick_300_time = 300000
    capacitor_amount = 10000
    capacitor_recharge = 9999999999999  # Can't set to 0 (divide by 0), set to a large number to kill regen
    module_list = [
        {
            'Amount': -786,
            'CycleTime': 12000,
            'Charges': False,
            'ReloadTime': 180000,
        },
        {
            'Amount': -1,
            'CycleTime': 1000,
            'Charges': False,
            'ReloadTime': False,
        }]

    # This module doesn't do much, we just want to trigger a
    # tick every 1 second so we can better keep track of how
    # often the MJD is firing off.

    matrix = Capacitor.capacitor_time_simulator(module_list,
                                                capacitor_amount,
                                                capacitor_recharge)

    assert expected_capacitor_tick_0_percent == matrix['Cached Runs'][0]['Capacitor Percentage']
    assert expected_capacitor_tick_0_time == matrix['Cached Runs'][0]['Current Time']
    assert expected_capacitor_tick_191_percent == matrix['Cached Runs'][191]['Capacitor Percentage']
    assert expected_capacitor_tick_191_time == matrix['Cached Runs'][191]['Current Time']
    assert expected_capacitor_tick_192_percent == matrix['Cached Runs'][192]['Capacitor Percentage']
    assert expected_capacitor_tick_192_time == matrix['Cached Runs'][192]['Current Time']
    assert expected_capacitor_tick_300_percent == matrix['Cached Runs'][300]['Capacitor Percentage']
    assert expected_capacitor_tick_300_time == matrix['Cached Runs'][300]['Current Time']
