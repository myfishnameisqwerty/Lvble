import logging
from fastapi import FastAPI, HTTPException

import aiosqlite
from schemas import CommandRequest, DataSchema
import uvicorn
from portals.shared_logic import RentPortalFactory
from utils import create_sqlite_table, save_data_to_sqlite

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

app = FastAPI()


@app.on_event("startup")
async def on_startup():
    await create_sqlite_table()


@app.post("/save_data/")
async def save_data(command: CommandRequest):
    logging.info(f"Got API call {command.model_dump()}")
    try:
        rent_portal = RentPortalFactory.create_portal(
            command.tenant_portal, command.username, command.password
        )
        async with rent_portal as portal:
            data = await portal.get_data()
            logging.info(f"Got {data=}")
            validated_data = DataSchema(**data)
            await save_data_to_sqlite(**validated_data.model_dump())
            return {"message": "Data saved or updated in SQLite database."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
