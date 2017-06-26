from math import sqrt, exp


class Formulas(object):
    def __init__(self):
        pass

    @staticmethod
    def capacitor_shield_tick(maximum_amount, current_amount, recharge_rate, end_time=1000, start_time=0):
        """
        :param maximum_amount:  The size of the capacitor/shield in gigajoules (GJ)
        :param current_amount:  The current level of the capacitor/shield in gigajoules (GJ)
        :param recharge_rate:   Recharge time listed for the capacitor/shield, in milliseconds
        :param end_time:        The length of time that we are running, in milliseconds
        :param start_time:      The length of time that we are starting, in milliseconds (unlikely to be used)
        :return:                Returns the new capacitor amount in gigajoules (GJ)

        This function assumes nothing else is at play to change the values while it's being calculated.
        Formula validated and confirmed by CCP Larrikin. <3
        """
        tau = recharge_rate / 5.0
        time_diff = start_time - end_time
        new_amount = (
                         (1.0 + (sqrt(current_amount / maximum_amount) - 1.0) * exp(time_diff / tau)) ** 2
                     ) * maximum_amount

        if new_amount > maximum_amount:
            # Sanity check and make sure we don't return more than our maximum somehow.
            return maximum_amount
        else:
            return new_amount

    @staticmethod
    def capacitor_shield_regen_matrix(capacitor_amount, capacitor_time):
        """
        :param capacitor_amount:  The size of the capacitor/shield in gigajoules (GJ)
        :param capacitor_time:    Recharge time listed for the capacitor/shield, in milliseconds
        :return:                  A matrix with the percent, capacitor amount after the tick, and the delta

        This function assumes nothing else is at play to change the values while it's being calculated.
        Most useful to determine the percentage point that gives the most cap, or for graphing it.
        """
        regen_matrix = []
        percent = 0
        while percent < 1:
            current_amount = capacitor_amount * percent
            tick_amount = Formulas.capacitor_shield_tick(capacitor_amount, current_amount, capacitor_time)
            regen_matrix.append(
                {
                    'Percent': round(percent, 2),
                    'AmountPostTick': tick_amount,
                    'DeltaAmount': tick_amount - current_amount
                }
            )
            percent += .01

        regen_matrix.append(
            {
                'Percent': 1,
                'AmountPostTick': capacitor_amount,
                'DeltaAmount': 0
            }
        )

        return regen_matrix

    @staticmethod
    def stacking_penalty(value, depth):
        """
        :param value:             The value to apply the stacking penalty to
        :param depth:             How many stacking penalties to apply
        :return:                  Value after stacking penalties have been applied.
        """
        current_effectiveness = 1 / exp(((depth - 1) / 2.67) ** 2.0)
        new_value = 1 + ((value * current_effectiveness) / 100)

        return new_value
