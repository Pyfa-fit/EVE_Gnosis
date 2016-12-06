# Test abstract things, usually situations were should _never_ come across.

import os
import sys

from pytest import raises

script_dir = os.path.dirname(os.path.abspath(__file__))
# Add Gnosis module to python paths
sys.path.append(os.path.realpath(os.path.join(script_dir, '..', '..')))

# noinspection PyPep8
from EVE_Gnosis.simulations.capacitor import Capacitor


def run_simulation(module_list, capacitor_amount, capacitor_recharge):
    matrix = Capacitor.capacitor_time_simulator(module_list,
                                                capacitor_amount,
                                                capacitor_recharge
                                                )
    return matrix


def test_empty_module_list():
    expected_matrix_size = 288
    expected_cached_run_count = 0
    expected_low_water_mark = 10000
    expected_time = 0
    expected_failed_to_run_modules = False

    module_list = []
    capacitor_amount = 10000
    capacitor_recharge = 1000
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
    assert expected_failed_to_run_modules == matrix['Stability']['FailedToRunModules']


def test_empty_capacitor_amount():
    # Test to make sure what we DO raise an error
    module_list = [
        {
            'Amount': -40,
            'CycleTime': 4500,
        }
    ]  # Small Ancilliary Armor Repairer (no paste)

    capacitor_amount = None
    capacitor_recharge = 1000
    with raises(TypeError) as excinfo:
        run_simulation(module_list, capacitor_amount, capacitor_recharge)


def test_empty_recharge_amount():
    # Test to make sure what we DO raise an error
    module_list = [
        {
            'Amount': -40,
            'CycleTime': 4500,
        }
    ]  # Small Ancilliary Armor Repairer (no paste)

    capacitor_amount = 1000
    capacitor_recharge = None

    with raises(TypeError) as excinfo:
        run_simulation(module_list, capacitor_amount, capacitor_recharge)
