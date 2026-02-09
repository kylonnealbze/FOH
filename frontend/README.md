# FOH Frontend - Coral Reef Data Viewer

## Overview
Interactive web-based mapping interface for visualizing and exploring coral reef monitoring data from the Fragments of Hope project. Built with Leaflet.js for mapping, Chart.js for data visualization, and vanilla JavaScript for interactivity.

## Features

### 🗺️ Interactive Map
- **Leaflet.js** powered mapping with OpenStreetMap base layer
- Pan, zoom, and click interactions
- Responsive design for desktop, tablet, and mobile

### 📍 Data Layers
- **Monitoring Sites** - Coral reef monitoring locations
- **Marine Protected Areas (MPAs)** - Protected area boundaries
- **Coral Outplanting** - Individual outplanting locations with species info
- **Photomosaics** - Coverage areas of aerial/underwater imagery
- **Photos** - Geotagged photo locations

### 🔍 Search & Filter
- **Text Search** - Find sites by name
- **Species Filter** - Filter outplanting by coral species
- **Date Range Filter** - Filter data by temporal range
- **Spatial Search** - Find data within radius of a point

### 📊 Data Visualization
- **Temperature Charts** - Time-series line charts for temperature data
- **Growth Trends** - Coral growth over time
- **Popup Details** - Click features for detailed information

### 🎨 User Interface
- Clean, modern design with sidebar controls
- Layer toggle switches
- Information panel for feature details
- Loading indicators
- Responsive layout

## Architecture

### File Structure
```
frontend/
├── index.html              # Main HTML page
├── css/
│   └── styles.css         # All CSS styling
├── js/
│   ├── api.js             # API communication layer
│   ├── map.js             # Map initialization and layer management
│   ├── popup.js           # Popup content generation
│   └── charts.js          # Chart.js data visualization
└── assets/
    └── icons/             # Custom marker icons (optional)
```

### Technology Stack
- **Leaflet.js 1.9.4** - Interactive maps
- **Chart.js 4.4.1** - Data visualization
- **Vanilla JavaScript** - No framework dependencies
- **HTML5/CSS3** - Modern web standards

## Setup and Configuration

### 1. Basic Setup (Static Files)

The frontend can be served as static files from any web server.

#### Option A: Local Development
```bash
cd frontend
python -m http.server 8080
```
Then open http://localhost:8080 in your browser.

#### Option B: Node.js Server
```bash
npx http-server frontend -p 8080
```

#### Option C: PHP Built-in Server (Hostgator)
```bash
php -S localhost:8080 -t frontend
```

### 2. Configure API Connection

Edit `frontend/js/api.js` and update the API base URL:

```javascript
const API_CONFIG = {
    baseURL: 'http://your-synology-ip:8000',
    timeout: 30000
};
```

For production on Hostgator, use your Synology's public IP or domain:
```javascript
const API_CONFIG = {
    baseURL: 'https://your-synology-domain.com:8000',
    timeout: 30000
};
```

### 3. Deploy to Hostgator

#### Using FTP/SFTP:
1. Connect to your Hostgator account via FTP
2. Navigate to `public_html` (or your domain directory)
3. Upload all files from the `frontend/` directory

#### Using cPanel File Manager:
1. Log into cPanel
2. Open File Manager
3. Navigate to `public_html`
4. Upload frontend files
5. Extract if uploaded as ZIP

#### File Permissions:
```bash
# Set appropriate permissions
chmod 644 index.html
chmod 644 css/*.css
chmod 644 js/*.js
chmod 755 assets
```

### 4. Configure CORS (if needed)

If you encounter CORS errors, ensure your backend API has proper CORS headers configured (already done in `backend/config.py`).

Alternatively, create a PHP proxy on Hostgator:

Create `api_proxy.php`:
```php
<?php
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST, PUT, DELETE');
header('Access-Control-Allow-Headers: Content-Type');

$api_base = 'http://your-synology-ip:8000';
$endpoint = $_GET['endpoint'] ?? '/';

$url = $api_base . $endpoint;
$response = file_get_contents($url);

echo $response;
?>
```

Then update `api.js` to use the proxy:
```javascript
const API_CONFIG = {
    baseURL: '/api_proxy.php?endpoint=',
    timeout: 30000
};
```

## Usage Guide

### Viewing Data

1. **Load the Map**
   - Open `index.html` in a web browser
   - Map loads centered on Belize (16.8°N, 88.1°W)
   - Sites layer loads automatically

2. **Toggle Layers**
   - Use checkboxes in sidebar to show/hide layers
   - Sites and MPAs are visible by default
   - Enable other layers as needed

3. **Click Features**
   - Click any marker or polygon
   - Popup appears with feature details
   - Buttons in popup provide additional actions

4. **Search Sites**
   - Enter site name in search box
   - Press Enter or click Search button
   - Matching sites are highlighted

5. **Filter Data**
   - Select species from dropdown
   - Set date range
   - Click "Apply Filters"

6. **Spatial Search**
   - Enter radius in meters
   - Click "Search Map Center"
   - Results shown within radius

### Viewing Details

**Site Details:**
- Click site marker → "View Details" button
- Information panel updates with full details
- "Temperature Data" button shows chart

**Temperature Charts:**
- Click "Temperature Data" button in site popup
- Chart appears in bottom of sidebar
- Shows time-series temperature readings

**Outplanting Info:**
- Enable outplanting layer
- Click coral marker
- View species, date, count, and notes

