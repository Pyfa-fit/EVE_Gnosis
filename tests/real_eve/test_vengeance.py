import os
import sys

script_dir = os.path.dirname(os.path.abspath(__file__))
# Add Gnosis module to python paths
sys.path.append(os.path.realpath(os.path.join(script_dir, '..', '..')))

from gnosis.simulations.capacitor import Capacitor
from gnosis.formulas.formulas import Formulas


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
        }
    )  # Small Ancilliary Armor Repairer (no paste)

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
    expected_capacitor_percent = 0.24
    expected_capacitor_delta = 8.887120876962797
    peak = regen_peak()
    assert expected_capacitor_percent == peak['PeakPercent']
    assert expected_capacitor_delta == peak['PeakDelta']


def test_simulation():
    expected_cached_run_count = 871
    expected_low_water_mark = 153.99624594529422
    expected_time = 1332000
    matrix = simulation_matrix()
    cached_runs_count = 0
    for _ in matrix['Cached Runs']:
        cached_runs_count += 1

    assert cached_runs_count == expected_cached_run_count
    assert matrix['Stability']['LowWaterMark'] == expected_low_water_mark
    assert matrix['Stability']['Time'] == expected_time
