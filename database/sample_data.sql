-- ============================================================================
-- FOH Sample Data
-- ============================================================================
-- Sample data for testing the FOH database schema
-- Includes realistic coral reef data from Belize
-- ============================================================================

-- ============================================================================
-- Insert Sample Sites
-- ============================================================================
-- Using ST_SetSRID to create Point geometries with SRID 4326
-- Coordinates are for locations in Belize

INSERT INTO sites (site_name, location, description, established_date) VALUES
(
    'Salt Water Caye',
    ST_SetSRID(ST_MakePoint(-88.0823, 16.9891), 4326),
    'A key coral restoration site in the Inner Cayes with active outplanting operations',
    '2020-01-15'
),
(
    'Laughing Bird Caye',
    ST_SetSRID(ST_MakePoint(-88.1862, 16.4479), 4326),
    'Protected area with extensive coral reef monitoring',
    '2019-06-20'
),
(
    'South Water Caye',
    ST_SetSRID(ST_MakePoint(-88.0790, 16.8150), 4326),
    'Marine reserve with diverse coral species and ongoing research',
    '2018-03-10'
);

-- ============================================================================
-- Insert Sample MPAs
-- ============================================================================
-- Creating polygon boundaries for Marine Protected Areas

INSERT INTO mpas (mpa_name, boundary, protection_level, established_year) VALUES
(
    'South Water Caye Marine Reserve',
    ST_SetSRID(ST_GeomFromText('POLYGON((-88.10 16.80, -88.05 16.80, -88.05 16.85, -88.10 16.85, -88.10 16.80))'), 4326),
    'Managed Access',
    2010
),
(
    'Laughing Bird Caye National Park',
    ST_SetSRID(ST_GeomFromText('POLYGON((-88.20 16.44, -88.17 16.44, -88.17 16.46, -88.20 16.46, -88.20 16.44))'), 4326),
    'Full Protection',
    1991
);

-- ============================================================================
-- Insert Sample Outplanting History
-- ============================================================================
-- Coral outplanting records with species and location data

INSERT INTO outplanting_history (site_id, location, species, number_of_corals, outplanting_date, source_nursery, notes) VALUES
(
    1, -- Salt Water Caye
    ST_SetSRID(ST_MakePoint(-88.0820, 16.9890), 4326),
    'Acropora cervicornis',
    25,
    '2023-04-15',
    'Salt Water Caye Nursery',
    'First outplanting of the season, corals looking healthy'
),
(
    1, -- Salt Water Caye
    ST_SetSRID(ST_MakePoint(-88.0825, 16.9895), 4326),
    'Acropora palmata',
    30,
    '2023-05-20',
    'Salt Water Caye Nursery',
    'Outplanted near existing healthy reef'
),
(
    2, -- Laughing Bird Caye
    ST_SetSRID(ST_MakePoint(-88.1860, 16.4480), 4326),
    'Orbicella faveolata',
    15,
    '2023-06-10',
    'Laughing Bird Nursery',
    'Testing new species in this location'
);

-- ============================================================================
-- Insert Sample Photomosaics
-- ============================================================================
-- Photomosaic metadata with coverage area polygons

INSERT INTO photomosaics (site_id, coverage_area, capture_date, file_path, resolution, photographer, processing_notes) VALUES
(
    1, -- Salt Water Caye
    ST_SetSRID(ST_GeomFromText('POLYGON((-88.083 16.989, -88.082 16.989, -88.082 16.990, -88.083 16.990, -88.083 16.989))'), 4326),
    '2023-07-15',
    '/data/photomosaics/2023/swc_july_2023.tif',
    0.02,
    'Dr. Jane Smith',
    'Processed with Agisoft Metashape, excellent visibility conditions'
),
(
    2, -- Laughing Bird Caye
    ST_SetSRID(ST_GeomFromText('POLYGON((-88.187 16.447, -88.185 16.447, -88.185 16.449, -88.187 16.449, -88.187 16.447))'), 4326),
    '2023-08-20',
    '/data/photomosaics/2023/lbc_august_2023.tif',
    0.015,
    'Dr. Jane Smith',
    'High-resolution mosaic covering main reef area'
);

-- ============================================================================
-- Insert Sample Temperature Data
-- ============================================================================
-- Time-series temperature measurements

