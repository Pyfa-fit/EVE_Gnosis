from unittest.mock import Mock
from simulations.capacitor import Capacitor
from formulas.formulas import Formulas

#from tests.restriction_tracker.restriction_testcase import RestrictionTestCase


class test_vengeance_stats():
    """Check functionality of booster slot index restriction"""

    module_list = []
    capacitor_amount = 375
    capacitor_recharge = 105468.75

    module_list.append(
        {
            'Amount': 10,
            'CycleTime': 2500,
            'Charges': False,
            'ReloadTime': False,
        }
    )  # Small T2 Nos

    module_list.append(
        {
            'Amount': -1.5,
            'CycleTime': 5000,
            'Charges': False,
            'ReloadTime': False,
        }
    )  # J5b Enduring Warp Scrambler

    module_list.append(
        {
            'Amount': -1.5,
            'CycleTime': 5000,
            'Charges': False,
            'ReloadTime': False,
        }
    )  # X5 Enduring Statis Webifier

    module_list.append(
        {
            'Amount': -40,
            'CycleTime': 4500,
            'Charges': False,
            'ReloadTime': False,
        }
    )  # Small Ancilliary Armor Repairer

    module_list.append(
        {
            'Amount': -10.5,
            'CycleTime': 5000,
            'Charges': False,
            'ReloadTime': False,
        }
    )  # Reactive Armor Hardener

    '''
    [Vengeance, Heavy Tackle]

    Energized Adaptive Nano Membrane II
    Small Ancillary Armor Repairer
    Reactive Armor Hardener
    True Sansha Adaptive Nano Plating

    5MN Quad LiF Restrained Microwarpdrive
    J5b Enduring Warp Scrambler
    X5 Enduring Stasis Webifier

    Rocket Launcher II, Nova Rage Rocket
    Rocket Launcher II, Nova Rage Rocket
    Rocket Launcher II, Nova Rage Rocket
    Rocket Launcher II, Nova Rage Rocket
    Small Energy Nosferatu II

    Small Anti-Thermal Pump II
    Small Auxiliary Nano Pump II
    '''

    def test_fail(self):
        # Check that if 2 or more holders are put into single slot
        # index, error is raised
        return_value = Capacitor.capacitor_time_simulator(self.module_list, self.capacitor_amount, self.capacitor_recharge)


    def test_fail_dos(self):
        return_matrix = Formulas.capacitor_shield_regen_matrix(self.capacitor_amount, self.capacitor_recharge)

    def test_add_does_not_set_default(mock_data_handler, mock_cache_handler):
        SourceManager.add('test', mock_data_handler, mock_cache_handler)

        assert SourceManager.default is None

    def test_fail_other_holder_class(self):
        # Make sure holders of all classes are affected
        item = self.ch.type_(type_id=1, attributes={Attribute.boosterness: 120})
        holder1 = Mock(state=State.offline, item=item, _domain=Domain.ship, spec_set=Module(1))
        holder2 = Mock(state=State.offline, item=item, _domain=Domain.ship, spec_set=Module(1))
        self.track_holder(holder1)
        self.track_holder(holder2)
        restriction_error1 = self.get_restriction_error(holder1, Restriction.booster_index)
        self.assertIsNotNone(restriction_error1)
        self.assertEqual(restriction_error1.holder_slot_index, 120)
        restriction_error2 = self.get_restriction_error(holder2, Restriction.booster_index)
        self.assertIsNotNone(restriction_error2)
        self.assertEqual(restriction_error2.holder_slot_index, 120)
        self.untrack_holder(holder1)
        self.untrack_holder(holder2)
        self.assertEqual(len(self.log), 0)
        self.assert_restriction_buffers_empty()