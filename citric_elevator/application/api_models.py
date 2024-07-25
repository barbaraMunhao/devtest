from pydantic import BaseModel

# Endpoints requests formats for the API


class DemandRequest(BaseModel):
    elevator_id: int
    demanded_floor: int


class ElevatorIdealRestingFloorRequest(BaseModel):
    elevator_id: int
    ideal_floor: int


class MultipleDemandsRequest(BaseModel):
    num_demand: int


class Demand(BaseModel):
    resting_floor: int
    demanded_floor: int
