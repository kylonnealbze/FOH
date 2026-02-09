"""
Outplanting History API Routes
Coral outplanting records and locations
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional

from ..database import get_db
from ..models import OutplantingHistory
from ..utils.geojson import models_to_geojson, model_to_geojson_feature

router = APIRouter(prefix="/api/outplanting", tags=["outplanting"])


@router.get("", summary="List all outplanting records")
def list_outplanting(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=1000),
    species: Optional[str] = None
):
    """
    Get all coral outplanting records as GeoJSON FeatureCollection
    
    Args:
        skip: Number of records to skip (pagination)
        limit: Maximum number of records to return
        species: Optional species filter
        
    Returns:
        GeoJSON FeatureCollection with outplanting locations
    """
    query = db.query(OutplantingHistory)
    
    if species:
        query = query.filter(OutplantingHistory.species.ilike(f"%{species}%"))
    
    outplanting = query.offset(skip).limit(limit).all()
    return models_to_geojson(outplanting, geometry_field="location")


@router.get("/by-site/{site_id}", summary="Get outplanting by site")
def get_outplanting_by_site(
    site_id: int,
    db: Session = Depends(get_db)
):
    """
    Get all outplanting records for a specific site
    
    Args:
        site_id: Unique site identifier
        
    Returns:
        GeoJSON FeatureCollection with outplanting records
    """
    outplanting = db.query(OutplantingHistory).filter(
        OutplantingHistory.site_id == site_id
    ).all()
    
    return models_to_geojson(outplanting, geometry_field="location")


@router.post("", summary="Create outplanting record", status_code=201)
def create_outplanting(
    site_id: int,
    latitude: float = Query(..., ge=-90, le=90),
    longitude: float = Query(..., ge=-180, le=180),
    species: str = Query(..., min_length=1),
    number_of_corals: int = Query(..., gt=0),
    outplanting_date: str = Query(...),
    source_nursery: Optional[str] = None,
    notes: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Create new coral outplanting record
    
    Args:
        site_id: Site where corals were outplanted
        latitude: Latitude coordinate (WGS84)
        longitude: Longitude coordinate (WGS84)
        species: Coral species name
        number_of_corals: Number of coral fragments outplanted
        outplanting_date: Date of outplanting (YYYY-MM-DD)
        source_nursery: Optional nursery source
        notes: Optional notes
        
    Returns:
        Created outplanting record as GeoJSON Feature
    """
    new_outplanting = OutplantingHistory(
        site_id=site_id,
        location=func.ST_SetSRID(func.ST_MakePoint(longitude, latitude), 4326),
        species=species,
        number_of_corals=number_of_corals,
        outplanting_date=outplanting_date,
        source_nursery=source_nursery,
        notes=notes
    )
    
    db.add(new_outplanting)
    db.commit()
    db.refresh(new_outplanting)
    
    return model_to_geojson_feature(new_outplanting, geometry_field="location")
