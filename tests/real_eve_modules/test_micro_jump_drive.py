import sys

from EVE_Gnosis.simulations.capacitor import Capacitor


def test_micro_jump_drive():
    expected_matrix_size = 288
    expected_cached_run_count = 14
    expected_low_water_mark = 0
    expected_time = 2304000
    expected_capacitor_tick_0_percent = 0.92
    expected_capacitor_tick_0_time = 0
    expected_capacitor_tick_7_percent = 0.37
    expected_capacitor_tick_7_time = 1344000
    expected_capacitor_tick_8_percent = 0.29
    expected_capacitor_tick_8_time = 1536000
    expected_capacitor_tick_max_run_percent = 0
    expected_capacitor_tick_max_run_time = 2496000

    capacitor_amount = 10000
    capacitor_recharge = 9999999999999  # Can't set to 0 (divide by 0), set to a large number to kill regen
    module_list = [
        {
            'Amount': -786,
            'CycleTime': 12000,
            'ReactivationDelay': 180000,
        }
    ]  # Micro Jump Drive

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
