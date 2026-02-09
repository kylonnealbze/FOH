-- ============================================================================
-- FOH Database Indexes
-- ============================================================================
-- Creates indexes for optimal query performance on geometry columns,
-- foreign keys, and frequently queried fields
-- ============================================================================

-- ============================================================================
-- Spatial Indexes (GIST)
-- ============================================================================
-- Spatial indexes dramatically improve performance of geometric queries
-- like finding nearby points, points within polygons, etc.

-- Index on sites location for spatial queries
CREATE INDEX idx_sites_location ON sites USING GIST (location);

-- Index on MPA boundaries for spatial containment queries
CREATE INDEX idx_mpas_boundary ON mpas USING GIST (boundary);

-- Index on outplanting locations for spatial queries
CREATE INDEX idx_outplanting_location ON outplanting_history USING GIST (location);

-- Index on photomosaic coverage areas
CREATE INDEX idx_photomosaics_coverage ON photomosaics USING GIST (coverage_area);

-- Index on photo locations
CREATE INDEX idx_photos_location ON photos USING GIST (location);

-- ============================================================================
-- Foreign Key Indexes
-- ============================================================================
-- Improves JOIN performance and foreign key constraint checking

-- Outplanting history foreign keys
CREATE INDEX idx_outplanting_site_id ON outplanting_history(site_id);

-- Photomosaics foreign keys
CREATE INDEX idx_photomosaics_site_id ON photomosaics(site_id);

-- Temperature data foreign keys
CREATE INDEX idx_temperature_site_id ON temperature_data(site_id);

-- Growth data foreign keys
CREATE INDEX idx_growth_outplanting_id ON growth_data(outplanting_id);

-- Surveys foreign keys
CREATE INDEX idx_surveys_site_id ON surveys(site_id);

-- Photos foreign keys
CREATE INDEX idx_photos_survey_id ON photos(survey_id);
CREATE INDEX idx_photos_site_id ON photos(site_id);

-- ============================================================================
-- Temporal Indexes
-- ============================================================================
-- Improves performance of time-based queries and date filtering

-- Index on temperature data timestamp for time-series queries
CREATE INDEX idx_temperature_recorded_at ON temperature_data(recorded_at);

-- Index on outplanting date for historical queries
CREATE INDEX idx_outplanting_date ON outplanting_history(outplanting_date);

-- Index on survey date for temporal filtering
CREATE INDEX idx_surveys_date ON surveys(survey_date);

-- Index on photo timestamp
CREATE INDEX idx_photos_taken_at ON photos(taken_at);

-- Index on growth measurement date
CREATE INDEX idx_growth_measurement_date ON growth_data(measurement_date);

-- Index on photomosaic capture date
CREATE INDEX idx_photomosaics_capture_date ON photomosaics(capture_date);

-- ============================================================================
-- Text Search Indexes
-- ============================================================================
-- Improves performance of text-based searches

-- Index on site names for searching
CREATE INDEX idx_sites_name ON sites(site_name);

-- Index on MPA names for searching
CREATE INDEX idx_mpas_name ON mpas(mpa_name);

-- Index on species for filtering outplanting data
CREATE INDEX idx_outplanting_species ON outplanting_history(species);

-- ============================================================================
-- Composite Indexes
-- ============================================================================
-- Optimizes common multi-column queries

-- Composite index for site-based time-series queries
CREATE INDEX idx_temperature_site_time ON temperature_data(site_id, recorded_at);

-- Composite index for outplanting queries by site and date
CREATE INDEX idx_outplanting_site_date ON outplanting_history(site_id, outplanting_date);

-- Composite index for survey queries by site and date
CREATE INDEX idx_surveys_site_date ON surveys(site_id, survey_date);

-- ============================================================================
-- Analyze tables for statistics
-- ============================================================================
-- Update table statistics for the query planner

ANALYZE sites;
ANALYZE mpas;
ANALYZE outplanting_history;
ANALYZE photomosaics;
ANALYZE temperature_data;
ANALYZE growth_data;
ANALYZE surveys;
ANALYZE photos;
