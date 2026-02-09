"""
Spatial Queries API Routes
Advanced geospatial queries using PostGIS functions
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, or_
from geoalchemy2.functions import ST_DWithin, ST_Distance, ST_Within, ST_MakePoint, ST_SetSRID

from ..database import get_db
from ..models import Site, OutplantingHistory, Photomosaic, Photo, MPA
from ..utils.geojson import models_to_geojson

router = APIRouter(prefix="/api/spatial", tags=["spatial"])


@router.get("/nearby", summary="Find sites and data within radius")
def find_nearby(
    latitude: float = Query(..., ge=-90, le=90),
    longitude: float = Query(..., ge=-180, le=180),
    radius: int = Query(..., ge=1, le=100000, description="Radius in meters"),
    db: Session = Depends(get_db)
):
    """
    Find all sites and data within a specified radius of a point
    
    Args:
        latitude: Center point latitude
        longitude: Center point longitude
        radius: Search radius in meters
        
    Returns:
        GeoJSON FeatureCollections for sites, outplanting, and photos within radius
    """
    # Create center point geometry
    center_point = func.ST_SetSRID(func.ST_MakePoint(longitude, latitude), 4326)
    
    # Find sites within radius
    # Cast to geography for accurate distance calculation in meters
    sites = db.query(Site).filter(
        func.ST_DWithin(
            Site.location.cast(type_=func.geography),
            center_point.cast(type_=func.geography),
            radius
        )
    ).all()
    
    # Find outplanting locations within radius
    outplanting = db.query(OutplantingHistory).filter(
        func.ST_DWithin(
            OutplantingHistory.location.cast(type_=func.geography),
            center_point.cast(type_=func.geography),
            radius
        )
    ).all()
    
    # Find photos within radius
    photos = db.query(Photo).filter(
        func.ST_DWithin(
            Photo.location.cast(type_=func.geography),
            center_point.cast(type_=func.geography),
            radius
        )
    ).all()
    
    return {
        "center": {
            "latitude": latitude,
            "longitude": longitude
        },
        "radius_meters": radius,
        "results": {
            "sites": models_to_geojson(sites, geometry_field="location"),
            "outplanting": models_to_geojson(outplanting, geometry_field="location"),
            "photos": models_to_geojson(photos, geometry_field="location")
        }
    }


@router.get("/within-mpa/{mpa_id}", summary="Get all data within MPA")
def get_data_within_mpa(
    mpa_id: int,
    db: Session = Depends(get_db)
):
    """
    Get all sites, outplanting, and photos within a Marine Protected Area
    
    Args:
        mpa_id: Unique MPA identifier
        
    Returns:
        All geospatial data contained within the MPA boundary
    """
    # Get the MPA
    mpa = db.query(MPA).filter(MPA.mpa_id == mpa_id).first()
    if not mpa:
        raise HTTPException(status_code=404, detail="MPA not found")
    
    # Find sites within MPA boundary
    sites = db.query(Site).filter(
        func.ST_Within(Site.location, mpa.boundary)
    ).all()
    
    # Find outplanting locations within MPA boundary
    outplanting = db.query(OutplantingHistory).filter(
        func.ST_Within(OutplantingHistory.location, mpa.boundary)
    ).all()
    
    # Find photos within MPA boundary
    photos = db.query(Photo).filter(
        func.ST_Within(Photo.location, mpa.boundary)
    ).all()
    
    return {
        "mpa": {
            "mpa_id": mpa.mpa_id,
            "mpa_name": mpa.mpa_name,
            "protection_level": mpa.protection_level
        },
        "results": {
            "sites": models_to_geojson(sites, geometry_field="location"),
            "outplanting": models_to_geojson(outplanting, geometry_field="location"),
            "photos": models_to_geojson(photos, geometry_field="location")
        }
    }


@router.get("/distance", summary="Calculate distance between points")
def calculate_distance(
    lat1: float = Query(..., ge=-90, le=90),
    lon1: float = Query(..., ge=-180, le=180),
    lat2: float = Query(..., ge=-90, le=90),
    lon2: float = Query(..., ge=-180, le=180),
    db: Session = Depends(get_db)
):
    """
    Calculate the distance between two geographic points
    
    Args:
        lat1: First point latitude
        lon1: First point longitude
        lat2: Second point latitude
        lon2: Second point longitude
        
    Returns:
        Distance in meters and kilometers
    """
    point1 = func.ST_SetSRID(func.ST_MakePoint(lon1, lat1), 4326)
    point2 = func.ST_SetSRID(func.ST_MakePoint(lon2, lat2), 4326)
    
    # Calculate distance using geography type for accurate results
    distance_meters = db.query(
        func.ST_Distance(
            point1.cast(type_=func.geography),
            point2.cast(type_=func.geography)
        )
    ).scalar()
    
    return {
        "point1": {"latitude": lat1, "longitude": lon1},
        "point2": {"latitude": lat2, "longitude": lon2},
        "distance_meters": float(distance_meters),
        "distance_kilometers": float(distance_meters) / 1000
    }
