from operator import itemgetter

from ..formulas.formulas import Formulas


class Capacitor:
    def __init__(self):
        pass

    @staticmethod
    def capacitor_time_simulator(module_list, max_capacitor_amount, capacitor_time, run_time=600000):
        run_tick = True
        failed_to_run_modules = False
        failed_to_run_modules_time = 0
        low_water_mark = current_capcitor_amount = max_capacitor_amount
        count_ticks = low_water_mark_elapsed_time = total_time_count = 0

        # We have to handle the first run special, because there is no reload.
        module_timers = []
        # print("First Run")
        for i, module in enumerate(module_list):
            if module['Amount'] is not None and module['CycleTime'] > 0:
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

        if module_timers:
            while run_tick:
                count_ticks += 1
                module_timers = sorted(module_timers, key=itemgetter('Time'))

                # Get the time until the next module runs.
                elapsed_time = module_timers[0]['Time']

                total_time_count += elapsed_time
                # print("Seconds elapsed: " + str(elapsed_time))

                # Run our capacitor regen
                new_capacitor_amount = Formulas.capacitor_shield_tick(max_capacitor_amount, current_capcitor_amount,
                                                                      capacitor_time, elapsed_time)

                delta_capacitor_regen = new_capacitor_amount - current_capcitor_amount
                current_capcitor_amount = new_capacitor_amount
                current_shield_repair = 0
                current_armor_repair = 0
                current_hull_repair = 0

                for i, module in enumerate(module_timers):
                    module_time = module['Time'] - elapsed_time

                    # Find our what percent we fire off the module at.
                    # Added so we can only fire off a module if the cap drops too low.
                    try:
                        percent_fire = module_list[module['ID']]['FireAtPercent']
                    except KeyError:
                        percent_fire = False

                    # See if the module is projected or not
                    try:
                        projected = module_list[module['ID']]['Projected']
                    except KeyError:
                        projected = False

                    if ((current_capcitor_amount / max_capacitor_amount) > percent_fire and
                                percent_fire is not False) and module_time <= 0:
                        # This module should only run if our cap is too low (below a certain percentage.
                        # If we're above that percentage, add 1 second to our time so we check it next tick.
                        module_time += 1000
                    elif module_list[module['ID']]['Amount'] < 0 and \
                                    (current_capcitor_amount + module_list[module['ID']]['Amount']) < 0 and \
                                    not projected:
                        # We don't have enough cap to run this module.  Delay by 1 second.
                        # Only apply to local modules
                        module_time += 1000
                        failed_to_run_modules = True
                        if not failed_to_run_modules_time:
                            failed_to_run_modules_time = total_time_count

                    if module_time <= 0:
                        # Time to run the module
                        current_capcitor_amount += module_list[module['ID']]['Amount']
                        module_time = module_list[module['ID']]['CycleTime']
                        # print("Applying cap modification: " + str(module_list[module['ID']]['Amount']))

                        # Populate the mount of reps we get each tick
                        try:
                            if module_list[module['ID']]['ShieldRepair']:
                                current_shield_repair += module_list[module['ID']]['ShieldRepair']
                        except KeyError:
                            current_shield_repair += 0

                        try:
                            if module_list[module['ID']]['ArmorRepair']:
                                current_armor_repair += module_list[module['ID']]['ArmorRepair']
                        except KeyError:
                            current_armor_repair += 0

                        try:
                            if module_list[module['ID']]['HullRepair']:
                                current_hull_repair += module_list[module['ID']]['HullRepair']
                        except KeyError:
                            current_hull_repair += 0

                        # Sanity check so we don't go over our total capacitor size, and we don't go under 0.
                        if current_capcitor_amount > max_capacitor_amount:
                            current_capcitor_amount = max_capacitor_amount
                        elif current_capcitor_amount < 0:
                            current_capcitor_amount = 0

                        # Find our reload time, set to False if doesn't exist
                        try:
                            reload_time = module_list[module['ID']]['ReloadTime']
                        except KeyError:
                            reload_time = False

                        # Find how many charges we have, and subtract 1 if we have more than 0
                        try:
                            new_charges = module['Charges']
                            if new_charges is not False and new_charges > 0:
                                new_charges = module['Charges'] - 1
                        except KeyError:
                            new_charges = False

                        if not new_charges:
                            try:
                                module_time += module_list[module['ID']]['ReactivationDelay']
                            except KeyError:
                                # Key doesn't exist, this is okay
                                pass

                        if new_charges <= 0 and new_charges is not False and reload_time:
                            # If we are out of charges, or charges is false and we have a reload time,
                            # then delay the next execution by the reload_time
                            module_time += reload_time
                            module_timers[i]['Charges'] = module_list[module['ID']]['Charges']
                        elif new_charges and new_charges is not False and reload_time:
                            # Reduce our
                            module_timers[i]['Charges'] = new_charges

                    # Set new values
                    module_timers[i]['Time'] = module_time

                cache_runs_dict.append(
                    {
                        'Current Time': total_time_count,
                        'Current Capacitor': current_capcitor_amount,
                        'Capacitor Percentage': round(current_capcitor_amount / max_capacitor_amount, 2),
                        'Capacitor Regen Delta': delta_capacitor_regen,
                        'Shield Reps': current_shield_repair,
                        'Armor Reps': current_armor_repair,
                        'Hull Reps': current_hull_repair,
                    }
                )

                if low_water_mark > current_capcitor_amount:
                    # Found a new capacitor low water mark.  Mark it, so we can report it later.
                    low_water_mark = current_capcitor_amount
                    low_water_mark_elapsed_time = total_time_count

                if total_time_count > run_time:
                    # We ran for the allotted amount of time.
                    break
        else:
            low_water_mark_elapsed_time = 0
            low_water_mark = max_capacitor_amount

        stability_dict = {
            'LowWaterMarkTime': low_water_mark_elapsed_time,
            'LowWaterMark': low_water_mark,
            'FailedToRunModules': failed_to_run_modules,
            'FailedToRunModulesTime': failed_to_run_modules_time,
            'RunTime': run_time,
        }
        return {'Stability': stability_dict, 'Cached Runs': cache_runs_dict}
