# noinspection PyPackageRequirements
from gnosis.simulations.capacitor import Capacitor
from gnosis.formulas.formulas import Formulas
from datetime import datetime

module_list = []

capacitor_amount = 4653.6525
capacitor_recharge = 60771.9922442

print("Start: ", datetime.now().time())

# ________________________________________________________
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

return_value = Capacitor.capacitor_time_simulator(module_list, capacitor_amount, capacitor_recharge)
return_matrix = Formulas.capacitor_shield_regen_matrix(capacitor_amount, capacitor_recharge)
pass  # Add break here if you want to see anything.

print("Base calc time: ", datetime.now().time())

'''
Note that not all modules effect cap.  Even though the full fit is below,most of the modules have no impact on cap.

[Tengu, Ebag Trescientas's Tengu]

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

'''
Now add a Curse and see how the cap holds up.
'''

i = 0
delay_time = 0
cycle_time = 12000
while i < 4:
    module_list.append(
        {
            'Amount': -324,
            'CycleTime': cycle_time,
            'DelayTime': delay_time,
        }
    )  # Add 4 Curse powered Medium Energy Neutralizer II
    i += 1
    delay_time += cycle_time / 4  # Add a delay to stagger our neuts

module_list.append(
    {
        'Amount': -64.8,
        'CycleTime': 5000,
    }
)  # Medium Energy Nosferatu II

return_value_two = Capacitor.capacitor_time_simulator(module_list, capacitor_amount, capacitor_recharge)
return_matrix_two = Formulas.capacitor_shield_regen_matrix(capacitor_amount, capacitor_recharge)

print("End time: ", datetime.now().time())  # Add break here if you want to see anything.

'''
[Curse, Shield Std]

Damage Control II
Power Diagnostic System II
Power Diagnostic System II
Reactor Control Unit II

10MN Monopropellant Enduring Afterburner
Adaptive Invulnerability Field II
Large Shield Extender II
Large Shield Extender II
Large Shield Extender II
EM Ward Amplifier II

Medium Energy Neutralizer II
Medium Energy Neutralizer II
Medium Energy Neutralizer II
Medium Energy Neutralizer II
Medium Energy Nosferatu II

Medium Core Defense Field Extender I
Medium Core Defense Field Extender I

'''
