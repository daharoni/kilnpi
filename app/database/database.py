import asyncio
from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import datetime
from app.models.database_model import Firing, Base, KilnMeasurement, LastKilnMeasurements
from app.utils.global_state import temperature_broadcaster
from app.models.sensor_model import TemperatureData
from app.routers.app_state import get_kiln_parameters, current_state


DATABASE_URL = "sqlite:///./data/sqlite.db"

# SQLAlchemy setup
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db_firing_id = ''

last_measurement = LastKilnMeasurements()

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Add new firing. This should happen when user clicks Start button
def add_new_firing(name: str):
    global db_firing_id
    
    db = SessionLocal()
    try:
        new_firing = Firing(name=name, start_time=datetime.datetime.now(), firing_profile='profile1')
        db.add(new_firing)
        db.commit()
        db.refresh(new_firing)  # Refreshes the instance from the database, and loads any newly generated identifiers
        db_firing_id = new_firing.firing_id
    except Exception as e:
        db.rollback()
        print(f"Failed to add new firing: {e}")
    finally:
        db.close()
        
async def add_new_measuremnt_entry():
    global db_firing_id
    global last_measurement
    global current_state
    
    kiln_params = get_kiln_parameters()
    
    db = SessionLocal()
    while True:
        if (current_state.isFiring):
            if (db_firing_id == ''):
                # Adds a new firing entry to the db for the first time after start of firing
                add_new_firing(current_state.firingName)
            try:
                # Create a new TemperatureMeasurement instance
                new_measurement = KilnMeasurement(
                    experiment_id=db_firing_id,
                    timestamp=last_measurement.time_since_start,
                    temperature_kiln=last_measurement.kiln_temperaure,
                    temperature_setpoint= last_measurement.setpoint_value,
                    duty_cycle= last_measurement.duty_cycle
                )

                # Add the new temperature measurement to the session and commit
                db.add(new_measurement)
                db.commit()
            except Exception as e:
                db.rollback()
                print(f"Failed to add new temperature entry: {e}")
            finally:
                db.close()
        
        await asyncio.sleep(kiln_params.database_parameters.logging_period)
    
# Initialize the database and create tables
init_db()
# temperature_broadcaster.add_listener(add_new_temperature_entry)
