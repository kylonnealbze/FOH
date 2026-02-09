-- ============================================================================
-- FOH Database Schema
-- ============================================================================
-- Complete database schema for Fragments of Hope coral reef monitoring system
-- Includes tables for sites, MPAs, outplanting history, photomosaics, 
-- temperature data, growth data, surveys, and photos
--
-- All geometry columns use SRID 4326 (WGS84) for GPS compatibility
-- ============================================================================

-- Drop tables if they exist (for clean re-creation)
DROP TABLE IF EXISTS photos CASCADE;
DROP TABLE IF EXISTS growth_data CASCADE;
DROP TABLE IF EXISTS surveys CASCADE;
DROP TABLE IF EXISTS temperature_data CASCADE;
DROP TABLE IF EXISTS photomosaics CASCADE;
DROP TABLE IF EXISTS outplanting_history CASCADE;
DROP TABLE IF EXISTS sites CASCADE;
DROP TABLE IF EXISTS mpas CASCADE;

-- ============================================================================
-- Sites Table
-- ============================================================================
-- Stores information about coral reef monitoring sites
-- location: Point geometry representing GPS coordinates of the site

CREATE TABLE sites (
    site_id SERIAL PRIMARY KEY,
    site_name VARCHAR(255) NOT NULL,
    location GEOMETRY(Point, 4326) NOT NULL,
    description TEXT,
    established_date DATE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE sites IS 'Coral reef monitoring sites with GPS coordinates';
COMMENT ON COLUMN sites.location IS 'GPS coordinates as PostGIS Point geometry (SRID 4326)';

-- ============================================================================
-- Marine Protected Areas (MPAs) Table
-- ============================================================================
-- Stores polygon boundaries of marine protected areas
-- boundary: Polygon geometry representing the MPA boundary

CREATE TABLE mpas (
    mpa_id SERIAL PRIMARY KEY,
    mpa_name VARCHAR(255) NOT NULL,
    boundary GEOMETRY(Polygon, 4326) NOT NULL,
    protection_level VARCHAR(100),
    established_year INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE mpas IS 'Marine Protected Areas with polygon boundaries';
COMMENT ON COLUMN mpas.boundary IS 'MPA boundary as PostGIS Polygon geometry (SRID 4326)';

-- ============================================================================
-- Outplanting History Table
-- ============================================================================
-- Tracks coral outplanting activities including species and location
-- location: Point geometry for the specific outplanting location

CREATE TABLE outplanting_history (
    outplanting_id SERIAL PRIMARY KEY,
    site_id INTEGER NOT NULL REFERENCES sites(site_id) ON DELETE CASCADE,
    location GEOMETRY(Point, 4326) NOT NULL,
    species VARCHAR(255) NOT NULL,
    number_of_corals INTEGER NOT NULL CHECK (number_of_corals > 0),
    outplanting_date DATE NOT NULL,
    source_nursery VARCHAR(255),
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE outplanting_history IS 'Record of coral outplanting activities';
COMMENT ON COLUMN outplanting_history.location IS 'GPS coordinates of outplanted corals (SRID 4326)';

-- ============================================================================
-- Photomosaics Table
-- ============================================================================
-- Stores metadata for photomosaic imagery of reef areas
-- coverage_area: Polygon geometry representing the area covered by the photomosaic

CREATE TABLE photomosaics (
    photomosaic_id SERIAL PRIMARY KEY,
    site_id INTEGER NOT NULL REFERENCES sites(site_id) ON DELETE CASCADE,
    coverage_area GEOMETRY(Polygon, 4326) NOT NULL,
    capture_date DATE NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    resolution DECIMAL(10, 4),
    photographer VARCHAR(255),
    processing_notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE photomosaics IS 'Photomosaic imagery metadata with coverage polygons';
COMMENT ON COLUMN photomosaics.coverage_area IS 'Area covered by photomosaic as Polygon (SRID 4326)';

-- ============================================================================
-- Temperature Data Table
-- ============================================================================
-- Time-series temperature measurements from reef sites

CREATE TABLE temperature_data (
    temp_id SERIAL PRIMARY KEY,
    site_id INTEGER NOT NULL REFERENCES sites(site_id) ON DELETE CASCADE,
    recorded_at TIMESTAMP WITH TIME ZONE NOT NULL,
    temperature_celsius DECIMAL(5, 2) NOT NULL,
    depth_meters DECIMAL(6, 2),
    sensor_id VARCHAR(100)
);

COMMENT ON TABLE temperature_data IS 'Time-series temperature measurements at monitoring sites';
COMMENT ON COLUMN temperature_data.temperature_celsius IS 'Water temperature in Celsius';

-- ============================================================================
-- Growth Data Table
-- ============================================================================
-- Tracks coral growth measurements over time

CREATE TABLE growth_data (
    growth_id SERIAL PRIMARY KEY,
    outplanting_id INTEGER NOT NULL REFERENCES outplanting_history(outplanting_id) ON DELETE CASCADE,
    measurement_date DATE NOT NULL,
    size_cm DECIMAL(6, 2) NOT NULL CHECK (size_cm >= 0),
    health_status VARCHAR(50),
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE growth_data IS 'Coral growth measurements over time';
COMMENT ON COLUMN growth_data.size_cm IS 'Coral size in centimeters';

-- ============================================================================
-- Surveys Table
-- ============================================================================
-- Records survey activities at sites

CREATE TABLE surveys (
    survey_id SERIAL PRIMARY KEY,
    site_id INTEGER NOT NULL REFERENCES sites(site_id) ON DELETE CASCADE,
    survey_date DATE NOT NULL,
    survey_type VARCHAR(100),
    surveyor_name VARCHAR(255),
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE surveys IS 'Survey activities at monitoring sites';

-- ============================================================================
-- Photos Table
-- ============================================================================
-- Stores photo metadata with GPS location and survey association

CREATE TABLE photos (
    photo_id SERIAL PRIMARY KEY,
    survey_id INTEGER REFERENCES surveys(survey_id) ON DELETE SET NULL,
    site_id INTEGER NOT NULL REFERENCES sites(site_id) ON DELETE CASCADE,
    location GEOMETRY(Point, 4326) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    caption TEXT,
    taken_at TIMESTAMP WITH TIME ZONE NOT NULL,
    photographer VARCHAR(255)
);

COMMENT ON TABLE photos IS 'Photo metadata with GPS coordinates and survey association';
COMMENT ON COLUMN photos.location IS 'GPS coordinates where photo was taken (SRID 4326)';

-- ============================================================================
-- Create update trigger function for updated_at timestamps
-- ============================================================================

CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply updated_at trigger to all relevant tables
CREATE TRIGGER update_sites_updated_at BEFORE UPDATE ON sites
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_mpas_updated_at BEFORE UPDATE ON mpas
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_outplanting_updated_at BEFORE UPDATE ON outplanting_history
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_photomosaics_updated_at BEFORE UPDATE ON photomosaics
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_growth_updated_at BEFORE UPDATE ON growth_data
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_surveys_updated_at BEFORE UPDATE ON surveys
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
