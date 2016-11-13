from gnosis.simulations.capacitor import capacitor
from gnosis.formulas.formulas import formulas
import pytest
import operator

#from tests.restriction_tracker.restriction_testcase import RestrictionTestCase


"""Check functionality of booster slot index restriction"""

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
            'Charges': False,
            'ReloadTime': False,
        }
    )  # Small T2 Nos

    module_list.append(
        {
            'Amount': -1.5,
            'CycleTime': 5000,
            'Charges': False,
            'ReloadTime': False,
        }
    )  # J5b Enduring Warp Scrambler

    module_list.append(
        {
            'Amount': -1.5,
            'CycleTime': 5000,
            'Charges': False,
            'ReloadTime': False,
        }
    )  # X5 Enduring Statis Webifier

    module_list.append(
        {
            'Amount': -40,
            'CycleTime': 4500,
            'Charges': False,
            'ReloadTime': False,
        }
    )  # Small Ancilliary Armor Repairer

    module_list.append(
        {
            'Amount': -10.5,
            'CycleTime': 5000,
            'Charges': False,
            'ReloadTime': False,
        }
    )  # Reactive Armor Hardener

    return module_list


def capacitor_amount():
    capacitor_amount = 375
    return capacitor_amount

def capacitor_recharge():
    capacitor_recharge = 105468.75
    return capacitor_recharge

def simulation_matrix():
    simulation_matrix = capacitor.capacitor_time_simulator(build_module_list(),
                                                           capacitor_amount(),
                                                           capacitor_recharge())
    return simulation_matrix

def regen_matrix():
    regen_matrix = formulas.capacitor_shield_regen_matrix(capacitor_amount(), capacitor_recharge())
    return regen_matrix

def test_peak_capacitor_regen():
    # Check that the peak capacitor regen is the expected delta and percent
    expected_capacitor_delta = 8.887120876962797
    expected_capacitor_percent = 0.24
    high_water_percent = 0
    high_water_delta = 0
    matrix = regen_matrix()
    for item in matrix:
        if high_water_delta < item['DeltaAmount']:
            high_water_percent = item['Percent']
            high_water_delta = item['DeltaAmount']

    assert expected_capacitor_delta == high_water_delta
    assert expected_capacitor_percent == high_water_percent


