import os
import sys

import pytest
import pytest_asyncio
from httpx import AsyncClient
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import app

@pytest.mark.asyncio
async def test_demand():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        valid_floor = 2
        valid_elevator = 1

        response = await ac.post("/demand", json={"elevator_id": valid_elevator,
                                                  "demanded_floor": valid_floor})
    assert response.status_code == 200
    assert response.json() == {"message": "Elevator demanded successfully"}

@pytest.mark.asyncio
async def test_update_ideal_resting_floor():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        valid_floor = 2
        valid_elevator_id = 1

        response = await ac.patch("/update_ideal_resting_floor",
                                 json={"elevator_id": valid_elevator_id, "ideal_floor": valid_floor})

    assert response.status_code == 200
    assert response.json() == {"message": "Ideal resting floor updated successfully"}

@pytest.mark.asyncio
async def test_complete_demand_history():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        valid_elevator_id = 1

        response = await ac.get("/complete_demand_history/{0}".format(valid_elevator_id))

    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_generate_multiple_demands():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        num_demand = 5

        response = await ac.post("/generate_multiple_demands", json={"num_demand": num_demand})

    assert response.status_code == 200
    assert response.json() == {"message": "{0} Demands generated successfully".format(num_demand)}