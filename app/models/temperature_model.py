# models/temperature_model.py
from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base  # Import your Base class from your database setup file
import datetime

class FiringProfile(Base):
    __tablename__ = "firing_profiles"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    max_temperature = Column(Float)
    # Relationship to link profiles with temperature records
    temperatures = relationship("TemperatureRecord", back_populates="profile")

class TemperatureRecord(Base):
    __tablename__ = "temperature_records"
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    temperature = Column(Float)
    profile_id = Column(Integer, ForeignKey('firing_profiles.id'))
    # Link back to the FiringProfile
    profile = relationship("FiringProfile", back_populates="temperatures")
