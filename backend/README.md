# FOH Backend API

## Overview
FastAPI-based REST API for the Fragments of Hope coral reef monitoring system. Provides geospatial data endpoints for sites, outplanting history, photomosaics, temperature data, and surveys.

## Architecture
This API is designed to run on a **Synology NAS** and serve data to a **PHP application hosted on Hostgator**.

```
┌─────────────────┐         ┌──────────────────┐         ┌─────────────────┐
│  Synology NAS   │         │   API Gateway    │         │   Hostgator     │
│                 │         │                  │         │                 │
│  PostgreSQL +   │◄────────│   FastAPI        │◄────────│  PHP App +      │
│  PostGIS        │         │   (Port 8000)    │         │  HTML/JS        │
└─────────────────┘         └──────────────────┘         └─────────────────┘
```

## Features
- ✅ RESTful API with GeoJSON responses
- ✅ PostGIS spatial queries (nearby, within MPA, distance)
- ✅ CORS enabled for cross-origin requests
- ✅ Automatic API documentation (Swagger/ReDoc)
- ✅ Connection pooling for performance
- ✅ Error handling and validation

## Installation

### Prerequisites
- Python 3.8+
- PostgreSQL 12+ with PostGIS extension
- pip (Python package manager)

### Setup Steps

1. **Install Python dependencies:**
```bash
cd backend
pip install -r requirements.txt
```

2. **Configure environment variables:**
Create a `.env` file in the backend directory:
```bash
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_NAME=foh_database
DATABASE_USER=postgres
DATABASE_PASSWORD=your_password
```

3. **Verify database connection:**
```bash
python -c "from database import engine; print(engine.connect())"
```

## Running the API

### Development Mode
```bash
cd backend
python app.py
```

Or with uvicorn directly:
```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

### Production Mode
```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --workers 4
```

### Using Gunicorn (recommended for production)
```bash
pip install gunicorn
gunicorn app:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## API Documentation

Once running, access interactive documentation at:
- **Swagger UI**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc
- **OpenAPI JSON**: http://localhost:8000/api/openapi.json

## API Endpoints

### Sites
- `GET /api/sites` - List all sites (GeoJSON)
- `GET /api/sites/{id}` - Get site by ID
- `POST /api/sites` - Create new site
- `PUT /api/sites/{id}` - Update site
- `DELETE /api/sites/{id}` - Delete site

### Photomosaics
- `GET /api/photomosaics` - List all photomosaics
- `GET /api/photomosaics/by-site/{site_id}` - Get by site

### Outplanting
- `GET /api/outplanting` - List all outplanting records (GeoJSON)
- `GET /api/outplanting/by-site/{site_id}` - Get by site
- `POST /api/outplanting` - Create outplanting record

### Temperature
- `GET /api/temperature/by-site/{site_id}` - Get temperature time series
- `POST /api/temperature` - Add temperature reading

### Surveys
- `GET /api/surveys` - List all surveys
- `GET /api/surveys/{id}` - Get survey with photos

### Spatial Queries
- `GET /api/spatial/nearby?lat={lat}&lon={lon}&radius={meters}` - Find within radius
- `GET /api/spatial/within-mpa/{mpa_id}` - Get data within MPA
- `GET /api/spatial/distance?lat1=...&lon1=...&lat2=...&lon2=...` - Calculate distance

## Consuming the API from PHP (Hostgator)

### Example 1: Get All Sites (GeoJSON)

```php
<?php
// API endpoint on Synology NAS
$api_url = 'http://your-synology-ip:8000/api/sites';

// Make GET request
$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, $api_url);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_HTTPHEADER, array('Content-Type: application/json'));

$response = curl_exec($ch);
$http_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
curl_close($ch);

if ($http_code == 200) {
    $geojson = json_decode($response, true);
    
    // Display sites on map
    foreach ($geojson['features'] as $feature) {
        $site_name = $feature['properties']['site_name'];
        $coordinates = $feature['geometry']['coordinates'];
        $lon = $coordinates[0];
        $lat = $coordinates[1];
        
        echo "Site: $site_name at ($lat, $lon)<br>";
    }
} else {
    echo "Error: Unable to fetch sites";
}
?>
```

### Example 2: Get Temperature Data for a Site

```php
<?php
$site_id = 1;
$api_url = "http://your-synology-ip:8000/api/temperature/by-site/$site_id";

$response = file_get_contents($api_url);
$data = json_decode($response, true);

echo "<h2>Temperature Data for Site {$data['site_id']}</h2>";
echo "<p>Total readings: {$data['count']}</p>";

echo "<table border='1'>
<tr>
    <th>Date/Time</th>
    <th>Temperature (°C)</th>
    <th>Depth (m)</th>
</tr>";

foreach ($data['data'] as $reading) {
    $datetime = date('Y-m-d H:i', strtotime($reading['recorded_at']));
    $temp = number_format($reading['temperature_celsius'], 1);
    $depth = number_format($reading['depth_meters'], 1);
    
    echo "<tr>
        <td>$datetime</td>
        <td>$temp</td>
        <td>$depth</td>
    </tr>";
}

echo "</table>";
?>
```

### Example 3: Find Nearby Sites (Spatial Query)

