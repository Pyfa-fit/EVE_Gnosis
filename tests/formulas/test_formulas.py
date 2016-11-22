from EVE_Gnosis.formulas.formulas import Formulas


def get_values_from_matrix(value_matrix, percent):
    for values in value_matrix:
        if values['Percent'] == percent:
            return {'Percent': values['Percent'],
                    'CapacitorAmountPostTick': values['CapacitorAmountPostTick'],
                    'DeltaAmount': values['DeltaAmount']}

    return False


"""
Test capacitor_shield_tick formula.
    capacitor_shield_tick(maximum_amount, current_amount, recharge_rate, end_time=1000, start_time=0)

These are simply some sanity checks to make sure that something doesn't change along the way.
These are not real numbers or validated against in game numbers.

Test name format: capacitor_shield_tick_[maximum]_[current]_[recharge]_[end]_[start]
Where [name] is the number being passed in
[end] and [start] are optional.

Example: test_capacitor_shield_tick_100_0_10000
Example: test_capacitor_shield_tick_100_0_10000_1000_0
"""


def test_capacitor_shield_tick_100_0_10000():
    # Check 1 tick
    expected_return = 15.481812174617549
    tick = Formulas.capacitor_shield_tick(100, 0, 10000)
    assert tick == expected_return


def test_capacitor_shield_tick_100_25_10000():
    # Check 1 tick
    expected_return = 48.543920058022714
    tick = Formulas.capacitor_shield_tick(100, 25, 10000)
    assert tick == expected_return


def test_capacitor_shield_tick_100_50_10000():
    # Check 1 tick
    expected_return = 67.62616322697144
    tick = Formulas.capacitor_shield_tick(100, 50, 10000)
    assert tick == expected_return


def test_capacitor_shield_tick_100_75_10000():
    # Check 1 tick
    expected_return = 84.40837384263237
    tick = Formulas.capacitor_shield_tick(100, 75, 10000)
    assert tick == expected_return


def test_capacitor_shield_tick_100_0_10000_10000():
    # Check 10 ticks
    expected_return = 98.65695059315915
    tick = Formulas.capacitor_shield_tick(100, 0, 10000, 10000)
    assert tick == expected_return


def test_capacitor_shield_tick_100_0_10000_20000_20000():
    # Check 10 ticks, should be same results as above
    expected_return = 98.65695059315915
    tick = Formulas.capacitor_shield_tick(100, 0, 10000, 20000, 10000)
    assert tick == expected_return


def test_capacitor_shield_tick_100000_0_10000000():
    # Check 1 tick
    expected_return = 0.024987503645050178
    tick = Formulas.capacitor_shield_tick(100000, 0, 10000000)
    assert tick == expected_return


def test_capacitor_shield_tick_100000_0_10000000_10000():
    # Check 10 ticks
    expected_return = 2.4875363803426804
    tick = Formulas.capacitor_shield_tick(100000, 0, 10000000, 10000)
    assert tick == expected_return


def test_capacitor_shield_tick_100000_0_10000000_20000_10000():
    # Check 10 ticks, should be same results as above
    expected_return = 2.4875363803426804
    tick = Formulas.capacitor_shield_tick(100000, 0, 10000000, 20000, 10000)
    assert tick == expected_return


def test_capacitor_shield_tick_37337_0_8008135():
    # Check 1 tick
    expected_return = 0.014546064622025907
    tick = Formulas.capacitor_shield_tick(37337, 0, 8008135)
    assert tick == expected_return


def test_capacitor_shield_tick_37337_0_8008135_10000():
    # Check 10 ticks
    expected_return = 1.4464601872474037
    tick = Formulas.capacitor_shield_tick(37337, 0, 8008135, 10000)
    assert tick == expected_return


def test_capacitor_shield_tick_37337_0_8008135_20000_10000():
    # Check 10 ticks, should be same results as above
    expected_return = 1.4464601872474037
    tick = Formulas.capacitor_shield_tick(37337, 0, 8008135, 20000, 10000)
    assert tick == expected_return


def test_capacitor_shield_tick_37337_0_8008135_20000():
    # Check 10 ticks, should NOT be same results as above
    expected_return = 1.4464601872474037
    tick = Formulas.capacitor_shield_tick(37337, 0, 8008135, 20000)
    assert tick != expected_return


"""
Test capacitor_shield_regen_matrix formula.
    capacitor_shield_regen_matrix(capacitor_amount, capacitor_time)

These are simply some sanity checks to make sure that something doesn't change along the way.
These are not real numbers or validated against in game numbers.

Test name format: capacitor_shield_regen_matrix_[amount]_[time]
Where [name] is the number being passed in
[end] and [start] are optional.

Example: capacitor_shield_regen_matrix_1000_100
"""


