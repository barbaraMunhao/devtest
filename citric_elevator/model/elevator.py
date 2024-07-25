import random
from exception.invalid_floor_error import InvalidFloorError


# A simple class to represent an elevator. An Elevator has an id, a first floor,
# a last floor, a current floor, an ideal resting floor, and a status
# that indicates if the elevator is vacant. The ideal resting floor
# is kept because the idea is to update its value using a prediction algorithm based on the demand history.
# Note: The elevator is programed to return to the ideal resting floor after a delivery. If the ideal
# resting floor do not change by an external interference, the elevator will always return
# to the same floor.

class Elevator(object):
    def __init__(self, elevator_id, first_floor, last_floor,
                 current_floor=None, ideal_resting_floor=None):
        self._id = elevator_id

        if not first_floor < last_floor:
            raise InvalidFloorError("First floor must be lower than the last one")
        self._first_floor = first_floor

        if not last_floor >= 0:
            raise InvalidFloorError("The last floor must be at least the 0 floor")
        self._last_floor = last_floor

        if current_floor is None:
            self._current_floor = 0
        else:
            if not (self._first_floor <= current_floor <= self._last_floor):
                raise InvalidFloorError("Current floor must be between first and last floor")
            self._current_floor = current_floor

        if ideal_resting_floor is None:
            self._ideal_resting_floor = 0
        else:
            if not (self._first_floor <= ideal_resting_floor <= self._last_floor):
                raise InvalidFloorError("Ideal resting floor must be between first and last floor")
            self._ideal_resting_floor = ideal_resting_floor

        self._is_vacant = True

    @property
    def current_floor(self):
        return self._current_floor

    @current_floor.setter
    def current_floor(self, floor):
        if not (self._first_floor <= floor <= self._last_floor):
            raise InvalidFloorError("Floor must be between first and last floor")
        self._current_floor = floor

    @property
    def first_floor(self):
        return self._first_floor

    @first_floor.setter
    def first_floor(self, floor):
        if not floor < self._last_floor:
            raise InvalidFloorError("First floor must be lower than the last one")
        self._first_floor = floor

    @property
    def last_floor(self):
        return self._last_floor

    @last_floor.setter
    def last_floor(self, floor):
        if not floor > self._first_floor:
            raise InvalidFloorError("Last floor must be higher than the first one")
        self._last_floor = floor

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, elevator_id):
        self._id = elevator_id

    @property
    def ideal_resting_floor(self):
        return self._ideal_resting_floor

    @ideal_resting_floor.setter
    def ideal_resting_floor(self, floor):
        if not (self._first_floor <= floor <= self._last_floor):
            raise InvalidFloorError("Ideal resting floor must be between first and last floor")
        self._ideal_resting_floor = floor

    @property
    def is_vacant(self):
        return self._is_vacant

    @is_vacant.setter
    def is_vacant(self, flag):
        self._is_vacant = flag

    def _move(self, floor):
        self.current_floor = floor

    #  Simulate the press of a button to choose the next floor.
    #  To simplify and still keep this as a step, a random number is used as the next floor.
    def _simulate_button_press(self):
        next_floor = random.randint(self._first_floor, self._last_floor)
        return next_floor

    # Method to process a call of the elevator to a floor and move it.
    # To simplify the Elevator class, this method accumulates all the logic
    # to move the elevator and modify its state. To be called the elevator is called,
    # it is supposed to be vacant, then the method call modify it status
    #  and move (if necessary) for the demanded floor. After that, it simulates the press of a button,
    #  to choose the next floor to go. Finally, it moves the elevator to the next floor,
    #  and return to the ideal resting floor, marking the elevator as vacant again.

    def call(self, floor):
        print("Called at {0}".format(floor))

        # Elevator is going to be used
        self.is_vacant = False

        # Verify if the elevator is in the demanded floor, if not move it
        if self._current_floor != floor:
            self._move(floor)

        # Wait for the next floor to go
        next_floor = self._simulate_button_press()
        self._move(next_floor)

        # Once the elevator was used, it can be marked as vacant
        self.is_vacant = True
        if self._current_floor != self._ideal_resting_floor:
            self._move(self._ideal_resting_floor)
        print("Resting at {0}".format(self._current_floor))
