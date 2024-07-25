import unittest
from unittest.mock import Mock

from application.api_models import Demand
from application.demand_history_handler import DemandHistoryHandler


class TestDemandHistoryHandler(unittest.TestCase):

    def test_save_demand_calls_db_save_demand(self):
        demand_history_db = Mock()
        handler = DemandHistoryHandler(demand_history_db)
        elevator_id = 1
        resting_floor = 2
        demanded_floor = 3

        handler.save_demand(elevator_id, resting_floor, demanded_floor)

        demand_history_db.save_demand.assert_called_once_with(elevator_id, resting_floor, demanded_floor)

    def test_get_complete_demand_history_returns_correct_history(self):
        demand_history_db = Mock()
        elevator_id = 1
        mock_demand_history = [(1, 1, 2, 3)]
        expected_demand_history = [Demand(resting_floor=2, demanded_floor=3).model_dump()]
        demand_history_db.get_demand_history.return_value = mock_demand_history
        handler = DemandHistoryHandler(demand_history_db)

        result = handler.get_complete_demand_history(elevator_id)

        self.assertEqual(result, expected_demand_history)

    def test_get_complete_demand_history_handles_empty_history(self):
        demand_history_db = Mock()
        expected_demand_history = []
        elevator_id = 1
        demand_history_db.get_demand_history.return_value = expected_demand_history
        handler = DemandHistoryHandler(demand_history_db)

        result = handler.get_complete_demand_history(elevator_id)

        self.assertEqual(result, expected_demand_history)


if __name__ == '__main__':
    unittest.main()