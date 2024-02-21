from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import datetime
from app.models.database_model import Firing, Base, TemperatureMeasurement
from app.utils.global_state import temperature_broadcaster
from app.models.sensor_model import TemperatureData


DATABASE_URL = "sqlite:///./data/sqlite.db"

# SQLAlchemy setup
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db_firing_id = ''

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
        
async def add_new_temperature_entry(temp_data: TemperatureData):
    global db_firing_id
    db = SessionLocal()
    try:
        # Create a new TemperatureMeasurement instance
        new_measurement = TemperatureMeasurement(
            experiment_id=db_firing_id,
            timestamp=temp_data.timestamp,
            temperature_kiln=temp_data.temperature,
            temperature_setpoint=0.0001
        )

        # Add the new temperature measurement to the session and commit
        db.add(new_measurement)
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Failed to add new temperature entry: {e}")
    finally:
        db.close()
    
# Initialize the database and create tables
init_db()
# temperature_broadcaster.add_listener(add_new_temperature_entry)