def test_capacitor_shield_regen_matrix_1000_100000_count_items():
    return_matrix = Formulas.capacitor_shield_regen_matrix(1000, 100000)
    count = 0
    for _ in return_matrix:
        count += 1

    assert count == 101


def test_capacitor_shield_regen_matrix_1000_100000_percent_0():
    expected_percent = 0
    expected_amount = 2.378569034531554
    expected_delta = 2.378569034531554
    return_matrix = Formulas.capacitor_shield_regen_matrix(1000, 100000)
    return_value = get_values_from_matrix(return_matrix, expected_percent)
    assert expected_percent == return_value['Percent']
    assert expected_amount == return_value['CapacitorAmountPostTick']
    assert expected_delta == return_value['DeltaAmount']


def test_capacitor_shield_regen_matrix_1000_100000_percent_1():
    expected_percent = .01
    expected_amount = 20.70534450784202
    expected_delta = 10.705344507842021
    return_matrix = Formulas.capacitor_shield_regen_matrix(1000, 100000)
    return_value = get_values_from_matrix(return_matrix, expected_percent)
    assert expected_percent == return_value['Percent']
    assert expected_amount == return_value['CapacitorAmountPostTick']
    assert expected_delta == return_value['DeltaAmount']


def test_capacitor_shield_regen_matrix_1000_100000_percent_2():
    expected_percent = .02
    expected_amount = 33.59695834088194
    expected_delta = 13.59695834088194
    return_matrix = Formulas.capacitor_shield_regen_matrix(1000, 100000)
    return_value = get_values_from_matrix(return_matrix, expected_percent)
    assert expected_percent == return_value['Percent']
    assert expected_amount == return_value['CapacitorAmountPostTick']
    assert expected_delta == return_value['DeltaAmount']


def test_capacitor_shield_regen_matrix_1000_100000_percent_3():
    expected_percent = .03
    expected_amount = 45.59435402801404
    expected_delta = 15.594354028014038
    return_matrix = Formulas.capacitor_shield_regen_matrix(1000, 100000)
    return_value = get_values_from_matrix(return_matrix, expected_percent)
    assert expected_percent == return_value['Percent']
    assert expected_amount == return_value['CapacitorAmountPostTick']
    assert expected_delta == return_value['DeltaAmount']


def test_capacitor_shield_regen_matrix_1000_100000_percent_4():
    expected_percent = .04
    expected_amount = 57.128868341871666
    expected_delta = 17.128868341871666
    return_matrix = Formulas.capacitor_shield_regen_matrix(1000, 100000)
    return_value = get_values_from_matrix(return_matrix, expected_percent)
    assert expected_percent == return_value['Percent']
    assert expected_amount == return_value['CapacitorAmountPostTick']
    assert expected_delta == return_value['DeltaAmount']


def test_capacitor_shield_regen_matrix_1000_100000_percent_5():
    expected_percent = .05
    expected_amount = 68.36757594988963
    expected_delta = 18.367575949889627
    return_matrix = Formulas.capacitor_shield_regen_matrix(1000, 100000)
    return_value = get_values_from_matrix(return_matrix, expected_percent)
    assert expected_percent == return_value['Percent']
    assert expected_amount == return_value['CapacitorAmountPostTick']
    assert expected_delta == return_value['DeltaAmount']


def test_capacitor_shield_regen_matrix_1000_100000_percent_10():
    expected_percent = .1
    expected_amount = 122.20319196890358
    expected_delta = 22.203191968903596
    return_matrix = Formulas.capacitor_shield_regen_matrix(1000, 100000)
    return_value = get_values_from_matrix(return_matrix, expected_percent)
    assert expected_percent == return_value['Percent']
    assert expected_amount == return_value['CapacitorAmountPostTick']
    assert expected_delta == return_value['DeltaAmount']


def test_capacitor_shield_regen_matrix_1000_100000_percent_20():
    expected_percent = .2
    expected_amount = 224.84032466884372
    expected_delta = 24.840324668843692
    return_matrix = Formulas.capacitor_shield_regen_matrix(1000, 100000)
    return_value = get_values_from_matrix(return_matrix, expected_percent)
    assert expected_percent == return_value['Percent']
    assert expected_amount == return_value['CapacitorAmountPostTick']
    assert expected_delta == return_value['DeltaAmount']


