# No need to import sqlite3 here
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routers import sensor, firing

app = FastAPI()

app.include_router(sensor.router)
app.include_router(firing.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}

app.mount("/static", StaticFiles(directory="static"), name="static")

# If you need to initialize the database at the start,
# assuming you have a function in your database module for it:
from database import init_db
init_db()