INSERT INTO temperature_data (site_id, recorded_at, temperature_celsius, depth_meters, sensor_id) VALUES
(1, '2023-09-01 08:00:00+00', 28.5, 5.0, 'HOBO-001'),
(1, '2023-09-01 12:00:00+00', 29.2, 5.0, 'HOBO-001'),
(1, '2023-09-01 16:00:00+00', 29.8, 5.0, 'HOBO-001'),
(1, '2023-09-02 08:00:00+00', 28.3, 5.0, 'HOBO-001'),
(2, '2023-09-01 08:00:00+00', 27.9, 8.0, 'HOBO-002'),
(2, '2023-09-01 12:00:00+00', 28.5, 8.0, 'HOBO-002'),
(2, '2023-09-01 16:00:00+00', 29.1, 8.0, 'HOBO-002'),
(3, '2023-09-01 08:00:00+00', 28.1, 6.5, 'HOBO-003'),
(3, '2023-09-01 12:00:00+00', 28.7, 6.5, 'HOBO-003');

-- ============================================================================
-- Insert Sample Growth Data
-- ============================================================================
-- Coral growth measurements over time

INSERT INTO growth_data (outplanting_id, measurement_date, size_cm, health_status, notes) VALUES
(1, '2023-05-15', 8.5, 'Healthy', 'One month post-outplanting, good tissue condition'),
(1, '2023-06-15', 9.2, 'Healthy', 'Two months post-outplanting, showing growth'),
(1, '2023-07-15', 10.1, 'Healthy', 'Three months post-outplanting, continued growth'),
(2, '2023-06-20', 7.8, 'Healthy', 'One month post-outplanting'),
(2, '2023-07-20', 8.6, 'Healthy', 'Two months post-outplanting, good color'),
(3, '2023-07-10', 12.3, 'Fair', 'One month post-outplanting, some bleaching observed'),
(3, '2023-08-10', 12.5, 'Fair', 'Two months post-outplanting, bleaching persists');

-- ============================================================================
-- Insert Sample Surveys
-- ============================================================================
-- Survey activities at sites

INSERT INTO surveys (site_id, survey_date, survey_type, surveyor_name, notes) VALUES
(
    1,
    '2023-07-15',
    'Photomosaic Survey',
    'Dr. Jane Smith',
    'Comprehensive photomosaic survey of entire restoration area'
),
(
    1,
    '2023-08-20',
    'Growth Monitoring',
    'John Doe',
    'Quarterly growth measurements of outplanted corals'
),
(
    2,
    '2023-08-25',
    'Baseline Survey',
    'Dr. Jane Smith',
    'Initial baseline survey for new monitoring area'
);

-- ============================================================================
-- Insert Sample Photos
-- ============================================================================
-- Photo metadata with GPS coordinates

INSERT INTO photos (survey_id, site_id, location, file_path, caption, taken_at, photographer) VALUES
(
    1,
    1,
    ST_SetSRID(ST_MakePoint(-88.0822, 16.9892), 4326),
    '/data/photos/2023/swc_survey_001.jpg',
    'Overview of outplanting site showing healthy coral growth',
    '2023-07-15 10:30:00+00',
    'Dr. Jane Smith'
),
(
    1,
    1,
    ST_SetSRID(ST_MakePoint(-88.0824, 16.9894), 4326),
    '/data/photos/2023/swc_survey_002.jpg',
    'Close-up of Acropora cervicornis fragment',
    '2023-07-15 11:00:00+00',
    'Dr. Jane Smith'
),
(
    2,
    1,
    ST_SetSRID(ST_MakePoint(-88.0821, 16.9891), 4326),
    '/data/photos/2023/swc_growth_001.jpg',
    'Measurement of coral fragment growth',
    '2023-08-20 09:15:00+00',
    'John Doe'
);

-- ============================================================================
-- Verification Queries
-- ============================================================================
-- Run these to verify the sample data was inserted correctly

-- Count records in each table
SELECT 'sites' AS table_name, COUNT(*) AS record_count FROM sites
UNION ALL
SELECT 'mpas', COUNT(*) FROM mpas
UNION ALL
SELECT 'outplanting_history', COUNT(*) FROM outplanting_history
UNION ALL
SELECT 'photomosaics', COUNT(*) FROM photomosaics
UNION ALL
SELECT 'temperature_data', COUNT(*) FROM temperature_data
UNION ALL
SELECT 'growth_data', COUNT(*) FROM growth_data
UNION ALL
SELECT 'surveys', COUNT(*) FROM surveys
UNION ALL
SELECT 'photos', COUNT(*) FROM photos;

-- Verify spatial data with coordinates
SELECT 
    site_name,
    ST_AsText(location) AS coordinates,
    ST_X(location) AS longitude,
    ST_Y(location) AS latitude
FROM sites;
