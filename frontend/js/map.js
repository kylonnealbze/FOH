/**
 * Map Module
 * Main map initialization and layer management
 */

let map;
let layerGroups = {
    sites: null,
    mpas: null,
    outplanting: null,
    photomosaics: null,
    photos: null
};

let searchMarker = null;

/**
 * Initialize the Leaflet map
 */
function initializeMap() {
    // Create map centered on Belize
    map = L.map('map').setView([16.8, -88.1], 10);
    
    // Add OpenStreetMap base layer
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors',
        maxZoom: 19
    }).addTo(map);
    
    // Alternative: Satellite imagery (uncomment to use)
    // L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
    //     attribution: 'Tiles &copy; Esri',
    //     maxZoom: 18
    // }).addTo(map);
    
    // Initialize layer groups
    layerGroups.sites = L.layerGroup().addTo(map);
    layerGroups.mpas = L.layerGroup().addTo(map);
    layerGroups.outplanting = L.layerGroup();
    layerGroups.photomosaics = L.layerGroup();
    layerGroups.photos = L.layerGroup();
    
    // Load initial data
    loadAllLayers();
    
    // Setup event listeners
    setupEventListeners();
    
    // Add scale control
    L.control.scale({ imperial: false, metric: true }).addTo(map);
    
    console.log('Map initialized successfully');
}

/**
 * Setup event listeners for UI controls
 */
function setupEventListeners() {
    // Layer toggles
    document.getElementById('sites-layer').addEventListener('change', (e) => {
        toggleLayer('sites', e.target.checked);
    });
    
    document.getElementById('mpa-layer').addEventListener('change', (e) => {
        toggleLayer('mpas', e.target.checked);
    });
    
    document.getElementById('outplanting-layer').addEventListener('change', (e) => {
        if (e.target.checked) {
            loadOutplanting();
        }
        toggleLayer('outplanting', e.target.checked);
    });
    
    document.getElementById('photomosaic-layer').addEventListener('change', (e) => {
        if (e.target.checked) {
            loadPhotomosaics();
        }
        toggleLayer('photomosaics', e.target.checked);
    });
    
    document.getElementById('photos-layer').addEventListener('change', (e) => {
        if (e.target.checked) {
            loadPhotos();
        }
        toggleLayer('photos', e.target.checked);
    });
    
    // Search button
    document.getElementById('search-btn').addEventListener('click', searchSites);
    document.getElementById('site-search').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') searchSites();
    });
    
    // Filter buttons
    document.getElementById('apply-filters').addEventListener('click', applyFilters);
    document.getElementById('clear-filters').addEventListener('click', clearFilters);
    
    // Spatial search
    document.getElementById('spatial-search-btn').addEventListener('click', performSpatialSearch);
    
    // Map click for spatial search
    map.on('click', onMapClick);
}

/**
 * Load all initial layers
 */
async function loadAllLayers() {
    try {
        await Promise.all([
            loadSites(),
            // MPAs would be loaded here if we had the endpoint
            // loadMPAs()
        ]);
    } catch (error) {
        console.error('Error loading layers:', error);
    }
}

/**
 * Load sites layer
 */
async function loadSites() {
    try {
        const geojson = await API.getSites();
        
        layerGroups.sites.clearLayers();
        
        L.geoJSON(geojson, {
            pointToLayer: (feature, latlng) => {
                return L.circleMarker(latlng, {
                    radius: 8,
                    fillColor: '#0077be',
                    color: '#fff',
                    weight: 2,
                    opacity: 1,
                    fillOpacity: 0.8
                });
            },
            onEachFeature: (feature, layer) => {
                const popupContent = PopupHelpers.createSitePopup(feature.properties);
                layer.bindPopup(popupContent);
                
                layer.on('click', () => {
                    PopupHelpers.updateInfoPanel(
                        `Site: ${feature.properties.site_name}`,
                        `<p>Click "View Details" in the popup for more information.</p>`
                    );
                });
            }
        }).addTo(layerGroups.sites);
        
        console.log(`Loaded ${geojson.features.length} sites`);
    } catch (error) {
        console.error('Error loading sites:', error);
    }
}

/**
 * Load outplanting layer
 */
async function loadOutplanting() {
    try {
        const speciesFilter = document.getElementById('species-filter').value;
        const geojson = await API.getOutplanting(speciesFilter || null);
        
        layerGroups.outplanting.clearLayers();
        
        L.geoJSON(geojson, {
            pointToLayer: (feature, latlng) => {
                return L.circleMarker(latlng, {
                    radius: 6,
                    fillColor: '#20b2aa',
                    color: '#fff',
                    weight: 2,
                    opacity: 1,
                    fillOpacity: 0.7
                });
            },
            onEachFeature: (feature, layer) => {
                const popupContent = PopupHelpers.createOutplantingPopup(feature.properties);
                layer.bindPopup(popupContent);
            }
        }).addTo(layerGroups.outplanting);
        
        console.log(`Loaded ${geojson.features.length} outplanting records`);
    } catch (error) {
        console.error('Error loading outplanting:', error);
    }
}

