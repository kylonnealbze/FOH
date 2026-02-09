"""
Photomosaics API Routes
Photomosaic imagery metadata and coverage areas
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional

from ..database import get_db
from ..models import Photomosaic
from ..utils.geojson import models_to_geojson, model_to_geojson_feature

router = APIRouter(prefix="/api/photomosaics", tags=["photomosaics"])


@router.get("", summary="List all photomosaics")
def list_photomosaics(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=1000)
):
    """
    Get all photomosaics as GeoJSON FeatureCollection
    
    Returns:
        GeoJSON FeatureCollection with photomosaic coverage areas
    """
    photomosaics = db.query(Photomosaic).offset(skip).limit(limit).all()
    return models_to_geojson(photomosaics, geometry_field="coverage_area")


@router.get("/by-site/{site_id}", summary="Get photomosaics by site")
def get_photomosaics_by_site(
    site_id: int,
    db: Session = Depends(get_db)
):
    """
    Get all photomosaics for a specific site
    
    Args:
        site_id: Unique site identifier
        
    Returns:
        GeoJSON FeatureCollection with photomosaics for the site
    """
    photomosaics = db.query(Photomosaic).filter(
        Photomosaic.site_id == site_id
    ).all()
    
    return models_to_geojson(photomosaics, geometry_field="coverage_area")


@router.post("", summary="Create photomosaic metadata", status_code=201)
def create_photomosaic(
    site_id: int,
    coverage_wkt: str,
    capture_date: str,
    file_path: str,
    resolution: Optional[float] = None,
    photographer: Optional[str] = None,
    processing_notes: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Create new photomosaic metadata record
    
    Args:
        site_id: Site where photomosaic was captured
        coverage_wkt: Coverage area as WKT polygon string
        capture_date: Date of capture (YYYY-MM-DD)
        file_path: Path to photomosaic file
        resolution: Optional resolution in meters
        photographer: Optional photographer name
        processing_notes: Optional processing notes
        
    Returns:
        Created photomosaic as GeoJSON Feature
    """
    from sqlalchemy import func
    
    new_photomosaic = Photomosaic(
        site_id=site_id,
        coverage_area=func.ST_GeomFromText(coverage_wkt, 4326),
        capture_date=capture_date,
        file_path=file_path,
        resolution=resolution,
        photographer=photographer,
        processing_notes=processing_notes
    )
    
    db.add(new_photomosaic)
    db.commit()
    db.refresh(new_photomosaic)
    
    return model_to_geojson_feature(new_photomosaic, geometry_field="coverage_area")