def test_capacitor_shield_regen_matrix_1000_100000_percent_30():
    expected_percent = .3
    expected_amount = 324.6496913026625
    expected_delta = 24.649691302662404
    return_matrix = Formulas.capacitor_shield_regen_matrix(1000, 100000)
    return_value = get_values_from_matrix(return_matrix, expected_percent)
    assert expected_percent == return_value['Percent']
    assert expected_amount == return_value['CapacitorAmountPostTick']
    assert expected_delta == return_value['DeltaAmount']


def test_capacitor_shield_regen_matrix_1000_100000_percent_40():
    expected_percent = .4
    expected_amount = 422.99529851046753
    expected_delta = 22.995298510467364
    return_matrix = Formulas.capacitor_shield_regen_matrix(1000, 100000)
    return_value = get_values_from_matrix(return_matrix, expected_percent)
    assert expected_percent == return_value['Percent']
    assert expected_amount == return_value['CapacitorAmountPostTick']
    assert expected_delta == return_value['DeltaAmount']


def test_capacitor_shield_regen_matrix_1000_100000_percent_50():
    expected_percent = .5
    expected_amount = 520.4054827806675
    expected_delta = 20.405482780667285
    return_matrix = Formulas.capacitor_shield_regen_matrix(1000, 100000)
    return_value = get_values_from_matrix(return_matrix, expected_percent)
    assert expected_percent == return_value['Percent']
    assert expected_amount == return_value['CapacitorAmountPostTick']
    assert expected_delta == return_value['DeltaAmount']


def test_capacitor_shield_regen_matrix_1000_100000_percent_60():
    expected_percent = .6
    expected_amount = 617.1512072301639
    expected_delta = 17.15120723016355
    return_matrix = Formulas.capacitor_shield_regen_matrix(1000, 100000)
    return_value = get_values_from_matrix(return_matrix, expected_percent)
    assert expected_percent == return_value['Percent']
    assert expected_amount == return_value['CapacitorAmountPostTick']
    assert expected_delta == return_value['DeltaAmount']


def test_capacitor_shield_regen_matrix_1000_100000_percent_70():
    expected_percent = .7
    expected_amount = 713.3934363792446
    expected_delta = 13.393436379244122
    return_matrix = Formulas.capacitor_shield_regen_matrix(1000, 100000)
    return_value = get_values_from_matrix(return_matrix, expected_percent)
    assert expected_percent == return_value['Percent']
    assert expected_amount == return_value['CapacitorAmountPostTick']
    assert expected_delta == return_value['DeltaAmount']


def test_capacitor_shield_regen_matrix_1000_100000_percent_80():
    expected_percent = .8
    expected_amount = 809.2370475175403
    expected_delta = 9.23704751753985
    return_matrix = Formulas.capacitor_shield_regen_matrix(1000, 100000)
    return_value = get_values_from_matrix(return_matrix, expected_percent)
    assert expected_percent == return_value['Percent']
    assert expected_amount == return_value['CapacitorAmountPostTick']
    assert expected_delta == return_value['DeltaAmount']


def test_capacitor_shield_regen_matrix_1000_100000_percent_90():
    expected_percent = .90
    expected_amount = 904.7548886592236
    expected_delta = 4.75488865922307
    return_matrix = Formulas.capacitor_shield_regen_matrix(1000, 100000)
    return_value = get_values_from_matrix(return_matrix, expected_percent)
    assert expected_percent == return_value['Percent']
    assert expected_amount == return_value['CapacitorAmountPostTick']
    assert expected_delta == return_value['DeltaAmount']


def test_capacitor_shield_regen_matrix_1000_100000_percent_99():
    expected_percent = .99
    expected_amount = 990.4865401193317
    expected_delta = 0.486540119331039
    return_matrix = Formulas.capacitor_shield_regen_matrix(1000, 100000)
    return_value = get_values_from_matrix(return_matrix, expected_percent)
    assert expected_percent == return_value['Percent']
    assert expected_amount == return_value['CapacitorAmountPostTick']
    assert expected_delta == return_value['DeltaAmount']


def test_capacitor_shield_regen_matrix_1000_100000_percent_100():
    expected_percent = 1
    expected_amount = 1000
    expected_delta = 0
    return_matrix = Formulas.capacitor_shield_regen_matrix(1000, 100000)
    return_value = get_values_from_matrix(return_matrix, expected_percent)
    assert expected_percent == return_value['Percent']
    assert expected_amount == return_value['CapacitorAmountPostTick']
    assert expected_delta == return_value['DeltaAmount']
