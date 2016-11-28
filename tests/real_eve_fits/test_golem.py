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
    Note that not all modules effect cap.
    Even though the full fit is below,most of the modules have no impact on cap.

    [Golem, TANKINESSISKING]

    Shadow Serpentis Damage Control
    Dread Guristas Ballistic Control System
    Dread Guristas Ballistic Control System
    Dread Guristas Ballistic Control System

    Pith X-Type X-Large Shield Booster
    Pithum A-Type Adaptive Invulnerability Field
    Pithum A-Type Adaptive Invulnerability Field
    Pith X-Type EM Ward Field
    Pith X-Type Shield Boost Amplifier
    Republic Fleet Large Cap Battery
    Dark Blood Heavy Capacitor Booster, Navy Cap Booster 800

    Bastion Module I
    Rapid Heavy Missile Launcher II
    Rapid Heavy Missile Launcher II
    Rapid Heavy Missile Launcher II
    Rapid Heavy Missile Launcher II
    Corpum A-Type Medium Energy Nosferatu
    Corpum A-Type Medium Energy Nosferatu
    Imperial Navy Large EMP Smartbomb

    Large Core Defense Capacitor Safeguard II
    Large Core Defense Operational Solidifier II
    '''

    neut_slots = 2
    neut_count = 0
    neut_delay = 0
    neut_cycle_time = 5000
    while neut_count < neut_slots:
        module_list.append(
            {
                'Amount': -36,
                'CycleTime': neut_cycle_time,
                'DelayTime': neut_delay,
            }
        )  # 2 x Corpum A-Type Medium Energy Nosferatu
        neut_count += 1
        neut_delay += neut_cycle_time / neut_slots

    module_list.append(
        {
            'Amount': -130,
            'CycleTime': 7500,
        }
    )  # Imperial Navy Large EMP Smartbomb

    module_list.append(
        {
            'Amount': -306,
            'CycleTime': 3200,
        }
    )  # Pith X-Type X-Large Shield Booster

    resist_slots = 2
    resist_count = 0
    resist_delay = 0
    resist_cycle_time = 12000
    while resist_count < resist_slots:
        module_list.append(
            {
                'Amount': -40,
                'CycleTime': resist_cycle_time,
                'DelayTime': resist_delay,
            }
        )  # 2 x Pithum A-Type Adaptive Invulnerability Field
        resist_count += 1
        resist_delay += resist_cycle_time / resist_slots

    module_list.append(
        {
            'Amount': -20,
            'CycleTime': 12000,
        }
    )  # Pith X-Type EM Ward Field

    module_list.append(
        {
            'Amount': 3200,
            'CycleTime': 11250,
            'ReloadTime': 10000,
            'Charges': 1,
            'FireAtPercent': .2,
        }
    )  # Dark Blood Heavy Capacitor Booster, Navy Cap Booster 3200

    return module_list


def capacitor_amount():
    value = 10181.25
    return value


def capacitor_recharge():
    value = 862500
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
    expected_matrix_size = 288
    expected_capacitor_percent = 0.25
    expected_capacitor_delta = 29.510540414111347

    peak = regen_peak()

    assert sys.getsizeof(peak) == expected_matrix_size
    assert expected_capacitor_percent == peak['PeakPercent']
    assert expected_capacitor_delta == peak['PeakDelta']


def test_simulation():
    expected_matrix_size = 288
    expected_cached_run_count = 677
    expected_low_water_mark = 1621.8674385430204
    expected_time = 307500
    expected_capacitor_tick_0_percent = 0.95
    expected_capacitor_tick_0_time = 0
    expected_capacitor_tick_7_percent = 0.91
    expected_capacitor_tick_7_time = 5000
    expected_capacitor_tick_8_percent = 0.91
    expected_capacitor_tick_8_time = 6000
    expected_capacitor_tick_max_run_percent = 0.22
    expected_capacitor_tick_max_run_time = 600500.0
    expected_failed_to_run_modules = False

    matrix = simulation_matrix()

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
    assert expected_failed_to_run_modules == matrix['Stability']['FailedToRunModules']
