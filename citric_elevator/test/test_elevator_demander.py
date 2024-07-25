import unittest
from unittest.mock import Mock
from application.elevator_demander import ElevatorDemander


class TestElevatorDemander(unittest.TestCase):

    def test_elevator_moves_to_requested_floor(self):
        elevator = Mock()
        elevator.current_floor = 2
        demand_history_handler = Mock()
        demander = ElevatorDemander(elevator, demand_history_handler)
        demanded_floor = 5

        demander.demand(demanded_floor)

        elevator.call.assert_called_once_with(demanded_floor)

    def test_demand_is_saved_when_flag_is_true(self):
        elevator = Mock()
        elevator.current_floor = 2
        elevator.id = 1
        demand_history_handler = Mock()
        demander = ElevatorDemander(elevator, demand_history_handler)
        demanded_floor = 5

        demander.demand(demanded_floor, save_demand=True)

        demand_history_handler.save_demand.assert_called_once_with(elevator.id,
                                                                   elevator.current_floor,
                                                                   demanded_floor)

    def test_demand_is_not_saved_when_flag_is_false(self):
        elevator = Mock()
        elevator.current_floor = 2
        demand_history_handler = Mock()
        demander = ElevatorDemander(elevator, demand_history_handler)
        demanded_floor = 5

        demander.demand(demanded_floor, save_demand=False)

        demand_history_handler.save_demand.assert_not_called()

    def test_elevator_stays_on_same_floor_if_called_to_current_floor(self):
        elevator = Mock()
        elevator.current_floor = 2
        demand_history_handler = Mock()
        demander = ElevatorDemander(elevator, demand_history_handler)

        demander.demand(elevator.current_floor)

        elevator.call.assert_called_once_with(elevator.current_floor)
        demand_history_handler.save_demand.assert_called_once_with(elevator.id,
                                                                   elevator.current_floor,
                                                                   elevator.current_floor)

if __name__ == '__main__':
    unittest.main()
