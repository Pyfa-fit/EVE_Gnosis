from capacitor.capsim import CapSimulator

from simulations.capacitor import Capacitor


# capacitor amount, capacitor regen time
# modifier amount, cycle time

module_list = []
#module_list.append([Amount (GJ), CycleTime (S), NumCharges (Count), ReloadTime (S))

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
        'ReloadTime': 60,
    }
) # Heavy Cap Booster with 3200 charges
'''

capacitor_amount = 7439.0625
capacitor_recharge = 528

return_value = Capacitor.CapacitorTimeSimulator(module_list, capacitor_amount, capacitor_recharge)