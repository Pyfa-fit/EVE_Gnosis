from math import sqrt, exp


class Formulas(object):
    def __init__(self):
        pass

    @staticmethod
    def capacitor_shield_tick(maximum_amount, current_amount, recharge_rate, end_time=1000, start_time=0):
        tau = recharge_rate / 5.0
        time_diff = start_time - end_time
        return ((1.0 + (sqrt(current_amount / maximum_amount) - 1.0) * exp(time_diff / tau)) ** 2) * maximum_amount

    @staticmethod
    def capacitor_shield_regen_matrix(capacitor_amount, capacitor_time):
        regen_matrix = []
        percent = 0
        while percent < 1:
            current_amount = capacitor_amount * percent
            tick_amount = Formulas.capacitor_shield_tick(capacitor_amount, current_amount, capacitor_time)
            regen_matrix.append(
                {
                    'Percent': percent,
                    'CapacitorAmountPostTick': tick_amount,
                    'DeltaAmount': tick_amount - current_amount
                }
            )
            percent += .01

        regen_matrix.append(
            {
                'Percent': 1,
                'CapacitorAmountPostTick': capacitor_amount,
                'DeltaAmount': 0
            }
        )

        return regen_matrix
