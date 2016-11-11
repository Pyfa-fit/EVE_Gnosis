from math import sqrt, exp

# noinspection PyPackageRequirements
from simulations.capacitor import Capacitor

test = exp(0)

MaximumAmount = 4653.6525
tau = 60771.9922442 / 5.0

percent = 0

while percent < 100:
    StartingAmount = MaximumAmount * (percent / 100)
    EndingAmount = ((1.0 + (sqrt(StartingAmount / MaximumAmount) - 1.0) * exp((0 - 1000) / tau)) ** 2) * MaximumAmount
    print(str(percent) + "% " + str(EndingAmount - StartingAmount))
    percent += 1

pass

# capacitor amount, capacitor regen time
# modifier amount, cycle time

module_list = []
# module_list.append([Amount (GJ), CycleTime (S), NumCharges (Count), ReloadTime (S))

i = 0
while i < 5:
    module_list.append(
        {
            'Amount': -324,
            'CycleTime': 12,
        }
    )
    i += 1
    # Add 5 Curse T2 medium neuts

'''
module_list.append(
    {
        'Amount': 3100,
        'CycleTime': 12,
        'Charges': 1,
        'ReloadTime': 10,
    }
) # Heavy Cap Booster with 3200 charges
'''

capacitor_amount = 7439.0625
capacitor_recharge = 528

return_value = Capacitor.capacitor_time_simulator(module_list, capacitor_amount, capacitor_recharge)
