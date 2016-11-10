import heapq
import time
import copy
from formulas.formulas import Formulas
import operator


class Capacitor(object):
    def __init__(self):
        pass

    @staticmethod
    def CapacitorTimeSimulator(module_list, max_capacitor_amount, capacitor_time):
        run_tick = True
        low_water_mark = current_capcitor_amount = max_capacitor_amount
        low_water_mark_elapsed_time = total_time_count = time_count = 0

        # We have to handle the first run special, because there is no reload.
        module_timers = []
        print("First Run")
        for i, module in enumerate(module_list):
            if module['Amount']:
                if module['Charges']:
                    # If we have a module with charges, don't run it right away.
                    # It's most likely a cap booster, and that would be a waste of a charge.
                    module_time = module['CycleTime']
                    new_charges = module['Charges']
                else:
                    # Regular module without charges.
                    # Neut, Nos, remote Cap Trans.
                    # Go ahead and apply to the capacitor
                    current_capcitor_amount += module['Amount']
                    module_time = module['CycleTime']
                    new_charges = False

                    # Sanity check so we don't go over our total capacitor size, and we don't go under 0.
                    if current_capcitor_amount > max_capacitor_amount:
                        current_capcitor_amount = max_capacitor_amount
                    elif current_capcitor_amount < 0:
                        current_capcitor_amount = 0

                # Populate a dict with the module IDs so we can create timers.
                module_timers.append(
                    {
                        'ID': i,
                        'Time': module_time,
                        'Charges': new_charges
                    }
                )
            else:
                # Module has nothing to add/drain. Why is it here?
                pass

        print("Full Run")
        while run_tick:
            module_timers = sorted(module_timers, key=operator.itemgetter('Time'))

            # Get the time until the next module runs.
            elapsed_time = module_timers[0]['Time']
            total_time_count += elapsed_time
            # print("Seconds elapsed: " + str(elapsed_time))

            # Run our capacitor regen
            current_capcitor_amount = Formulas.capacitor_shield_tick(max_capacitor_amount, current_capcitor_amount,
                                                                     capacitor_time, elapsed_time)

            for i, module in enumerate(module_timers):
                module_time = module['Time'] - elapsed_time

                if module_time <= 0:
                    # Time to run the module
                    current_capcitor_amount += module_list[module['ID']]['Amount']
                    module_time = module_list[module['ID']]['CycleTime']
                    # print("Applying cap modification: " + str(module_list[module['ID']]['Amount']))

                    # Sanity check so we don't go over our total capacitor size, and we don't go under 0.
                    if current_capcitor_amount > max_capacitor_amount:
                        current_capcitor_amount = max_capacitor_amount
                    elif current_capcitor_amount < 0:
                        current_capcitor_amount = 0

                    testID = module['ID']
                    testCharges = module['Charges']
                    testListCharges = module_list[module['ID']]['Charges']
                    if module['Charges']:
                        new_charges = module['Charges'] - 1

                        if new_charges <= 0:
                            try:
                                if module_list[module['ID']]['ReloadTime']:
                                    module_time += module_list[module['ID']]['ReloadTime']

                                new_charges = module_list[module['ID']]['Charges']
                            except KeyError:
                                # Attribute doesn't exist, do nothing
                                pass

                        module_timers[i]['Charges'] = new_charges

                # Set new values
                module_timers[i]['Time'] = module_time

            # print ("Current Capacitor: " + str(current_capcitor_amount) + " Percent: " + str(current_capcitor_amount/max_capacitor_amount))

            if low_water_mark > current_capcitor_amount:
                low_water_mark = current_capcitor_amount
                low_water_mark_elapsed_time = total_time_count
                time_count = 0
                # print("Low water mark: " + str(low_water_mark) + " Seconds: " + str(total_time_count / 1000))
            else:
                time_count += 1

                if time_count > 100:
                    break
                else:
                    continue

        return_dict = [{
            'Time': low_water_mark_elapsed_time,
            'LowWaterMark': low_water_mark
        }]
        return return_dict
