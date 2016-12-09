class AdaptiveArmorHardener:
    def __init__(self):
        pass

    @staticmethod
    def run_cycle(resistances, damage_pattern, adaptive_pattern=None, adjust_amount=6):

        if adaptive_pattern is None:
            adaptive_pattern = {}
        applied_damage = {}

        # If an adaptive pattern isn't passed in, set to a default of 15
        if not adaptive_pattern:
            for _ in damage_pattern:
                adaptive_pattern[_] = 15

        # Reset applied damage back to 0
        for applied_damage_type, applied_damage_amount in applied_damage:
            applied_damage[applied_damage_type] = 0

        # Apply damage tuple to current resists
        for _ in damage_pattern:
            applied_damage[_] = resistances[_] * damage_pattern[_]

        # Sort applied damage tuple
        applied_damage = sorted(applied_damage.items(),
                                key=lambda x: (x[1], x[0])
                                )

        # Adjust our resists
        transferred_amount = 0
        for idx, single_applied_damage in enumerate(applied_damage):
            key, value = single_applied_damage
            if idx <= 1:
                if adaptive_pattern[key] > adjust_amount / 2:
                    transferred_amount += 3
                    adaptive_pattern[key] -= 3
                else:
                    transferred_amount += adaptive_pattern[key]
                    adaptive_pattern[key] = 0
            elif idx >= len(applied_damage) - 2:
                adaptive_pattern[key] += transferred_amount / 2
            else:
                continue

        return {'AppliedDamage': applied_damage, 'AdaptivePattern': adaptive_pattern}
