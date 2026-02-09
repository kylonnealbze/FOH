"""
Surveys API Routes
Survey activities and associated photos
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional

from ..database import get_db
from ..models import Survey, Photo
from ..utils.geojson import models_to_geojson

router = APIRouter(prefix="/api/surveys", tags=["surveys"])


@router.get("", summary="List all surveys")
def list_surveys(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=1000),
    site_id: Optional[int] = None
):
    """
    Get all surveys
    
    Args:
        skip: Number of records to skip (pagination)
        limit: Maximum number of records to return
        site_id: Optional site filter
        
    Returns:
        List of surveys
    """
    query = db.query(Survey)
    
    if site_id:
        query = query.filter(Survey.site_id == site_id)
    
    surveys = query.offset(skip).limit(limit).all()
    
    return {
        "count": len(surveys),
        "surveys": [
            {
                "survey_id": s.survey_id,
                "site_id": s.site_id,
                "survey_date": s.survey_date.isoformat() if s.survey_date else None,
                "survey_type": s.survey_type,
                "surveyor_name": s.surveyor_name,
                "notes": s.notes,
                "created_at": s.created_at.isoformat() if s.created_at else None
            }
            for s in surveys
        ]
    }


@router.get("/{survey_id}", summary="Get survey details")
def get_survey(survey_id: int, db: Session = Depends(get_db)):
    """
    Get survey details including associated photos
    
    Args:
        survey_id: Unique survey identifier
        
    Returns:
        Survey details with photos as GeoJSON
    """
    survey = db.query(Survey).filter(Survey.survey_id == survey_id).first()
    if not survey:
        raise HTTPException(status_code=404, detail="Survey not found")
    
    # Get photos for this survey
    photos = db.query(Photo).filter(Photo.survey_id == survey_id).all()
    photos_geojson = models_to_geojson(photos, geometry_field="location")
    
    return {
        "survey": {
            "survey_id": survey.survey_id,
            "site_id": survey.site_id,
            "survey_date": survey.survey_date.isoformat() if survey.survey_date else None,
            "survey_type": survey.survey_type,
            "surveyor_name": survey.surveyor_name,
            "notes": survey.notes,
            "created_at": survey.created_at.isoformat() if survey.created_at else None
        },
        "photos": photos_geojson
    }
