# FOH Database Setup Guide

## Overview
This directory contains the PostgreSQL/PostGIS database schema for the Fragments of Hope (FOH) coral reef monitoring system. The database is designed to store and manage geospatial data including coral reef sites, outplanting history, photomosaics, temperature data, and survey information.

## Database Architecture

### Tables
1. **sites** - Coral reef monitoring sites with GPS coordinates
2. **mpas** - Marine Protected Areas with polygon boundaries
3. **outplanting_history** - Coral outplanting records with location data
4. **photomosaics** - Photomosaic imagery metadata with coverage areas
5. **temperature_data** - Time-series temperature measurements
6. **growth_data** - Coral growth measurements over time
7. **surveys** - Survey activities at sites
8. **photos** - Photo metadata with GPS coordinates

### Key Features
- **PostGIS Integration**: All spatial data uses PostGIS geometry types with SRID 4326 (WGS84)
- **Spatial Indexes**: GIST indexes on all geometry columns for fast spatial queries
- **Foreign Key Constraints**: Maintains referential integrity between related tables
- **Automatic Timestamps**: Created_at and updated_at fields with automatic triggers
- **Data Validation**: CHECK constraints ensure data quality

## Prerequisites

### Required Software
- PostgreSQL 12+ 
- PostGIS 3.0+
- psql command-line tool (comes with PostgreSQL)

### Installation on Synology NAS
1. Open Package Center
2. Install PostgreSQL (version 12 or later recommended)
3. Install PostGIS extension through Package Center or manually

### Installation on Ubuntu/Debian
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib postgis
```

### Installation on macOS
```bash
brew install postgresql postgis
brew services start postgresql
```

## Database Setup

### Step 1: Create Database
```bash
# Connect to PostgreSQL as superuser
psql -U postgres

# Create the database
CREATE DATABASE foh_database;

# Connect to the new database
\c foh_database
```

### Step 2: Initialize PostGIS
Run the initialization script to enable PostGIS extension:
```bash
psql -U postgres -d foh_database -f init.sql
```

This will:
- Enable PostGIS extension
- Enable UUID extension
- Verify PostGIS installation

### Step 3: Create Schema
Run the schema script to create all tables:
```bash
psql -U postgres -d foh_database -f schema.sql
```

This will create:
- All 8 tables with proper relationships
- Foreign key constraints
- Check constraints
- Automatic timestamp triggers

### Step 4: Create Indexes
Run the indexes script to optimize query performance:
```bash
psql -U postgres -d foh_database -f indexes.sql
```

This will create:
- Spatial indexes (GIST) on all geometry columns
- Foreign key indexes for JOIN optimization
- Temporal indexes for time-based queries
- Text search indexes for name lookups
- Composite indexes for common query patterns

### Step 5: Load Sample Data
Load sample data for testing:
```bash
psql -U postgres -d foh_database -f sample_data.sql
```

This will insert:
- 3 sample sites
- 2 sample MPAs
- 3 outplanting records
- 2 photomosaics
- 9 temperature readings
- 7 growth measurements
- 3 surveys
- 3 photos

## All-in-One Setup
Run all setup scripts at once:
```bash
psql -U postgres -d foh_database -f init.sql
psql -U postgres -d foh_database -f schema.sql
psql -U postgres -d foh_database -f indexes.sql
psql -U postgres -d foh_database -f sample_data.sql
```

## Database Configuration

### Connection Settings
Edit `postgresql.conf` to allow network connections:
```ini
listen_addresses = '*'
port = 5432
max_connections = 100
```

### Authentication
Edit `pg_hba.conf` to configure access:
```
# Allow local connections
local   all             all                                     trust

