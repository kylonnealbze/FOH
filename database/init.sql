-- ============================================================================
-- FOH Database Initialization Script
-- ============================================================================
-- This script sets up the PostgreSQL database with PostGIS extension
-- and creates necessary extensions for geospatial operations
-- 
-- Usage:
--   psql -U postgres -d foh_database < init.sql
-- ============================================================================

-- Enable PostGIS extension for spatial data support
CREATE EXTENSION IF NOT EXISTS postgis;

-- Enable UUID extension for generating unique identifiers
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Verify PostGIS installation
SELECT PostGIS_Version();

-- Set the default SRID to 4326 (WGS84 - used by GPS)
-- This is the standard coordinate system for latitude/longitude
SELECT postgis_lib_version();

COMMENT ON EXTENSION postgis IS 'PostGIS extension for spatial and geographic objects';
