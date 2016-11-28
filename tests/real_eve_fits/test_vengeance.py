import os
import sys

script_dir = os.path.dirname(os.path.abspath(__file__))
# Add Gnosis module to python paths
sys.path.append(os.path.realpath(os.path.join(script_dir, '..', '..')))

# noinspection PyPep8
from EVE_Gnosis.simulations.capacitor import Capacitor
# noinspection PyPep8
from EVE_Gnosis.formulas.formulas import Formulas


def build_module_list():
    module_list = []

    '''
    [Vengeance, Heavy Tackle]

    Energized Adaptive Nano Membrane II
    Small Ancillary Armor Repairer
    Reactive Armor Hardener
    True Sansha Adaptive Nano Plating

    5MN Quad LiF Restrained Microwarpdrive
    J5b Enduring Warp Scrambler
    X5 Enduring Stasis Webifier

    Rocket Launcher II, Nova Rage Rocket
    Rocket Launcher II, Nova Rage Rocket
    Rocket Launcher II, Nova Rage Rocket
    Rocket Launcher II, Nova Rage Rocket
    Small Energy Nosferatu II

    Small Anti-Thermal Pump II
    Small Auxiliary Nano Pump II
    '''

    module_list.append(
        {
            'Amount': 10,
            'CycleTime': 2500,
        }
    )  # Small T2 Nos

    module_list.append(
        {
            'Amount': -1.5,
            'CycleTime': 5000,
        }
    )  # J5b Enduring Warp Scrambler

    module_list.append(
        {
            'Amount': -1.5,
            'CycleTime': 5000,
        }
    )  # X5 Enduring Statis Webifier

    module_list.append(
        {
            'Amount': -40,
            'CycleTime': 4500,
            'Charges': 8,
            'ReloadTime': 60000,
        }
    )  # Small Ancilliary Armor Repairer (with paste)

    module_list.append(
        {
            'Amount': -10.5,
            'CycleTime': 5000,
        }
    )  # Reactive Armor Hardener

    return module_list


def capacitor_amount():
    value = 375
    return value


def capacitor_recharge():
    value = 105468.75
    return value


def simulation_matrix():
    matrix = Capacitor.capacitor_time_simulator(build_module_list(),
                                                capacitor_amount(),
                                                capacitor_recharge())
    return matrix


def regen_matrix():
    matrix = Formulas.capacitor_shield_regen_matrix(capacitor_amount(), capacitor_recharge())
    return matrix


def regen_peak():
    matrix = regen_matrix()
    high_water_percent = 0
    high_water_delta = 0
    for item in matrix:
        if high_water_delta < item['DeltaAmount']:
            high_water_percent = item['Percent']
            high_water_delta = item['DeltaAmount']

    return {'PeakDelta': high_water_delta, 'PeakPercent': high_water_percent}


def test_peak_capacitor():
    # Check that the peak capacitor regen is the expected percent and delta
    expected_matrix_size = 288
    expected_capacitor_percent = 0.24
    expected_capacitor_delta = 8.887120876962797

    peak = regen_peak()

    assert sys.getsizeof(peak) == expected_matrix_size
    assert expected_capacitor_percent == peak['PeakPercent']
    assert expected_capacitor_delta == peak['PeakDelta']


def test_simulation():
    expected_matrix_size = 288
    expected_cached_run_count = 120
    expected_low_water_mark = 211.91023291385895
    expected_time = 31500
    expected_capacitor_tick_0_percent = 0.86
    expected_capacitor_tick_0_time = 0
    expected_capacitor_tick_7_percent = 0.8
    expected_capacitor_tick_7_time = 12500
    expected_capacitor_tick_8_percent = 0.7
    expected_capacitor_tick_8_time = 13500
    expected_capacitor_tick_max_run_percent = 0.92
    expected_capacitor_tick_max_run_time = 250000
    expected_failed_to_run_modules = False

    matrix = simulation_matrix()
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
    assert expected_failed_to_run_modules == matrix['Stability']['FailedToRunModules']