**Photomosaics:**
- Enable photomosaic layer
- Colored polygons show coverage areas
- Click for capture date and photographer

## Customization

### Change Base Map

Edit `frontend/js/map.js`:

```javascript
// Satellite imagery
L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
    attribution: 'Tiles &copy; Esri',
    maxZoom: 18
}).addTo(map);

// Dark mode
L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
    attribution: '&copy; OpenStreetMap contributors &copy; CARTO',
    maxZoom: 19
}).addTo(map);
```

### Customize Marker Colors

Edit marker styles in `frontend/js/map.js`:

```javascript
// Sites - change fillColor
fillColor: '#0077be',  // Your custom color

// Outplanting
fillColor: '#20b2aa',  // Your custom color

// Photomosaic polygons
color: '#ff6b6b',      // Your custom color
```

### Add Custom Marker Icons

Create icon files in `assets/icons/` and update the marker creation:

```javascript
const customIcon = L.icon({
    iconUrl: 'assets/icons/site-marker.png',
    iconSize: [32, 32],
    iconAnchor: [16, 32],
    popupAnchor: [0, -32]
});

L.marker(latlng, { icon: customIcon });
```

### Modify Chart Appearance

Edit `frontend/js/charts.js` to customize Chart.js options:

```javascript
// Change colors
borderColor: 'rgb(0, 119, 190)',
backgroundColor: 'rgba(0, 119, 190, 0.1)',

// Change chart type
type: 'bar',  // or 'line', 'pie', etc.
```

## Integration with PHP (Hostgator)

### Example: Embedding in PHP Page

```php
<!DOCTYPE html>
<html>
<head>
    <title>FOH Data Viewer</title>
    <?php include 'includes/header.php'; ?>
</head>
<body>
    <?php include 'includes/nav.php'; ?>
    
    <!-- Embed the map -->
    <div style="height: 600px;">
        <iframe src="/map-viewer/index.html" 
                style="width: 100%; height: 100%; border: none;">
        </iframe>
    </div>
    
    <?php include 'includes/footer.php'; ?>
</body>
</html>
```

### Example: PHP Template with Map

```php
<?php
// Get site ID from URL
$site_id = $_GET['site_id'] ?? 1;

// Fetch site data from API
$api_url = "http://your-synology-ip:8000/api/sites/$site_id";
$site_data = json_decode(file_get_contents($api_url), true);

$site_name = $site_data['properties']['site_name'];
$lat = $site_data['geometry']['coordinates'][1];
$lon = $site_data['geometry']['coordinates'][0];
?>

<!DOCTYPE html>
<html>
<head>
    <title><?php echo $site_name; ?> - FOH Data</title>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
</head>
<body>
    <h1><?php echo $site_name; ?></h1>
    
    <div id="map" style="height: 400px;"></div>
    
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <script>
        const map = L.map('map').setView([<?php echo $lat; ?>, <?php echo $lon; ?>], 13);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);
        L.marker([<?php echo $lat; ?>, <?php echo $lon; ?>])
            .addTo(map)
            .bindPopup('<?php echo $site_name; ?>');
    </script>
</body>
</html>
```

## Browser Support

- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Edge 90+
- ✅ Mobile browsers (iOS Safari, Chrome Mobile)

## Performance Optimization

### Lazy Loading
Layers only load when enabled:
```javascript
if (e.target.checked) {
    loadOutplanting();  // Only loads when checkbox is checked
}
```

### Data Pagination
Limit results for large datasets:
```javascript
await API.getSites({ limit: 100 });
```

### Caching
Browser automatically caches map tiles and API responses.

## Troubleshooting

### Map Not Loading
- Check browser console for errors
- Verify internet connection (Leaflet loads from CDN)
- Check that `index.html` is being served properly

### No Data Appearing
- Check API connection in `js/api.js`
- Verify API is running: http://your-synology-ip:8000/api/health
- Check browser console for API errors
- Verify CORS is enabled on backend

### CORS Errors
- Update CORS_ORIGINS in `backend/config.py`
- Use PHP proxy (see Configuration section)
- Ensure API allows your domain

### Slow Performance
- Reduce data returned from API (pagination)
- Disable unused layers
- Consider clustering for large datasets

## Future Enhancements

Potential improvements:
- [ ] Marker clustering for better performance with many points
- [ ] Drawing tools for creating new features
- [ ] Export data as CSV/GeoJSON
- [ ] Heatmap visualization for temperature data
- [ ] Animation of time-series data
- [ ] 3D terrain visualization
- [ ] Offline support with service workers
- [ ] Print/export map functionality

## Development

### Adding a New Layer

1. Add checkbox to `index.html`:
```html
<label class="layer-toggle">
    <input type="checkbox" id="new-layer">
    New Layer
</label>
```

2. Create layer group in `map.js`:
```javascript
layerGroups.newLayer = L.layerGroup();
```

3. Add event listener:
```javascript
document.getElementById('new-layer').addEventListener('change', (e) => {
    if (e.target.checked) loadNewLayer();
    toggleLayer('newLayer', e.target.checked);
});
```

4. Create load function:
```javascript
async function loadNewLayer() {
    const data = await API.getNewData();
    // Add to map...
}
```

## Support

For issues or questions:
- Check browser console for errors
- Review API documentation in `backend/README.md`
- Ensure database is running with sample data

## License

Part of the Fragments of Hope (FOH) coral reef monitoring project.
