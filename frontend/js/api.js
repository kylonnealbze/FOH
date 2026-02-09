/**
 * API Module
 * Handles all API requests to the FastAPI backend
 */

// API Configuration
const API_CONFIG = {
    // Update this to your Synology NAS IP and port
    baseURL: 'http://localhost:8000',
    // For PHP on Hostgator, use: 'http://your-synology-ip:8000'
    timeout: 30000
};

/**
 * Make a GET request to the API
 */
async function apiGet(endpoint, params = {}) {
    try {
        const url = new URL(`${API_CONFIG.baseURL}${endpoint}`);
        Object.keys(params).forEach(key => {
            if (params[key] !== null && params[key] !== undefined && params[key] !== '') {
                url.searchParams.append(key, params[key]);
            }
        });
        
        showLoading();
        const response = await fetch(url, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        hideLoading();
        return data;
    } catch (error) {
        hideLoading();
        console.error('API GET Error:', error);
        showError(`Failed to fetch data: ${error.message}`);
        throw error;
    }
}

/**
 * Make a POST request to the API
 */
async function apiPost(endpoint, data) {
    try {
        showLoading();
        const response = await fetch(`${API_CONFIG.baseURL}${endpoint}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const result = await response.json();
        hideLoading();
        return result;
    } catch (error) {
        hideLoading();
        console.error('API POST Error:', error);
        showError(`Failed to create data: ${error.message}`);
        throw error;
    }
}

// API Endpoint Functions

/**
 * Get all sites as GeoJSON
 */
async function getSites() {
    return apiGet('/api/sites');
}

/**
 * Get a specific site by ID
 */
async function getSite(siteId) {
    return apiGet(`/api/sites/${siteId}`);
}

/**
 * Get all outplanting records as GeoJSON
 */
async function getOutplanting(species = null) {
    const params = species ? { species } : {};
    return apiGet('/api/outplanting', params);
}

/**
 * Get outplanting by site
 */
async function getOutplantingBySite(siteId) {
    return apiGet(`/api/outplanting/by-site/${siteId}`);
}

/**
 * Get all photomosaics as GeoJSON
 */
async function getPhotomosaics() {
    return apiGet('/api/photomosaics');
}

/**
 * Get photomosaics for a specific site
 */
async function getPhotomosaicsBySite(siteId) {
    return apiGet(`/api/photomosaics/by-site/${siteId}`);
}

/**
 * Get temperature data for a site
 */
async function getTemperatureBySite(siteId, startDate = null, endDate = null) {
    const params = {};
    if (startDate) params.start_date = startDate;
    if (endDate) params.end_date = endDate;
    return apiGet(`/api/temperature/by-site/${siteId}`, params);
}

/**
 * Get all surveys
 */
async function getSurveys(siteId = null) {
    const params = siteId ? { site_id: siteId } : {};
    return apiGet('/api/surveys', params);
}

/**
 * Get survey details with photos
 */
async function getSurvey(surveyId) {
    return apiGet(`/api/surveys/${surveyId}`);
}

/**
 * Find sites and data within radius (spatial query)
 */
async function findNearby(latitude, longitude, radius) {
    return apiGet('/api/spatial/nearby', {
        latitude,
        longitude,
        radius
    });
}

/**
 * Get data within an MPA
 */
async function getDataWithinMPA(mpaId) {
    return apiGet(`/api/spatial/within-mpa/${mpaId}`);
}

/**
 * Calculate distance between two points
 */
async function calculateDistance(lat1, lon1, lat2, lon2) {
    return apiGet('/api/spatial/distance', {
        lat1,
        lon1,
        lat2,
        lon2
    });
}

// UI Helper Functions

function showLoading() {
    const overlay = document.getElementById('loading-overlay');
    if (overlay) {
        overlay.style.display = 'flex';
    }
}

function hideLoading() {
    const overlay = document.getElementById('loading-overlay');
    if (overlay) {
        overlay.style.display = 'none';
    }
}

function showError(message) {
    // Simple error display - can be enhanced with a proper notification system
    console.error(message);
    alert(message);
}

function showSuccess(message) {
    console.log(message);
    // Could be enhanced with a proper notification system
}

// Export functions for use in other modules
window.API = {
    getSites,
    getSite,
    getOutplanting,
    getOutplantingBySite,
    getPhotomosaics,
    getPhotomosaicsBySite,
    getTemperatureBySite,
    getSurveys,
    getSurvey,
    findNearby,
    getDataWithinMPA,
    calculateDistance
};
