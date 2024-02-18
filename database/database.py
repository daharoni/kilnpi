from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import datetime
from app.models.database_model import Firing, Base

DATABASE_URL = "sqlite:///./data/sqlite.db"

# SQLAlchemy setup
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


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
    db = SessionLocal()
    try:
        new_firing = Firing(name=name, start_time=datetime.datetime.now(), firing_profile='profile1')
        db.add(new_firing)
        db.commit()
    finally:
        db.close()
    
# Initialize the database and create tables
init_db()
