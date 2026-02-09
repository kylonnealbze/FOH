"""
GeoJSON Serialization Utilities
Helper functions to convert PostGIS geometries to GeoJSON format
"""
from typing import Any, Dict, List
from geoalchemy2 import WKBElement
from geoalchemy2.shape import to_shape
import json


def geometry_to_geojson(geom: WKBElement) -> Dict[str, Any]:
    """
    Convert a GeoAlchemy2 geometry element to GeoJSON geometry object
    
    Args:
        geom: GeoAlchemy2 WKBElement geometry
        
    Returns:
        Dictionary representing GeoJSON geometry
    """
    if geom is None:
        return None
    
    # Convert to Shapely geometry
    shapely_geom = to_shape(geom)
    
    # Convert to GeoJSON-like dict
    return json.loads(json.dumps(shapely_geom.__geo_interface__))


def create_feature(properties: Dict[str, Any], geometry: WKBElement) -> Dict[str, Any]:
    """
    Create a GeoJSON Feature from properties and geometry
    
    Args:
        properties: Dictionary of feature properties
        geometry: GeoAlchemy2 geometry element
        
    Returns:
        GeoJSON Feature dictionary
    """
    return {
        "type": "Feature",
        "geometry": geometry_to_geojson(geometry),
        "properties": properties
    }


def create_feature_collection(features: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Create a GeoJSON FeatureCollection from a list of features
    
    Args:
        features: List of GeoJSON Feature dictionaries
        
    Returns:
        GeoJSON FeatureCollection dictionary
    """
    return {
        "type": "FeatureCollection",
        "features": features
    }


def model_to_geojson_feature(model_instance: Any, geometry_field: str, exclude_fields: List[str] = None) -> Dict[str, Any]:
    """
    Convert a SQLAlchemy model instance to a GeoJSON Feature
    
    Args:
        model_instance: SQLAlchemy model instance
        geometry_field: Name of the geometry field in the model
        exclude_fields: List of field names to exclude from properties
        
    Returns:
        GeoJSON Feature dictionary
    """
    if exclude_fields is None:
        exclude_fields = []
    
    # Extract geometry
    geometry = getattr(model_instance, geometry_field, None)
    
    # Build properties dictionary, excluding geometry and specified fields
    properties = {}
    for column in model_instance.__table__.columns:
        field_name = column.name
        if field_name != geometry_field and field_name not in exclude_fields:
            value = getattr(model_instance, field_name)
            # Convert datetime and date objects to ISO format strings
            if hasattr(value, 'isoformat'):
                value = value.isoformat()
            # Convert Decimal to float
            if hasattr(value, '__float__'):
                try:
                    value = float(value)
                except:
                    pass
            properties[field_name] = value
    
    return create_feature(properties, geometry)


def models_to_geojson(model_instances: List[Any], geometry_field: str, exclude_fields: List[str] = None) -> Dict[str, Any]:
    """
    Convert a list of SQLAlchemy model instances to a GeoJSON FeatureCollection
    
    Args:
        model_instances: List of SQLAlchemy model instances
        geometry_field: Name of the geometry field in the models
        exclude_fields: List of field names to exclude from properties
        
    Returns:
        GeoJSON FeatureCollection dictionary
    """
    features = [
        model_to_geojson_feature(instance, geometry_field, exclude_fields)
        for instance in model_instances
    ]
    return create_feature_collection(features)
