from simulations.capacitor import Capacitor
from formulas.formulas import Formulas

module_list = []

capacitor_amount = 375
capacitor_recharge = 105468.75

module_list.append(
    {
        'Amount': 10,
        'CycleTime': 2500,
        'Charges': False,
        'ReloadTime': False,
    }
) # Small T2 Nos

module_list.append(
    {
        'Amount': -1.5,
        'CycleTime': 5000,
        'Charges': False,
        'ReloadTime': False,
    }
) # J5b Enduring Warp Scrambler

module_list.append(
    {
        'Amount': -1.5,
        'CycleTime': 5000,
        'Charges': False,
        'ReloadTime': False,
    }
) # X5 Enduring Statis Webifier

module_list.append(
    {
        'Amount': -40,
        'CycleTime': 4500,
        'Charges': False,
        'ReloadTime': False,
    }
) # Small Ancilliary Armor Repairer

module_list.append(
    {
        'Amount': -10.5,
        'CycleTime': 5000,
        'Charges': False,
        'ReloadTime': False,
    }
) # Reactive Armor Hardener

return_value = Capacitor.CapacitorTimeSimulator(module_list, capacitor_amount, capacitor_recharge)
return_matrix = Formulas.capacitor_shield_regen_matrix(capacitor_amount, capacitor_recharge)
pass # Add break here if you want to see anything.


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
Rocket Launcher II
Small Energy Nosferatu II

Small Anti-Thermal Pump II
Small Auxiliary Nano Pump II
'''
