from EVE_Gnosis.formulas.formulas import Formulas
from EVE_Gnosis.simulations.capacitor import Capacitor


def build_module_list():
    module_list = []

    '''
    Note that not all modules effect cap.  Even though the full fit is below,most of the modules have no impact on cap.

    [Tengu, Ebag Trescientas's RegenGu]

    Capacitor Flux Coil II
    Damage Control II
    Power Diagnostic System II
    Power Diagnostic System II
    Power Diagnostic System II

    10MN Monopropellant Enduring Afterburner
    Caldari Navy Warp Scrambler
    Gist A-Type EM Ward Field
    Gistum C-Type Adaptive Invulnerability Field
    Pith X-Type X-Large Shield Booster
    Republic Fleet Large Cap Battery

    Rapid Light Missile Launcher II, Caldari Navy Scourge Light Missile
    Rapid Light Missile Launcher II, Caldari Navy Scourge Light Missile
    Rapid Light Missile Launcher II, Caldari Navy Scourge Light Missile
    Rapid Light Missile Launcher II, Caldari Navy Scourge Light Missile
    Rapid Light Missile Launcher II, Caldari Navy Scourge Light Missile

    Medium Capacitor Control Circuit I
    Medium Capacitor Control Circuit II
    Medium Capacitor Control Circuit II

    Tengu Defensive - Amplification Node
    Tengu Electronics - Dissolution Sequencer
    Tengu Engineering - Capacitor Regeneration Matrix
    Tengu Offensive - Accelerated Ejection Bay
    Tengu Propulsion - Fuel Catalyst
    '''
    # RegenGu Modules
    module_list.append(
        {
            'Amount': -15,
            'CycleTime': 7500,
        }
    )  # 10mn Monopropellant Enduring Afterburner

    module_list.append(
        {
            'Amount': -3,
            'CycleTime': 5000,
        }
    )  # Caldari Navy Warp Scrambler

    module_list.append(
        {
            'Amount': -1.5,
            'CycleTime': 5000,
        }
    )  # X5 Enduring Statis Webifier

    module_list.append(
        {
            'Amount': -18,
            'CycleTime': 12000,
            'DelayTime': 6000,  # We want to stagger the two resist modules, so delay 6 seconds
        }
    )  # Gist A-Type EM Ward Field

    module_list.append(
        {
            'Amount': -32,
            'CycleTime': 12000,
        }
    )  # Gistum C-Type Adaptive Invulnerability Field

    module_list.append(
        {
            'Amount': -360,
            'CycleTime': 4000,
        }
    )  # Pith X-Type X-Large Shield Booster

    return module_list


def capacitor_amount():
    value = 4653.6525
    return value


def capacitor_recharge():
    value = 60771.9922442
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
    expected_capacitor_percent = 0.23
    expected_capacitor_delta = 191.33109953033863

    peak = regen_peak()

    assert expected_capacitor_percent == peak['PeakPercent']
    assert expected_capacitor_delta == peak['PeakDelta']


def test_simulation():
    expected_cached_run_count = 390
    expected_low_water_mark = 3153.2261050206575
    expected_time = 540000
    expected_capacitor_tick_0_percent = 0.91
    expected_capacitor_tick_0_time = 0
    expected_capacitor_tick_7_percent = 0.78
    expected_capacitor_tick_7_time = 12000
    expected_capacitor_tick_8_percent = 0.82
    expected_capacitor_tick_8_time = 15000
    expected_capacitor_tick_max_run_percent = 0.68
    expected_capacitor_tick_max_run_time = 728000

    matrix = simulation_matrix()

    cached_runs_count = 0
    for _ in matrix['Cached Runs']:
        cached_runs_count += 1

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
