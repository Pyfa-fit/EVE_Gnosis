import heapq
from math import sqrt, exp
import time
import copy


class Capacitor(object):

    def __init__(self):
        pass

    def CapacitorTimeSimulator(module_list, capacitor_amount, capacitor_time):
        pass

        run_tick = True
        current_capcitor = capacitor_amount
        time_count = 0

        module_list_orig = copy.deepcopy(module_list)
        while run_tick:
            time_count += 1

            print ("Current Capacitor: ", current_capcitor)

            if current_capcitor < capacitor_amount:
                if current_capcitor < (capacitor_amount-current_capcitor):
                    pass
                    #current_capcitor += capacitor_amount
                else:
                    pass
                    #current_capcitor = capacitor_amount

            for i, module in enumerate(module_list):
                # module_list.append([Amount (GJ), CycleTime (S), NumCharges (Count), ReloadTime (S))

                '''
                try:
                    if module_list[i]['Charges'] > 0:
                        print ("Number of charges: ", module['Charges'])
                        module_list[i]['Charges'] -= 1
                        skip_boost = False
                    else:
                        module_list[i]['ReloadTime'] -= 1
                        print("Reload time: ", module_list[i]['ReloadTime'])
                        skip_boost = True
                except KeyError:
                    # Key doesn't exist, don't do anything
                    pass

                try:
                    if module_list[i]['ReloadTime'] == 0:
                        module_list[i]['Charges'] = module_list_orig[i]['Charges']
                        module_list[i]['ReloadTime'] = module_list_orig[i]['ReloadTime']
                        print('Module reloaded: ',i, module_list[i]['Charges'], module_list[i]['ReloadTime'])
                except KeyError:
                    # Key doesn't exist, don't do anything
                    pass
                '''

                if (time_count/module['CycleTime']).is_integer():
                    current_capcitor += module['Amount']
                    print ("Module: ", module['Amount'])



            print ("Final Capacitor: ", current_capcitor)

            if time_count > 130:
                break