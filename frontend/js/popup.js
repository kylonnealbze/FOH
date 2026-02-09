/**
 * Popup Module
 * Generates popup content for map features
 */

/**
 * Create popup content for a site
 */
function createSitePopup(properties) {
    const established = properties.established_date 
        ? new Date(properties.established_date).toLocaleDateString() 
        : 'Unknown';
    
    return `
        <div class="popup-content">
            <div class="popup-title">${properties.site_name}</div>
            <div class="popup-section">
                <span class="popup-label">Site ID:</span>
                <span class="popup-value">${properties.site_id}</span>
            </div>
            <div class="popup-section">
                <span class="popup-label">Established:</span>
                <span class="popup-value">${established}</span>
            </div>
            ${properties.description ? `
                <div class="popup-section">
                    <span class="popup-label">Description:</span><br>
                    <span class="popup-value">${properties.description}</span>
                </div>
            ` : ''}
            <button class="popup-button" onclick="showSiteDetails(${properties.site_id})">
                View Details
            </button>
            <button class="popup-button" onclick="showTemperatureData(${properties.site_id})">
                Temperature Data
            </button>
        </div>
    `;
}

/**
 * Create popup content for outplanting
 */
function createOutplantingPopup(properties) {
    const date = new Date(properties.outplanting_date).toLocaleDateString();
    
    return `
        <div class="popup-content">
            <div class="popup-title">🪸 Coral Outplanting</div>
            <div class="popup-section">
                <span class="popup-label">Species:</span>
                <span class="popup-value">${properties.species}</span>
            </div>
            <div class="popup-section">
                <span class="popup-label">Number of Corals:</span>
                <span class="popup-value">${properties.number_of_corals}</span>
            </div>
            <div class="popup-section">
                <span class="popup-label">Date:</span>
                <span class="popup-value">${date}</span>
            </div>
            ${properties.source_nursery ? `
                <div class="popup-section">
                    <span class="popup-label">Source Nursery:</span>
                    <span class="popup-value">${properties.source_nursery}</span>
                </div>
            ` : ''}
            ${properties.notes ? `
                <div class="popup-section">
                    <span class="popup-label">Notes:</span><br>
                    <span class="popup-value">${properties.notes}</span>
                </div>
            ` : ''}
            <button class="popup-button" onclick="showGrowthData(${properties.outplanting_id})">
                View Growth Data
            </button>
        </div>
    `;
}

/**
 * Create popup content for photomosaic
 */
function createPhotomosaicPopup(properties) {
    const date = new Date(properties.capture_date).toLocaleDateString();
    
    return `
        <div class="popup-content">
            <div class="popup-title">📷 Photomosaic</div>
            <div class="popup-section">
                <span class="popup-label">Capture Date:</span>
                <span class="popup-value">${date}</span>
            </div>
            ${properties.photographer ? `
                <div class="popup-section">
                    <span class="popup-label">Photographer:</span>
                    <span class="popup-value">${properties.photographer}</span>
                </div>
            ` : ''}
            ${properties.resolution ? `
                <div class="popup-section">
                    <span class="popup-label">Resolution:</span>
                    <span class="popup-value">${properties.resolution}m</span>
                </div>
            ` : ''}
            ${properties.processing_notes ? `
                <div class="popup-section">
                    <span class="popup-label">Notes:</span><br>
                    <span class="popup-value">${properties.processing_notes}</span>
                </div>
            ` : ''}
            <button class="popup-button" onclick="viewPhotomosaic('${properties.file_path}')">
                View Image
            </button>
        </div>
    `;
}

/**
 * Create popup content for photos
 */
function createPhotoPopup(properties) {
    const date = new Date(properties.taken_at).toLocaleString();
    
    return `
        <div class="popup-content">
            <div class="popup-title">🖼️ Photo</div>
            <div class="popup-section">
                <span class="popup-label">Taken:</span>
                <span class="popup-value">${date}</span>
            </div>
            ${properties.photographer ? `
                <div class="popup-section">
                    <span class="popup-label">Photographer:</span>
                    <span class="popup-value">${properties.photographer}</span>
                </div>
            ` : ''}
            ${properties.caption ? `
                <div class="popup-section">
                    <span class="popup-label">Caption:</span><br>
                    <span class="popup-value">${properties.caption}</span>
                </div>
            ` : ''}
            <button class="popup-button" onclick="viewPhoto('${properties.file_path}')">
                View Full Size
            </button>
        </div>
    `;
}

/**
 * Update info panel with feature details
 */
function updateInfoPanel(title, content) {
    const infoPanel = document.getElementById('info-content');
    if (infoPanel) {
        infoPanel.innerHTML = `
            <h3 style="color: var(--primary-color); margin-bottom: 10px;">${title}</h3>
            ${content}
        `;
    }
}

/**
 * Clear info panel
 */
function clearInfoPanel() {
    const infoPanel = document.getElementById('info-content');
    if (infoPanel) {
        infoPanel.innerHTML = '<p class="info-placeholder">Click on a feature to see details</p>';
    }
}

// Action functions called from popups

async function showSiteDetails(siteId) {
    try {
        const site = await API.getSite(siteId);
        const props = site.properties;
        
        let content = `
            <div class="info-item">
                <div class="info-label">Site Name</div>
                <div class="info-value">${props.site_name}</div>
            </div>
            <div class="info-item">
                <div class="info-label">Coordinates</div>
                <div class="info-value">
                    Lat: ${site.geometry.coordinates[1].toFixed(6)}<br>
                    Lon: ${site.geometry.coordinates[0].toFixed(6)}
                </div>
            </div>
        `;
        
        if (props.description) {
            content += `
                <div class="info-item">
                    <div class="info-label">Description</div>
                    <div class="info-value">${props.description}</div>
                </div>
            `;
        }
        
        updateInfoPanel(`Site: ${props.site_name}`, content);
    } catch (error) {
        console.error('Error loading site details:', error);
    }
}

async function showTemperatureData(siteId) {
    try {
        const data = await API.getTemperatureBySite(siteId);
        if (data.count > 0) {
            createTemperatureChart(data.data);
            document.getElementById('chart-panel').style.display = 'block';
        } else {
            updateInfoPanel('Temperature Data', '<p>No temperature data available for this site.</p>');
        }
    } catch (error) {
        console.error('Error loading temperature data:', error);
    }
}

function showGrowthData(outplantingId) {
    updateInfoPanel('Growth Data', `<p>Loading growth data for outplanting ${outplantingId}...</p>`);
    // This would need a new API endpoint for growth data by outplanting ID
    console.log('Show growth data for outplanting:', outplantingId);
}

function viewPhotomosaic(filePath) {
    console.log('View photomosaic:', filePath);
    alert(`Photomosaic viewer would open: ${filePath}`);
    // In a real implementation, this would open a modal or new window with the image
}

function viewPhoto(filePath) {
    console.log('View photo:', filePath);
    alert(`Photo viewer would open: ${filePath}`);
    // In a real implementation, this would open a modal or new window with the image
}

// Export functions
window.PopupHelpers = {
    createSitePopup,
    createOutplantingPopup,
    createPhotomosaicPopup,
    createPhotoPopup,
    updateInfoPanel,
    clearInfoPanel
};

window.showSiteDetails = showSiteDetails;
window.showTemperatureData = showTemperatureData;
window.showGrowthData = showGrowthData;
window.viewPhotomosaic = viewPhotomosaic;
window.viewPhoto = viewPhoto;