# Allow network connections (adjust IP range as needed)
host    foh_database    foh_user        192.168.1.0/24         md5
```

### Create Database User
```sql
CREATE USER foh_user WITH PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE foh_database TO foh_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO foh_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO foh_user;
```

## Verification

### Check Tables
```sql
\dt
```

### Verify PostGIS
```sql
SELECT PostGIS_Version();
```

### Check Sample Data
```sql
-- Count records in each table
SELECT 'sites' AS table_name, COUNT(*) FROM sites
UNION ALL SELECT 'mpas', COUNT(*) FROM mpas
UNION ALL SELECT 'outplanting_history', COUNT(*) FROM outplanting_history
UNION ALL SELECT 'photomosaics', COUNT(*) FROM photomosaics
UNION ALL SELECT 'temperature_data', COUNT(*) FROM temperature_data
UNION ALL SELECT 'growth_data', COUNT(*) FROM growth_data
UNION ALL SELECT 'surveys', COUNT(*) FROM surveys
UNION ALL SELECT 'photos', COUNT(*) FROM photos;
```

### Verify Spatial Indexes
```sql
SELECT tablename, indexname, indexdef 
FROM pg_indexes 
WHERE schemaname = 'public' 
ORDER BY tablename, indexname;
```

## Useful Spatial Queries

### Find Sites Within Distance
```sql
-- Find all sites within 10 km of a point
SELECT site_name, 
       ST_Distance(location::geography, 
                  ST_SetSRID(ST_MakePoint(-88.0823, 16.9891), 4326)::geography) / 1000 AS distance_km
FROM sites
WHERE ST_DWithin(location::geography, 
                 ST_SetSRID(ST_MakePoint(-88.0823, 16.9891), 4326)::geography, 
                 10000);
```

### Find Sites Within MPA
```sql
-- Find all sites within a specific MPA
SELECT s.site_name, m.mpa_name
FROM sites s
JOIN mpas m ON ST_Within(s.location, m.boundary)
WHERE m.mpa_id = 1;
```

### Get Outplanting Locations as GeoJSON
```sql
SELECT jsonb_build_object(
    'type', 'FeatureCollection',
    'features', jsonb_agg(
        jsonb_build_object(
            'type', 'Feature',
            'geometry', ST_AsGeoJSON(location)::jsonb,
            'properties', jsonb_build_object(
                'outplanting_id', outplanting_id,
                'species', species,
                'number_of_corals', number_of_corals,
                'outplanting_date', outplanting_date
            )
        )
    )
) AS geojson
FROM outplanting_history;
```

## Backup and Restore

### Backup Database
```bash
pg_dump -U postgres -F c -f foh_backup.dump foh_database
```

### Restore Database
```bash
pg_restore -U postgres -d foh_database -c foh_backup.dump
```

### Backup Only Schema
```bash
pg_dump -U postgres -s -f foh_schema.sql foh_database
```

## Troubleshooting

### PostGIS Extension Not Found
```sql
-- Check available extensions
SELECT * FROM pg_available_extensions WHERE name LIKE '%postgis%';

-- Install PostGIS (if available)
CREATE EXTENSION postgis;
```

### Permission Denied Errors
```sql
-- Grant permissions to user
GRANT ALL PRIVILEGES ON DATABASE foh_database TO foh_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO foh_user;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO foh_user;
```

### Spatial Index Not Working
```sql
-- Rebuild spatial indexes
REINDEX INDEX idx_sites_location;
REINDEX INDEX idx_outplanting_location;

-- Update statistics
ANALYZE sites;
ANALYZE outplanting_history;
```

## Next Steps

1. **Backend API**: Set up the FastAPI backend in the `../backend/` directory
2. **Frontend**: Configure the web-based map interface in the `../frontend/` directory
3. **Docker**: Use `../docker-compose.yml` to run the full stack
4. **Data Import**: Import your real FOH data into the database

## Resources

- [PostGIS Documentation](https://postgis.net/documentation/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Spatial SQL Cheat Sheet](https://postgis.net/docs/reference.html)
- [GeoJSON Specification](https://geojson.org/)
