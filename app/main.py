# No need to import sqlite3 here
from fastapi import FastAPI
from app.routers import sensor, firing

app = FastAPI()

app.include_router(sensor.router)
app.include_router(firing.router)

# If you need to initialize the database at the start,
# assuming you have a function in your database module for it:
from database import init_db
init_db()
