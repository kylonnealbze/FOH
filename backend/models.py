"""
FOH SQLAlchemy Models with GeoAlchemy2
Database models for all tables with PostGIS geometry support
"""
from sqlalchemy import Column, Integer, String, Text, Date, DateTime, Numeric, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from geoalchemy2 import Geometry

from .database import Base


class Site(Base):
    """Coral reef monitoring sites"""
    __tablename__ = "sites"
    
    site_id = Column(Integer, primary_key=True, index=True)
    site_name = Column(String(255), nullable=False, index=True)
    location = Column(Geometry(geometry_type='POINT', srid=4326), nullable=False)
    description = Column(Text)
    established_date = Column(Date)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    outplanting_history = relationship("OutplantingHistory", back_populates="site", cascade="all, delete-orphan")
    photomosaics = relationship("Photomosaic", back_populates="site", cascade="all, delete-orphan")
    temperature_data = relationship("TemperatureData", back_populates="site", cascade="all, delete-orphan")
    surveys = relationship("Survey", back_populates="site", cascade="all, delete-orphan")
    photos = relationship("Photo", back_populates="site", cascade="all, delete-orphan")


class MPA(Base):
    """Marine Protected Areas"""
    __tablename__ = "mpas"
    
    mpa_id = Column(Integer, primary_key=True, index=True)
    mpa_name = Column(String(255), nullable=False, index=True)
    boundary = Column(Geometry(geometry_type='POLYGON', srid=4326), nullable=False)
    protection_level = Column(String(100))
    established_year = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class OutplantingHistory(Base):
    """Coral outplanting records"""
    __tablename__ = "outplanting_history"
    
    outplanting_id = Column(Integer, primary_key=True, index=True)
    site_id = Column(Integer, ForeignKey("sites.site_id", ondelete="CASCADE"), nullable=False, index=True)
    location = Column(Geometry(geometry_type='POINT', srid=4326), nullable=False)
    species = Column(String(255), nullable=False, index=True)
    number_of_corals = Column(Integer, nullable=False)
    outplanting_date = Column(Date, nullable=False, index=True)
    source_nursery = Column(String(255))
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    __table_args__ = (
        CheckConstraint('number_of_corals > 0', name='check_positive_corals'),
    )
    
    # Relationships
    site = relationship("Site", back_populates="outplanting_history")
    growth_data = relationship("GrowthData", back_populates="outplanting", cascade="all, delete-orphan")


class Photomosaic(Base):
    """Photomosaic imagery metadata"""
    __tablename__ = "photomosaics"
    
    photomosaic_id = Column(Integer, primary_key=True, index=True)
    site_id = Column(Integer, ForeignKey("sites.site_id", ondelete="CASCADE"), nullable=False, index=True)
    coverage_area = Column(Geometry(geometry_type='POLYGON', srid=4326), nullable=False)
    capture_date = Column(Date, nullable=False, index=True)
    file_path = Column(String(500), nullable=False)
    resolution = Column(Numeric(10, 4))
    photographer = Column(String(255))
    processing_notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    site = relationship("Site", back_populates="photomosaics")


class TemperatureData(Base):
    """Temperature measurements"""
    __tablename__ = "temperature_data"
    
    temp_id = Column(Integer, primary_key=True, index=True)
    site_id = Column(Integer, ForeignKey("sites.site_id", ondelete="CASCADE"), nullable=False, index=True)
    recorded_at = Column(DateTime(timezone=True), nullable=False, index=True)
    temperature_celsius = Column(Numeric(5, 2), nullable=False)
    depth_meters = Column(Numeric(6, 2))
    sensor_id = Column(String(100))
    
    # Relationships
    site = relationship("Site", back_populates="temperature_data")


class GrowthData(Base):
    """Coral growth measurements"""
    __tablename__ = "growth_data"
    
    growth_id = Column(Integer, primary_key=True, index=True)
    outplanting_id = Column(Integer, ForeignKey("outplanting_history.outplanting_id", ondelete="CASCADE"), nullable=False, index=True)
    measurement_date = Column(Date, nullable=False, index=True)
    size_cm = Column(Numeric(6, 2), nullable=False)
    health_status = Column(String(50))
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    __table_args__ = (
        CheckConstraint('size_cm >= 0', name='check_positive_size'),
    )
    
    # Relationships
    outplanting = relationship("OutplantingHistory", back_populates="growth_data")


class Survey(Base):
    """Survey activities"""
    __tablename__ = "surveys"
    
    survey_id = Column(Integer, primary_key=True, index=True)
    site_id = Column(Integer, ForeignKey("sites.site_id", ondelete="CASCADE"), nullable=False, index=True)
    survey_date = Column(Date, nullable=False, index=True)
    survey_type = Column(String(100))
    surveyor_name = Column(String(255))
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    site = relationship("Site", back_populates="surveys")
    photos = relationship("Photo", back_populates="survey")


class Photo(Base):
    """Photo metadata with GPS coordinates"""
    __tablename__ = "photos"
    
    photo_id = Column(Integer, primary_key=True, index=True)
    survey_id = Column(Integer, ForeignKey("surveys.survey_id", ondelete="SET NULL"), index=True)
    site_id = Column(Integer, ForeignKey("sites.site_id", ondelete="CASCADE"), nullable=False, index=True)
    location = Column(Geometry(geometry_type='POINT', srid=4326), nullable=False)
    file_path = Column(String(500), nullable=False)
    caption = Column(Text)
    taken_at = Column(DateTime(timezone=True), nullable=False, index=True)
    photographer = Column(String(255))
    
    # Relationships
    survey = relationship("Survey", back_populates="photos")
    site = relationship("Site", back_populates="photos")
