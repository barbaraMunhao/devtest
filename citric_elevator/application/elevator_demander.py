# A simple class to deal only with the elevator demand.

class ElevatorDemander(object):

    def __init__(self, elevator, demand_history_handler):
        self._elevator = elevator
        self._demand_history_handler = demand_history_handler

    def demand(self, floor, save_demand=True):
        # Get the elevator current floor before it moves
        elevator_floor = self._elevator.current_floor

        # Call the elevator
        self._elevator.call(floor)

        # Save demand if save_demand flag is true - application may want to stop recording demands
        if save_demand:
            self._demand_history_handler.save_demand(self._elevator.id,
                                                     elevator_floor, floor)
