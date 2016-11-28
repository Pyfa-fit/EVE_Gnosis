import os
import sys

script_dir = os.path.dirname(os.path.abspath(__file__))
# Add Gnosis module to python paths
sys.path.append(os.path.realpath(os.path.join(script_dir, '..', '..')))

# noinspection PyPep8
from EVE_Gnosis.simulations.capacitor import Capacitor


def test_small_ancilliary_armor_repairer():
    expected_matrix_size = 288
    expected_cached_run_count = 55
    expected_low_water_mark = 7800.00032235305
    expected_time = 603000
    expected_capacitor_tick_0_percent = 1
    expected_capacitor_tick_0_time = 0
    expected_capacitor_tick_7_percent = 0.97
    expected_capacitor_tick_7_time = 31500
    expected_capacitor_tick_8_percent = 0.96
    expected_capacitor_tick_8_time = 96000
    expected_capacitor_tick_max_run_percent = .78
    expected_capacitor_tick_max_run_time = 603000

    capacitor_amount = 10000
    capacitor_recharge = 9999999999999  # Can't set to 0 (divide by 0), set to a large number to kill regen
    module_list = [
        {
            'Amount': -40,
            'CycleTime': 4500,
            'Charges': 8,
            'ReloadTime': 60000,
        }
    ]  # Small Ancilliary Armor Repairer (with paste)

    matrix = Capacitor.capacitor_time_simulator(module_list,
                                                capacitor_amount,
                                                capacitor_recharge)

    cached_runs_count = 0
    for _ in matrix['Cached Runs']:
        cached_runs_count += 1

    assert sys.getsizeof(matrix) == expected_matrix_size
    assert expected_cached_run_count == cached_runs_count
    assert expected_low_water_mark == matrix['Stability']['LowWaterMark']
    assert expected_time == matrix['Stability']['LowWaterMarkTime']
    assert expected_capacitor_tick_0_percent == matrix['Cached Runs'][0]['Capacitor Percentage']
    assert expected_capacitor_tick_0_time == matrix['Cached Runs'][0]['Current Time']
    assert expected_capacitor_tick_7_percent == matrix['Cached Runs'][7]['Capacitor Percentage']
    assert expected_capacitor_tick_7_time == matrix['Cached Runs'][7]['Current Time']
    assert expected_capacitor_tick_8_percent == matrix['Cached Runs'][8]['Capacitor Percentage']
    assert expected_capacitor_tick_8_time == matrix['Cached Runs'][8]['Current Time']
    assert expected_capacitor_tick_max_run_percent == matrix['Cached Runs'][cached_runs_count - 1][
        'Capacitor Percentage']
    assert expected_capacitor_tick_max_run_time == matrix['Cached Runs'][cached_runs_count - 1]['Current Time']


def test_small_ancilliary_armor_repairer_no_paste():
    expected_matrix_size = 288
    expected_cached_run_count = 135
    expected_low_water_mark = 4600.000720432291
    expected_time = 603000
    expected_capacitor_tick_0_percent = 1
    expected_capacitor_tick_0_time = 0
    expected_capacitor_tick_7_percent = 0.97
    expected_capacitor_tick_7_time = 31500
    expected_capacitor_tick_8_percent = 0.96
    expected_capacitor_tick_8_time = 36000
    expected_capacitor_tick_max_run_percent = .46
    expected_capacitor_tick_max_run_time = 603000

    capacitor_amount = 10000
    capacitor_recharge = 9999999999999  # Can't set to 0 (divide by 0), set to a large number to kill regen
    module_list = [
        {
            'Amount': -40,
            'CycleTime': 4500,
        }
    ]  # Small Ancilliary Armor Repairer (no paste)

    matrix = Capacitor.capacitor_time_simulator(module_list,
                                                capacitor_amount,
                                                capacitor_recharge)

    cached_runs_count = 0
    for _ in matrix['Cached Runs']:
        cached_runs_count += 1

    assert sys.getsizeof(matrix) == expected_matrix_size
    assert expected_cached_run_count == cached_runs_count
    assert expected_low_water_mark == matrix['Stability']['LowWaterMark']
    assert expected_time == matrix['Stability']['LowWaterMarkTime']
    assert expected_capacitor_tick_0_percent == matrix['Cached Runs'][0]['Capacitor Percentage']
    assert expected_capacitor_tick_0_time == matrix['Cached Runs'][0]['Current Time']
    assert expected_capacitor_tick_7_percent == matrix['Cached Runs'][7]['Capacitor Percentage']
    assert expected_capacitor_tick_7_time == matrix['Cached Runs'][7]['Current Time']
    assert expected_capacitor_tick_8_percent == matrix['Cached Runs'][8]['Capacitor Percentage']
    assert expected_capacitor_tick_8_time == matrix['Cached Runs'][8]['Current Time']
    assert expected_capacitor_tick_max_run_percent == matrix['Cached Runs'][cached_runs_count - 1][
        'Capacitor Percentage']
    assert expected_capacitor_tick_max_run_time == matrix['Cached Runs'][cached_runs_count - 1]['Current Time']
