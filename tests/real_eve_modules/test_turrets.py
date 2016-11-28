import os
import sys

script_dir = os.path.dirname(os.path.abspath(__file__))
# Add Gnosis module to python paths
sys.path.append(os.path.realpath(os.path.join(script_dir, '..', '..')))

# noinspection PyPep8
from EVE_Gnosis.simulations.capacitor import Capacitor


def test_heavy_ion_blaster_ii_void():
    expected_matrix_size = 288
    expected_cached_run_count = 3364
    expected_low_water_mark = 2.069232064593132
    expected_time = 1916829.51999992
    expected_capacitor_tick_0_percent = 1
    expected_capacitor_tick_0_time = 0
    expected_capacitor_tick_7_percent = 1
    expected_capacitor_tick_7_time = 4059.7200000000007
    expected_capacitor_tick_8_percent = 1
    expected_capacitor_tick_8_time = 4639.680000000001
    expected_capacitor_tick_max_run_percent = 0
    expected_capacitor_tick_max_run_time = 2018409.47999992

    capacitor_amount = 10000
    capacitor_recharge = 9999999999999  # Can't set to 0 (divide by 0), set to a large number to kill regen

    turret_slots = 5
    turret_count = 0
    delay_time = 0
    cycle_time = 2899.8000000000006
    module_list = []
    while turret_count < turret_slots:
        module_list.append(
            {
                'Amount': -3.06403125,
                'CycleTime': cycle_time,
                'ReloadTime': 5000,
                'Charges': 120,
                'DelayTime': delay_time,  # Stagger guns
            }
        )  # 5 x Heavy Ion Blaster II with Void ammo
        turret_count += 1
        delay_time += cycle_time / turret_slots

    matrix = Capacitor.capacitor_time_simulator(module_list,
                                                capacitor_amount,
                                                capacitor_recharge)

    cached_runs_count = 0
    for _ in matrix['Cached Runs']:
        cached_runs_count += 1

    assert sys.getsizeof(matrix) == expected_matrix_size
    assert cached_runs_count == expected_cached_run_count
    assert matrix['Stability']['LowWaterMark'] == expected_low_water_mark
    assert matrix['Stability']['Time'] == expected_time

    assert expected_capacitor_tick_0_percent == matrix['Cached Runs'][0]['Capacitor Percentage']
    assert expected_capacitor_tick_0_time == matrix['Cached Runs'][0]['Current Time']
    assert expected_capacitor_tick_7_percent == matrix['Cached Runs'][7]['Capacitor Percentage']
    assert expected_capacitor_tick_7_time == matrix['Cached Runs'][7]['Current Time']
    assert expected_capacitor_tick_8_percent == matrix['Cached Runs'][8]['Capacitor Percentage']
    assert expected_capacitor_tick_8_time == matrix['Cached Runs'][8]['Current Time']
    assert expected_capacitor_tick_max_run_percent == matrix['Cached Runs'][cached_runs_count - 1][
        'Capacitor Percentage']
    assert expected_capacitor_tick_max_run_time == matrix['Cached Runs'][cached_runs_count - 1]['Current Time']
