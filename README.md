# Fragments of Hope (FOH) - Coral Reef Monitoring System

A comprehensive geospatial database and visualization platform for managing coral reef restoration data, including monitoring sites, outplanting history, photomosaics, temperature data, and surveys.

## 🌊 Overview

This system provides a complete solution for managing and visualizing coral reef data:
- **PostgreSQL/PostGIS Database** - Spatial database for geospatial data
- **FastAPI Backend** - RESTful API with GeoJSON support
- **Interactive Frontend** - Web-based map visualization with Leaflet.js
- **Docker Support** - Easy deployment with Docker Compose

## 🏗️ Architecture

```
┌─────────────────┐         ┌──────────────────┐         ┌─────────────────┐
│  Synology NAS   │         │   FastAPI        │         │   Hostgator     │
│                 │         │   Backend        │         │                 │
│  PostgreSQL +   │◄────────│   (Port 8000)    │◄────────│  PHP App +      │
│  PostGIS        │         │   REST API       │         │  Web Frontend   │
│  (Port 5432)    │         │   + CORS         │         │  (Port 80/443)  │
└─────────────────┘         └──────────────────┘         └─────────────────┘
        │                            │                             │
        └────────────────────────────┴─────────────────────────────┘
                      GeoJSON Data Flow
```

## 📦 Project Structure

```
FOH/
├── database/              # PostgreSQL/PostGIS schema and data
│   ├── init.sql          # PostGIS initialization
│   ├── schema.sql        # Table definitions
│   ├── indexes.sql       # Spatial indexes
│   ├── sample_data.sql   # Test data
│   └── README.md         # Database documentation
├── backend/               # FastAPI REST API
│   ├── app.py            # Main application
│   ├── config.py         # Configuration
│   ├── database.py       # DB connection
│   ├── models.py         # SQLAlchemy models
│   ├── routes/           # API endpoints
│   ├── utils/            # Helper functions
│   ├── requirements.txt  # Python dependencies
│   └── README.md         # API documentation
├── frontend/              # Web visualization
│   ├── index.html        # Main page
│   ├── css/              # Styles
│   ├── js/               # JavaScript modules
│   │   ├── api.js       # API client
│   │   ├── map.js       # Map logic
│   │   ├── popup.js     # Popups
│   │   └── charts.js    # Visualizations
│   └── README.md         # Frontend documentation
├── docker-compose.yml     # Docker orchestration
├── .env.example          # Environment template
└── README.md             # This file
```

## 🚀 Quick Start

### Option 1: Docker Compose (Recommended)

1. **Clone the repository:**
```bash
git clone https://github.com/kylonnealbze/FOH.git
cd FOH
```

2. **Create environment file:**
```bash
cp .env.example .env
# Edit .env with your settings
```

3. **Start all services:**
```bash
docker-compose up -d
```

4. **Access the application:**
- Frontend: http://localhost:8080
- API Docs: http://localhost:8000/api/docs
- Database: localhost:5432

### Option 2: Manual Installation

#### Step 1: Database Setup

```bash
# Install PostgreSQL and PostGIS
sudo apt-get install postgresql postgis

# Create database
createdb foh_database

# Initialize schema
cd database
psql -d foh_database -f init.sql
psql -d foh_database -f schema.sql
psql -d foh_database -f indexes.sql
psql -d foh_database -f sample_data.sql
```

See `database/README.md` for detailed instructions.

#### Step 2: Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
export DATABASE_HOST=localhost
export DATABASE_NAME=foh_database
export DATABASE_USER=postgres
export DATABASE_PASSWORD=your_password

# Run API
python app.py
```

API will be available at http://localhost:8000

See `backend/README.md` for detailed instructions and PHP examples.

#### Step 3: Frontend Setup

```bash
cd frontend

# Serve static files with Python
python -m http.server 8080

# Or with Node.js
npx http-server -p 8080
```

Frontend will be available at http://localhost:8080

See `frontend/README.md` for detailed instructions.

## 🔧 Configuration

### Database Configuration

Edit PostgreSQL connection in `.env` or `backend/config.py`:
```python
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_NAME=foh_database
DATABASE_USER=postgres
DATABASE_PASSWORD=your_secure_password
```

### API Configuration

Configure CORS for Hostgator access in `backend/config.py`:
```python
CORS_ORIGINS: list = [
    "https://your-domain.com",
    "http://localhost:8080",
]
```

### Frontend Configuration

Update API endpoint in `frontend/js/api.js`:
```javascript
const API_CONFIG = {
    baseURL: 'http://your-synology-ip:8000',
    timeout: 30000
};
```

## 📊 Database Schema

The system includes 8 main tables:

1. **sites** - Monitoring sites with GPS coordinates
2. **mpas** - Marine Protected Areas with polygon boundaries
3. **outplanting_history** - Coral outplanting records
4. **photomosaics** - Photomosaic imagery metadata
5. **temperature_data** - Time-series temperature measurements
6. **growth_data** - Coral growth tracking
7. **surveys** - Survey activities
8. **photos** - Photo metadata with GPS tags

All spatial data uses **SRID 4326 (WGS84)** for GPS compatibility.

See `database/README.md` for complete schema documentation.

## 🌐 API Endpoints

### Core Endpoints
- `GET /api/sites` - List all sites (GeoJSON)
- `GET /api/outplanting` - List outplanting records
- `GET /api/photomosaics` - List photomosaics
- `GET /api/temperature/by-site/{id}` - Temperature data
- `GET /api/surveys` - List surveys

### Spatial Queries
- `GET /api/spatial/nearby?lat=...&lon=...&radius=...` - Find within radius
- `GET /api/spatial/within-mpa/{id}` - Data within MPA
- `GET /api/spatial/distance?lat1=...&lon1=...&lat2=...&lon2=...` - Calculate distance

See `backend/README.md` for complete API documentation with PHP examples.

## 🖥️ Deployment

### Deploying on Synology NAS

1. **Install PostgreSQL package** from Package Center
2. **Install Python 3** via Package Center or SSH
3. **Clone repository** to shared folder (e.g., `/volume1/FOH`)
4. **Setup database** using SQL scripts
5. **Run backend** as background service or Docker container
6. **Configure port forwarding** for external access

### Deploying Frontend on Hostgator

1. **Upload files** via FTP/SFTP or cPanel File Manager
2. **Update API URL** in `frontend/js/api.js`
3. **Configure CORS** in backend to allow Hostgator domain
4. **Test connection** from browser

#### Example PHP Integration

```php
<?php
// Fetch data from Synology API
$api_url = 'http://your-synology-ip:8000/api/sites';
$sites = json_decode(file_get_contents($api_url), true);

