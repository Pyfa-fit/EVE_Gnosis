class AdaptiveArmorHardener:
    def __init__(self):
        pass

    @staticmethod
    def run_cycle(resistances, damage_pattern, adaptive_pattern=None, adjust_amount=6):
        # If an adaptive pattern isn't passed in, set to a default of 15
        if not adaptive_pattern:
            adaptive_pattern = {}
            for _ in damage_pattern:
                adaptive_pattern[_] = 15

        # Reset applied damage to 0
        applied_damage = {}
        for applied_damage_type, applied_damage_amount in applied_damage:
            applied_damage[applied_damage_type] = 0

        # Apply damage tuple to current resists
        for _ in damage_pattern:
            applied_damage[_] = (1 - resistances[_]) * damage_pattern[_]

        # Sort applied damage tuple
        applied_damage = sorted(applied_damage.items(),
                                key=lambda x: (x[1], x[0])
                                )

        # Get how many incoming damage types we have
        count_damage_types = len([{type: amount} for type, amount in applied_damage if amount])

        # Adjust our resists
        transferred_amount = 0
        fail_to_steal = False
        for idx, single_applied_damage in enumerate(applied_damage):
            key, value = single_applied_damage
            if idx <= 1:
                if adaptive_pattern[key] == 0:
                    fail_to_steal = True
                elif adaptive_pattern[key] > adjust_amount:
                    transferred_amount += adjust_amount
                    adaptive_pattern[key] -= adjust_amount
                else:
                    transferred_amount += adaptive_pattern[key]
                    adaptive_pattern[key] = 0
            elif 1 < idx <= (len(applied_damage) - 2) and count_damage_types == 1 and fail_to_steal:
                # We failed to steal resist from the bottom two resists.
                # If we only have 1 damage type, we're allowed to steal from the next resist.
                if adaptive_pattern[key] > adjust_amount:
                    transferred_amount += adjust_amount
                    adaptive_pattern[key] -= adjust_amount
                else:
                    transferred_amount += adaptive_pattern[key]
                    adaptive_pattern[key] = 0
            elif idx >= (len(applied_damage) - 2) and count_damage_types >= 2:
                adaptive_pattern[key] += transferred_amount / 2
            elif idx >= (len(applied_damage) - 1) and count_damage_types == 1:
                adaptive_pattern[key] += transferred_amount
            else:
                continue

        return {'AppliedDamage': applied_damage, 'AdaptivePattern': adaptive_pattern}
