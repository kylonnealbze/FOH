"""
Sites API Routes
CRUD operations and spatial queries for coral reef sites
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from geoalchemy2.functions import ST_MakePoint, ST_SetSRID, ST_AsGeoJSON
from typing import List, Optional

from ..database import get_db
from ..models import Site
from ..utils.geojson import models_to_geojson, model_to_geojson_feature

router = APIRouter(prefix="/api/sites", tags=["sites"])


@router.get("", summary="List all sites")
def list_sites(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=1000)
):
    """
    Get all coral reef monitoring sites as GeoJSON FeatureCollection
    
    Returns:
        GeoJSON FeatureCollection with all sites
    """
    sites = db.query(Site).offset(skip).limit(limit).all()
    return models_to_geojson(sites, geometry_field="location")


@router.get("/{site_id}", summary="Get site by ID")
def get_site(site_id: int, db: Session = Depends(get_db)):
    """
    Get detailed information about a specific site
    
    Args:
        site_id: Unique site identifier
        
    Returns:
        GeoJSON Feature with site details
    """
    site = db.query(Site).filter(Site.site_id == site_id).first()
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    
    return model_to_geojson_feature(site, geometry_field="location")


@router.post("", summary="Create new site", status_code=201)
def create_site(
    site_name: str,
    latitude: float = Query(..., ge=-90, le=90),
    longitude: float = Query(..., ge=-180, le=180),
    description: Optional[str] = None,
    established_date: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Create a new coral reef monitoring site
    
    Args:
        site_name: Name of the site
        latitude: Latitude coordinate (WGS84)
        longitude: Longitude coordinate (WGS84)
        description: Optional site description
        established_date: Optional establishment date (YYYY-MM-DD)
        
    Returns:
        Created site as GeoJSON Feature
    """
    # Create new site with PostGIS point geometry
    new_site = Site(
        site_name=site_name,
        location=func.ST_SetSRID(func.ST_MakePoint(longitude, latitude), 4326),
        description=description,
        established_date=established_date
    )
    
    db.add(new_site)
    db.commit()
    db.refresh(new_site)
    
    return model_to_geojson_feature(new_site, geometry_field="location")


@router.put("/{site_id}", summary="Update site")
def update_site(
    site_id: int,
    site_name: Optional[str] = None,
    latitude: Optional[float] = Query(None, ge=-90, le=90),
    longitude: Optional[float] = Query(None, ge=-180, le=180),
    description: Optional[str] = None,
    established_date: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Update an existing site
    
    Args:
        site_id: Unique site identifier
        site_name: Optional new name
        latitude: Optional new latitude
        longitude: Optional new longitude
        description: Optional new description
        established_date: Optional new establishment date
        
    Returns:
        Updated site as GeoJSON Feature
    """
    site = db.query(Site).filter(Site.site_id == site_id).first()
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    
    # Update fields if provided
    if site_name is not None:
        site.site_name = site_name
    if description is not None:
        site.description = description
    if established_date is not None:
        site.established_date = established_date
    if latitude is not None and longitude is not None:
        site.location = func.ST_SetSRID(func.ST_MakePoint(longitude, latitude), 4326)
    
    db.commit()
    db.refresh(site)
    
    return model_to_geojson_feature(site, geometry_field="location")


@router.delete("/{site_id}", summary="Delete site", status_code=204)
def delete_site(site_id: int, db: Session = Depends(get_db)):
    """
    Delete a site and all associated data
    
    Args:
        site_id: Unique site identifier
    """
    site = db.query(Site).filter(Site.site_id == site_id).first()
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    
    db.delete(site)
    db.commit()
    
    return {"detail": "Site deleted successfully"}