// Display sites
foreach ($sites['features'] as $feature) {
    $name = $feature['properties']['site_name'];
    $coords = $feature['geometry']['coordinates'];
    echo "$name at ({$coords[1]}, {$coords[0]})<br>";
}
?>
```

See `backend/README.md` for complete PHP examples.

## 🔒 Security

- Store credentials in `.env` file (never commit to Git)
- Use HTTPS in production
- Configure CORS to specific domains only
- Use database user with limited permissions
- Enable firewall rules on Synology NAS
- Consider API authentication for write operations

## 🧪 Testing

### Test Database Connection
```bash
psql -h localhost -U postgres -d foh_database -c "SELECT PostGIS_Version();"
```

### Test API
```bash
curl http://localhost:8000/api/sites
curl http://localhost:8000/api/health
```

### Test Frontend
Open http://localhost:8080 in browser and verify map loads.

## 📱 Features

### Interactive Map
- ✅ Pan, zoom, and click interactions
- ✅ Multiple data layers (sites, MPAs, outplanting, photomosaics)
- ✅ Custom markers and polygons
- ✅ Popup details for features

### Data Visualization
- ✅ Temperature time-series charts
- ✅ Coral growth trends
- ✅ Species distribution

### Search & Filter
- ✅ Search sites by name
- ✅ Filter by species
- ✅ Filter by date range
- ✅ Spatial search (find within radius)

### GeoJSON Support
- ✅ All spatial endpoints return GeoJSON
- ✅ Compatible with mapping libraries
- ✅ Easy integration with GIS tools

## 🛠️ Technology Stack

**Database:**
- PostgreSQL 12+
- PostGIS 3.0+

**Backend:**
- Python 3.8+
- FastAPI
- SQLAlchemy + GeoAlchemy2
- psycopg2

**Frontend:**
- HTML5/CSS3/JavaScript
- Leaflet.js 1.9.4
- Chart.js 4.4.1

**Deployment:**
- Docker & Docker Compose
- Nginx (for frontend)
- Uvicorn/Gunicorn (for API)

## 📖 Documentation

- [Database Documentation](database/README.md) - Schema, setup, and SQL examples
- [Backend Documentation](backend/README.md) - API reference and PHP examples
- [Frontend Documentation](frontend/README.md) - Usage guide and customization

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is part of the Fragments of Hope coral reef restoration initiative.

## 🐛 Troubleshooting

### Database won't connect
- Check PostgreSQL is running: `sudo systemctl status postgresql`
- Verify credentials in `.env`
- Check `pg_hba.conf` allows connections

### API returns CORS errors
- Add your domain to `CORS_ORIGINS` in `backend/config.py`
- Restart API server after changes

### Frontend shows no data
- Verify API is running: http://localhost:8000/api/health
- Check browser console for errors
- Verify API URL in `frontend/js/api.js`

### Docker containers won't start
- Check logs: `docker-compose logs`
- Verify ports aren't already in use
- Ensure `.env` file exists

## 📞 Support

For questions or issues:
1. Check the documentation in each directory
2. Review error messages in browser console or server logs
3. Verify all services are running
4. Check network connectivity between components

## 🗺️ Sample Data

The system includes sample data for Belize coral reef sites:
- 3 monitoring sites (Salt Water Caye, Laughing Bird Caye, South Water Caye)
- 2 Marine Protected Areas
- Outplanting records with various coral species
- Temperature readings
- Survey data with photos

Load sample data: `psql -d foh_database -f database/sample_data.sql`

## PostgreSQL/PostGIS Background

### Why Use PostgreSQL + PostGIS?
PostgreSQL is a powerful, open-source relational database system that can handle a variety of data types. When combined with PostGIS, it becomes a robust platform for storing and analyzing geospatial data, making it particularly well-suited for coral reef data that involves geographic coordinates and spatial analysis.

### PostGIS Extension Setup
```sql
CREATE EXTENSION postgis;
SELECT PostGIS_Version();
```

### Connection Examples
```python
import psycopg2

connection = psycopg2.connect(
    host="your_host",
    database="foh_database",
    user="your_user",
    password="your_password"
)
```
