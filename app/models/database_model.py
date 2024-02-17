from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime, ForeignKey, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()

class Firing(Base):
    __tablename__ = 'firing'
    
    firing_id = Column(Integer, primary_key=True)
    name = Column(String)
    start_time = Column(DateTime)
    firing_profile = Column(String)
    measurements = relationship("TemperatureMeasurement", back_populates="firing")

class TemperatureMeasurement(Base):
    __tablename__ = 'temperature_measurements'
    
    measurement_id = Column(Integer, primary_key=True)
    experiment_id = Column(Integer, ForeignKey('firing.firing_id'))
    timestamp = Column(DateTime)
    temperature_kiln = Column(Float)
    temperature_setpoint = Column(Float)
    firing = relationship("Firing", back_populates="measurements")
