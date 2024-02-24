from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime, ForeignKey, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from pydantic import BaseModel
from typing import Optional

Base = declarative_base()

class Firing(Base):
    """
    Represents a firing process in the database.
    
    Attributes:
        firing_id (int): The primary key of the firing process.
        name (str): The name of the firing process.
        start_time (datetime): The start time of the firing process.
        firing_profile (str): The firing profile.
        measurements (relationship): The associated temperature measurements.
    """
    __tablename__ = 'firing'
    
    firing_id = Column(Integer, primary_key=True)
    name = Column(String)
    start_time = Column(DateTime)
    firing_profile = Column(String)
    measurements = relationship("KilnMeasurement", back_populates="firing")

class KilnMeasurement(Base):
    """
    The KilnMeasurement class represents a table in the database that stores temperature measurements associated with a firing process.
    """
    __tablename__ = 'temperature_measurements'
    
    measurement_id = Column(Integer, primary_key=True)
    experiment_id = Column(Integer, ForeignKey('firing.firing_id'))
    timestamp = Column(Float)
    temperature_kiln = Column(Float)
    temperature_setpoint = Column(Float)
    duty_cycle = Column(Float)
    firing = relationship("Firing", back_populates="measurements")
    
class LastKilnMeasurements(BaseModel):
    time_since_start: Optional[float] = None
    kiln_temperaure: Optional[float] = None
    setpoint_value: Optional[float] = None
    duty_cycle: Optional[float] = None
