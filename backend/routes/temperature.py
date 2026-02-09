"""
Temperature Data API Routes
Time-series temperature measurements
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional
from datetime import datetime

from ..database import get_db
from ..models import TemperatureData

router = APIRouter(prefix="/api/temperature", tags=["temperature"])


@router.get("/by-site/{site_id}", summary="Get temperature data by site")
def get_temperature_by_site(
    site_id: int,
    db: Session = Depends(get_db),
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    limit: int = Query(1000, ge=1, le=10000)
):
    """
    Get temperature time-series data for a specific site
    
    Args:
        site_id: Unique site identifier
        start_date: Optional start date filter (YYYY-MM-DD)
        end_date: Optional end date filter (YYYY-MM-DD)
        limit: Maximum number of records to return
        
    Returns:
        List of temperature readings with timestamps
    """
    query = db.query(TemperatureData).filter(
        TemperatureData.site_id == site_id
    )
    
    if start_date:
        query = query.filter(TemperatureData.recorded_at >= start_date)
    if end_date:
        query = query.filter(TemperatureData.recorded_at <= end_date)
    
    temps = query.order_by(TemperatureData.recorded_at).limit(limit).all()
    
    # Convert to simple list of dictionaries
    return {
        "site_id": site_id,
        "count": len(temps),
        "data": [
            {
                "temp_id": t.temp_id,
                "recorded_at": t.recorded_at.isoformat() if t.recorded_at else None,
                "temperature_celsius": float(t.temperature_celsius) if t.temperature_celsius else None,
                "depth_meters": float(t.depth_meters) if t.depth_meters else None,
                "sensor_id": t.sensor_id
            }
            for t in temps
        ]
    }


@router.post("", summary="Add temperature reading", status_code=201)
def add_temperature(
    site_id: int,
    temperature_celsius: float,
    recorded_at: Optional[str] = None,
    depth_meters: Optional[float] = None,
    sensor_id: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Add a new temperature reading
    
    Args:
        site_id: Site where temperature was recorded
        temperature_celsius: Temperature in Celsius
        recorded_at: Optional timestamp (defaults to now)
        depth_meters: Optional depth in meters
        sensor_id: Optional sensor identifier
        
    Returns:
        Created temperature record
    """
    if recorded_at is None:
        recorded_at = datetime.utcnow()
    
    new_temp = TemperatureData(
        site_id=site_id,
        recorded_at=recorded_at,
        temperature_celsius=temperature_celsius,
        depth_meters=depth_meters,
        sensor_id=sensor_id
    )
    
    db.add(new_temp)
    db.commit()
    db.refresh(new_temp)
    
    return {
        "temp_id": new_temp.temp_id,
        "site_id": new_temp.site_id,
        "recorded_at": new_temp.recorded_at.isoformat(),
        "temperature_celsius": float(new_temp.temperature_celsius),
        "depth_meters": float(new_temp.depth_meters) if new_temp.depth_meters else None,
        "sensor_id": new_temp.sensor_id
    }