/**
 * Load photomosaics layer
 */
async function loadPhotomosaics() {
    try {
        const geojson = await API.getPhotomosaics();
        
        layerGroups.photomosaics.clearLayers();
        
        L.geoJSON(geojson, {
            style: {
                color: '#ff6b6b',
                weight: 2,
                opacity: 0.7,
                fillOpacity: 0.2
            },
            onEachFeature: (feature, layer) => {
                const popupContent = PopupHelpers.createPhotomosaicPopup(feature.properties);
                layer.bindPopup(popupContent);
            }
        }).addTo(layerGroups.photomosaics);
        
        console.log(`Loaded ${geojson.features.length} photomosaics`);
    } catch (error) {
        console.error('Error loading photomosaics:', error);
    }
}

/**
 * Load photos layer (stub - would need API endpoint)
 */
async function loadPhotos() {
    console.log('Photos layer - API endpoint not yet implemented');
    // This would call API.getPhotos() when available
}

/**
 * Toggle layer visibility
 */
function toggleLayer(layerName, visible) {
    if (visible) {
        if (!map.hasLayer(layerGroups[layerName])) {
            layerGroups[layerName].addTo(map);
        }
    } else {
        if (map.hasLayer(layerGroups[layerName])) {
            map.removeLayer(layerGroups[layerName]);
        }
    }
}

/**
 * Search sites by name
 */
function searchSites() {
    const searchTerm = document.getElementById('site-search').value.toLowerCase();
    
    if (!searchTerm) {
        loadSites(); // Reload all sites
        return;
    }
    
    // Filter sites on the map
    layerGroups.sites.eachLayer(layer => {
        if (layer.feature) {
            const siteName = layer.feature.properties.site_name.toLowerCase();
            if (siteName.includes(searchTerm)) {
                layer.setStyle({ fillOpacity: 0.8, opacity: 1 });
                // Optionally zoom to matching site
                if (layerGroups.sites.getLayers().length === 1) {
                    map.setView(layer.getLatLng(), 13);
                    layer.openPopup();
                }
            } else {
                layer.setStyle({ fillOpacity: 0.2, opacity: 0.3 });
            }
        }
    });
}

/**
 * Apply filters
 */
function applyFilters() {
    const dateFrom = document.getElementById('date-from').value;
    const dateTo = document.getElementById('date-to').value;
    const species = document.getElementById('species-filter').value;
    
    console.log('Applying filters:', { dateFrom, dateTo, species });
    
    // Reload layers with filters
    if (document.getElementById('outplanting-layer').checked) {
        loadOutplanting();
    }
    
    // Additional filter logic can be added here
}

/**
 * Clear all filters
 */
function clearFilters() {
    document.getElementById('site-search').value = '';
    document.getElementById('species-filter').value = '';
    document.getElementById('date-from').value = '';
    document.getElementById('date-to').value = '';
    
    // Reload layers
    loadSites();
    if (document.getElementById('outplanting-layer').checked) {
        loadOutplanting();
    }
}

/**
 * Perform spatial search around a point
 */
async function performSpatialSearch() {
    const radius = parseInt(document.getElementById('search-radius').value) || 10000;
    const center = map.getCenter();
    
    try {
        const results = await API.findNearby(center.lat, center.lng, radius);
        
        // Clear previous search marker
        if (searchMarker) {
            map.removeLayer(searchMarker);
        }
        
        // Add search center marker
        searchMarker = L.marker([center.lat, center.lng], {
            icon: L.divIcon({
                className: 'search-center-icon',
                html: '🎯',
                iconSize: [30, 30]
            })
        }).addTo(map);
        
        // Add circle showing search radius
        const searchCircle = L.circle([center.lat, center.lng], {
            radius: radius,
            color: '#0077be',
            fillColor: '#0077be',
            fillOpacity: 0.1,
            weight: 2,
            dashArray: '5, 10'
        }).addTo(map);
        
        // Fit map to search area
        map.fitBounds(searchCircle.getBounds());
        
        // Display results
        const sitesCount = results.results.sites.features.length;
        const outplantingCount = results.results.outplanting.features.length;
        
        PopupHelpers.updateInfoPanel(
            'Spatial Search Results',
            `
                <div class="info-item">
                    <div class="info-label">Search Radius</div>
                    <div class="info-value">${radius}m (${(radius/1000).toFixed(1)}km)</div>
                </div>
                <div class="info-item">
                    <div class="info-label">Sites Found</div>
                    <div class="info-value">${sitesCount}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">Outplanting Records</div>
                    <div class="info-value">${outplantingCount}</div>
                </div>
            `
        );
        
    } catch (error) {
        console.error('Spatial search error:', error);
    }
}

/**
 * Handle map click for spatial search
 */
function onMapClick(e) {
    // Optional: update search center on map click
    console.log('Map clicked at:', e.latlng);
}

// Make initializeMap available globally
window.initializeMap = initializeMap;
