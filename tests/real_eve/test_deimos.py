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
    Note that not all modules effect cap.  Even though the full fit is below,most of the modules have no impact on cap.

    [Deimos, LCB Deimos]

    Reactive Armor Hardener
    Energized Adaptive Nano Membrane II
    Energized Adaptive Nano Membrane II
    Energized Explosive Membrane II
    Magnetic Field Stabilizer II
    Medium Armor Repairer II

    50MN Quad LiF Restrained Microwarpdrive
    Stasis Webifier II
    Small Electrochemical Capacitor Booster I, Navy Cap Booster 100
    Large Compact Pb-Acid Cap Battery

    Heavy Ion Blaster II, Void M
    Heavy Ion Blaster II, Void M
    Heavy Ion Blaster II, Void M
    Heavy Ion Blaster II, Void M
    Heavy Ion Blaster II, Void M

    Medium Auxiliary Nano Pump I
    Medium Auxiliary Nano Pump I
    '''
    # Deimos Modules

    turret_slots = 5
    turret_count = 0
    while turret_count < turret_slots:
        module_list.append(
            {
                'Amount': -3.06403125,
                'CycleTime': 2899.8000000000006,
                'ReloadTime': 5000,
                'Charges': 120,
            }
        )  # 5 x Heavy Ion Blaster II with Void ammo
        turret_count += 1

    module_list.append(
        {
            'Amount': -135,
            'CycleTime': 10000,
        }
    )  # 50mn Quad LiF Restrained Microwarpdrive

    module_list.append(
        {
            'Amount': -4.5,
            'CycleTime': 5000,
        }
    )  # Stasis Webifier II

    module_list.append(
        {
            'Amount': 100,
            'CycleTime': 12000,
            'ReloadTime': 10000,
            'Charges': 4,
            'DelayTime': 10000,  # Delay running this right away, so we don't waste charges
        }
    )  # Small Electrochemical Capacitor Booster I

    module_list.append(
        {
            'Amount': -10.5,
            'CycleTime': 5000,
        }
    )  # Reactive Armor Hardener

    module_list.append(
        {
            'Amount': -160,
            'CycleTime': 9000,
        }
    )  # Medium Armor Repairer II

    return module_list


def capacitor_amount():
    value = 2830
    return value


def capacitor_recharge():
    value = 168750
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


def test_peak_capacitor_regen():
    # Check that the peak capacitor regen is the expected percent and delta
    expected_capacitor_percent = 0.24
    expected_capacitor_delta = 41.92167610022477
    peak = regen_peak()
    assert expected_capacitor_percent == peak['PeakPercent']
    assert expected_capacitor_delta == peak['PeakDelta']


def test_simulation():
    expected_cached_run_count = 451
    expected_low_water_mark = 1412.806156339044
    expected_time = 440999.9999999997
    matrix = simulation_matrix()
    cached_runs_count = 0
    for _ in matrix['Cached Runs']:
        cached_runs_count += 1

    assert cached_runs_count == expected_cached_run_count
    assert matrix['Stability']['LowWaterMark'] == expected_low_water_mark
    assert matrix['Stability']['Time'] == expected_time
