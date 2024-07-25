import unittest

from exception.invalid_floor_error import InvalidFloorError
from model.elevator import Elevator
from unittest.mock import patch


class TestElevator(unittest.TestCase):

    def test_initializes_correctly_with_valid_parameters(self):
        expected_id = 1
        expected_first_floor = 0
        expected_last_floor = 10
        expected_current_floor = 5
        expected_ideal_resting_floor = 3
        expected_is_vacant = True

        elevator = Elevator(elevator_id=expected_id, first_floor=expected_first_floor,
                            last_floor=expected_last_floor, current_floor=expected_current_floor,
                            ideal_resting_floor=expected_ideal_resting_floor)

        self.assertEqual(elevator.id, expected_id)
        self.assertEqual(elevator.first_floor, expected_first_floor)
        self.assertEqual(elevator.last_floor, expected_last_floor)
        self.assertEqual(elevator.current_floor, expected_current_floor)
        self.assertEqual(elevator.ideal_resting_floor, expected_ideal_resting_floor)
        self.assertEqual(elevator.is_vacant, expected_is_vacant)

    def test_initializes_with_default_values(self):
        expected_id = 1
        expected_first_floor = 0
        expected_last_floor = 10
        expected_current_floor = 0
        expected_ideal_resting_floor = 0

        elevator = Elevator(elevator_id=expected_id, first_floor=expected_first_floor,
                            last_floor=expected_last_floor)

        self.assertEqual(elevator.current_floor, expected_current_floor)
        self.assertEqual(elevator._ideal_resting_floor, expected_ideal_resting_floor)

    def test_raises_assertion_error_for_invalid_floor_range(self):
        elevator_id = 1
        first_floor = 10
        last_floor = 0
        with self.assertRaises(InvalidFloorError):
            Elevator(elevator_id=elevator_id, first_floor=first_floor, last_floor=last_floor)

    def test_move_method_updates_current_floor(self):
        elevator_id = 1
        first_floor = 0
        last_floor = 10
        current_floor = 2
        elevator = Elevator(elevator_id=elevator_id, first_floor=first_floor,
                            last_floor=last_floor, current_floor=current_floor)
        demanded_floor = 5

        elevator._move(demanded_floor)

        self.assertEqual(elevator.current_floor, demanded_floor)

    def test_elevator_is_vacant_after_call(self):
        elevator_id = 1
        first_floor = 0
        last_floor = 10
        current_floor = 2
        ideal_resting_floor = 3
        elevator = Elevator(elevator_id=elevator_id, first_floor=first_floor,
                            last_floor=last_floor, current_floor=current_floor, ideal_resting_floor=ideal_resting_floor)
        elevator.is_vacant = False
        demanded_floor = 5

        elevator.call(demanded_floor)

        self.assertTrue(elevator.is_vacant)

    def test_moves_to_ideal_resting_floor_after_use(self):
        elevator_id = 1
        first_floor = 0
        last_floor = 10
        ideal_resting_floor = 3
        elevator = Elevator(elevator_id=elevator_id, first_floor=first_floor,
                            last_floor=last_floor, ideal_resting_floor=ideal_resting_floor)
        demanded_floor = 5

        elevator.call(demanded_floor)

        self.assertEqual(elevator.current_floor, elevator.ideal_resting_floor)

    def test_raises_assertion_error_for_invalid_current_floor(self):
        elevator_id = 1
        first_floor = 0
        last_floor = 10
        current_floor = 11

        with self.assertRaises(InvalidFloorError):
            Elevator(elevator_id=elevator_id, first_floor=first_floor,
                     last_floor=last_floor, current_floor=current_floor)

    def test_raises_assertion_error_for_invalid_ideal_resting_floor(self):
        elevator_id = 1
        first_floor = 0
        last_floor = 10
        ideal_resting_floor = 11

        with self.assertRaises(InvalidFloorError):
            Elevator(elevator_id=elevator_id, first_floor=first_floor,
                     last_floor=last_floor, ideal_resting_floor=ideal_resting_floor)

    @patch.object(Elevator, '_move')
    @patch.object(Elevator, '_simulate_button_press', return_value=7)
    def test_call_method_calls_move_with_correct_parameters(self, mock_simulate_button_press, mock_move):
        elevator_id = 1
        first_floor = 0
        last_floor = 10
        current_floor = 2
        ideal_resting_floor = 3
        elevator = Elevator(elevator_id=elevator_id, first_floor=first_floor,
                            last_floor=last_floor, current_floor=current_floor, ideal_resting_floor=ideal_resting_floor)
        demanded_floor = 5

        elevator.call(demanded_floor)

        mock_move.assert_any_call(demanded_floor)
        mock_move.assert_any_call(mock_simulate_button_press.return_value)
        mock_move.assert_any_call(elevator.ideal_resting_floor)


if __name__ == '__main__':
    unittest.main()
