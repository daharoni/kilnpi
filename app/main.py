# No need to import sqlite3 here
from fastapi import FastAPI, WebSocket
from fastapi.staticfiles import StaticFiles
from app.routers import sensor, firing
import asyncio
from typing import List
from app.services.websocket_manager import connections, broadcast
from app.services.temperature_sampling import poll_temperature_sensor

app = FastAPI()
connections: List[WebSocket] = []  # Keep track of active connections

app.include_router(sensor.router)
app.include_router(firing.router)

@app.websocket("/ws/temperature")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connections.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Handle incoming message (if necessary)
    except Exception as e:
        connections.remove(websocket)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(poll_temperature_sensor())

app.mount("/static", StaticFiles(directory="static"), name="static")

# If you need to initialize the database at the start,
# assuming you have a function in your database module for it:
from database import init_db
init_db()


# Run the application directly using uvicorn when this file is executed as the main program
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)