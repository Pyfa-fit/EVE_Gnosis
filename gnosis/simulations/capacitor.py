import operator

from gnosis.formulas.formulas import Formulas


class Capacitor(object):
    def __init__(self):
        pass

    @staticmethod
    def capacitor_time_simulator(module_list, max_capacitor_amount, capacitor_time):
        run_tick = True
        low_water_mark = current_capcitor_amount = max_capacitor_amount
        low_water_mark_elapsed_time = total_time_count = time_count = 0

        # We have to handle the first run special, because there is no reload.
        module_timers = []
        # print("First Run")
        for i, module in enumerate(module_list):
            if module['Amount']:
                module_time = 0
                try:
                    if module['DelayTime']:
                        # We have a delay before we need to run this, so we're going to not run it right away.
                        # This can be used to stagger modules, so we don't start them all at the same time.
                        # Can also use this to not run specific modules right away.
                        module_time += module['DelayTime']
                except KeyError:
                    # Key doesn't exist, do nothing
                    pass

                try:
                    if module['Charges']:
                        # Add our chargese so we can properly count down.
                        new_charges = module['Charges']
                    else:
                        new_charges = False
                except KeyError:
                    # Key doesn't exist, do nothing
                    new_charges = False

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

        # print("Full Run")
        cache_runs_dict = []
        while run_tick:
            module_timers = sorted(module_timers, key=operator.itemgetter('Time'))

            # Get the time until the next module runs.
            elapsed_time = module_timers[0]['Time']
            total_time_count += elapsed_time
            # print("Seconds elapsed: " + str(elapsed_time))

            # Run our capacitor regen
            new_capacitor_amount = Formulas.capacitor_shield_tick(max_capacitor_amount, current_capcitor_amount,
                                                                  capacitor_time, elapsed_time)

            delta_capacitor_regen = new_capacitor_amount - current_capcitor_amount
            current_capcitor_amount = new_capacitor_amount

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

            # print ("Current Capacitor: " + str(current_capcitor_amount) +
            #       " Percent: " + str(current_capcitor_amount/max_capacitor_amount))

            cache_runs_dict.append(
                {
                    'Current Time': total_time_count,
                    'Current Capacitor': current_capcitor_amount,
                    'Capacitor Percentage': round(current_capcitor_amount / max_capacitor_amount, 2),
                    'Capacitor Regen Delta': delta_capacitor_regen,
                }
            )

            if low_water_mark > current_capcitor_amount:
                low_water_mark = current_capcitor_amount
                low_water_mark_elapsed_time = total_time_count
                time_count = 0
                # print("Low water mark: " + str(low_water_mark) + " Seconds: " + str(total_time_count / 1000))
            elif current_capcitor_amount == 0:
                # We've run out of cap, go ahead and break out of the loop.
                break
            else:
                time_count += 1

                if time_count > 100:
                    # We have performed 100 loops since the last low water mark was found.
                    # Break out as we are highly likely to be cap stable here.
                    break
                else:
                    continue

        stability_dict = {
            'Time': low_water_mark_elapsed_time,
            'LowWaterMark': low_water_mark
        }
        return {'Stability': stability_dict, 'Cached Runs': cache_runs_dict}
