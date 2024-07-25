from application.elevator_demander import ElevatorDemander
from application.demand_history_handler import DemandHistoryHandler
from model.elevator import Elevator
from db.demand_history_db import DemandHistoryDB
from db import database
import random
from application.api_models import *

from fastapi import FastAPI

# Initialize the database
database_file = "database.db"
database.create_database(database_file)

# Create an instance of the Elevator class - this is a simple version of the system,
# so we are going to create only one elevator to demand it.
elevator = Elevator(1, 0, 3)

# Instantiate a handle to deal with the demand history
demand_history_db = DemandHistoryDB(database_file)
demand_history_handler = DemandHistoryHandler(demand_history_db)

# Instantiate an elevator demander to process demands and pass to the elevator
# and the demand history handler
elevator_demander = ElevatorDemander(elevator, demand_history_handler)

# Create an instance of the FastAPI class
app = FastAPI()

# The endpoints receive the elevator id, even our system has only one elevator,
# because this way it is possible to scale the system to have multiple elevators.
# For now, the endpoints simply verify if the elevator id in the request matches
# the elevator id existed. If it does, the request is processed, otherwise,
# an error message is returned.


# Define the endpoint for the /generate_demand
@app.post("/generate_multiple_demands")
async def generate_multiple_demands(request: MultipleDemandsRequest):
    for i in range(request.num_demand):
        demanded_floor = random.randint(elevator.first_floor, elevator.last_floor)
        elevator_demander.demand(demanded_floor)
        change_ideal_resting_floor = random.randint(0, 1)
        if change_ideal_resting_floor:
            ideal_floor = random.randint(elevator.first_floor, elevator.last_floor)
            elevator.ideal_resting_floor = ideal_floor
    return {"message": "{0} Demands generated successfully".format(request.num_demand)}


# Define the endpoint for the /demand - Endpoint used to demand an elevator
@app.post("/demand")
async def demand(request: DemandRequest):
    if request.elevator_id == elevator.id:
        elevator_demander.demand(request.demanded_floor)
        return {"message": "Elevator demanded successfully"}
    return {"message": "Elevator not found"}


# Define the endpoint for the /update_ideal_resting_floor - Endpoint used
# to update the ideal resting floor of an elevator
@app.patch("/update_ideal_resting_floor")
async def update_ideal_resting_floor(request: ElevatorIdealRestingFloorRequest):
    if request.elevator_id == elevator.id:
        elevator.ideal_floor = request.ideal_floor
        return {"message": "Ideal resting floor updated successfully"}
    return {"message": "Elevator not found"}


# Define the endpoint for the /complete_demand_history - Endpoint used
# to get the complete demand history of an elevator
@app.get("/complete_demand_history/{elevator_id}")
async def complete_demand_history(elevator_id: int):
    if elevator_id == elevator.id:
        demand_history = demand_history_handler.get_complete_demand_history(elevator.id)
        return demand_history
    return {"message": "Elevator not found"}