```php
<?php
// Search within 10km of a point
$lat = 16.9891;
$lon = -88.0823;
$radius = 10000; // meters

$api_url = "http://your-synology-ip:8000/api/spatial/nearby?latitude=$lat&longitude=$lon&radius=$radius";

$response = file_get_contents($api_url);
$data = json_decode($response, true);

echo "<h2>Sites within {$data['radius_meters']}m</h2>";

// Display sites
$sites = $data['results']['sites']['features'];
echo "<p>Found " . count($sites) . " sites</p>";

foreach ($sites as $site) {
    $name = $site['properties']['site_name'];
    $coords = $site['geometry']['coordinates'];
    echo "- $name at ({$coords[1]}, {$coords[0]})<br>";
}
?>
```

### Example 4: Create New Outplanting Record (POST)

```php
<?php
// Data for new outplanting record
$data = array(
    'site_id' => 1,
    'latitude' => 16.9890,
    'longitude' => -88.0820,
    'species' => 'Acropora cervicornis',
    'number_of_corals' => 25,
    'outplanting_date' => '2024-01-15',
    'source_nursery' => 'Salt Water Caye Nursery',
    'notes' => 'Healthy specimens from nursery'
);

$api_url = 'http://your-synology-ip:8000/api/outplanting';

// Prepare POST request
$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, $api_url . '?' . http_build_query($data));
curl_setopt($ch, CURLOPT_POST, true);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_HTTPHEADER, array('Content-Type: application/json'));

$response = curl_exec($ch);
$http_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
curl_close($ch);

if ($http_code == 201) {
    echo "Outplanting record created successfully!";
    $result = json_decode($response, true);
    echo "<pre>" . print_r($result, true) . "</pre>";
} else {
    echo "Error creating record: HTTP $http_code";
}
?>
```

### Example 5: Error Handling

```php
<?php
function fetchFromAPI($endpoint) {
    $api_base = 'http://your-synology-ip:8000';
    $url = $api_base . $endpoint;
    
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_TIMEOUT, 30);
    
    $response = curl_exec($ch);
    $http_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    $error = curl_error($ch);
    curl_close($ch);
    
    if ($error) {
        return array('error' => "cURL Error: $error");
    }
    
    if ($http_code != 200) {
        return array('error' => "HTTP Error: $http_code");
    }
    
    return json_decode($response, true);
}

// Usage
$sites = fetchFromAPI('/api/sites');

if (isset($sites['error'])) {
    echo "Error: {$sites['error']}";
} else {
    // Process sites
    echo "Loaded " . count($sites['features']) . " sites";
}
?>
```

## Network Configuration for Synology → Hostgator

### 1. Configure Synology Firewall
Allow incoming connections on port 8000:
- Control Panel → Security → Firewall
- Add rule: Allow TCP port 8000

### 2. Setup Port Forwarding (if needed)
If API needs to be accessible from internet:
- Router settings → Port Forwarding
- Forward external port (e.g., 8000) to Synology IP:8000

### 3. Use HTTPS (Recommended)
Set up reverse proxy with SSL:
- Control Panel → Application Portal → Reverse Proxy
- Create rule for port 8000 with SSL certificate

### 4. Update CORS in backend/config.py
```python
CORS_ORIGINS: list = [
    "https://your-hostgator-domain.com",
    "http://your-hostgator-domain.com",
]
```

## Testing the API

### Using curl
```bash
# Get all sites
curl http://localhost:8000/api/sites

# Get specific site
curl http://localhost:8000/api/sites/1

# Create new site
curl -X POST "http://localhost:8000/api/sites?site_name=Test%20Site&latitude=16.5&longitude=-88.0"

# Spatial query
curl "http://localhost:8000/api/spatial/nearby?latitude=16.99&longitude=-88.08&radius=5000"
```

### Using Python
```python
import requests

# Get sites as GeoJSON
response = requests.get('http://localhost:8000/api/sites')
sites = response.json()

for feature in sites['features']:
    print(f"Site: {feature['properties']['site_name']}")
```

## Deployment on Synology NAS

### Option 1: Run as Background Service
Create a startup script:
```bash
#!/bin/bash
cd /volume1/FOH/backend
source venv/bin/activate
gunicorn app:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000 --daemon
```

### Option 2: Use Systemd (if available)
Create `/etc/systemd/system/foh-api.service`:
```ini
[Unit]
Description=FOH API Service
After=network.target

[Service]
Type=simple
User=your-user
WorkingDirectory=/volume1/FOH/backend
ExecStart=/usr/bin/python3 app.py
Restart=always

[Install]
WantedBy=multi-user.target
```

### Option 3: Use Docker (see docker-compose.yml)

## Monitoring and Logs

### View API logs
```bash
tail -f /var/log/foh-api.log
```

### Health check endpoint
```bash
curl http://localhost:8000/api/health
```

## Security Best Practices

1. **Use environment variables** for sensitive data (don't hardcode passwords)
2. **Enable HTTPS** with SSL certificates
3. **Restrict CORS** to specific Hostgator domain
4. **Use database user** with limited permissions (not postgres superuser)
5. **Implement rate limiting** to prevent abuse
6. **Add authentication** for write operations (POST, PUT, DELETE)

## Troubleshooting

### Can't connect to database
```bash
# Test connection
psql -h localhost -U postgres -d foh_database -c "SELECT PostGIS_Version();"
```

### CORS errors from PHP app
- Add Hostgator domain to CORS_ORIGINS in config.py
- Check that API is accessible from Hostgator server

### Import errors
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

## Performance Optimization

### Connection Pooling
Already configured in `database.py`:
- pool_size=10 (10 connections)
- max_overflow=20 (up to 30 total)

### Caching (Optional)
Install Redis caching:
```bash
pip install fastapi-cache2 redis
```

## Support
For issues or questions, see the main repository README.
