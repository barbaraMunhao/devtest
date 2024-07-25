from application.api_models import Demand


# A simple class to handle the demand history.
class DemandHistoryHandler(object):
    def __init__(self, demand_history_db):
        self._demand_history_db = demand_history_db

    def save_demand(self, elevator_id, resting_floor, demanded_floor):
        self._demand_history_db.save_demand(elevator_id, resting_floor, demanded_floor)

    # Get the complete demand history for a given elevator and return a JSON object.
    def get_complete_demand_history(self, elevator_id):
        demand_history = self._demand_history_db.get_demand_history(elevator_id)
        demand_history_json = [Demand(resting_floor=row[2], demanded_floor=row[3]).model_dump()
                               for row in demand_history]
        return demand_history_json
