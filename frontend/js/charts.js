/**
 * Charts Module
 * Handles data visualization using Chart.js
 */

let temperatureChart = null;

/**
 * Create or update temperature chart
 */
function createTemperatureChart(data) {
    const ctx = document.getElementById('temperature-chart');
    if (!ctx) {
        console.error('Chart canvas not found');
        return;
    }
    
    // Destroy existing chart if it exists
    if (temperatureChart) {
        temperatureChart.destroy();
    }
    
    // Prepare data for Chart.js
    const labels = data.map(d => {
        const date = new Date(d.recorded_at);
        return date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    });
    
    const temperatures = data.map(d => d.temperature_celsius);
    
    // Create chart
    temperatureChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Temperature (°C)',
                data: temperatures,
                borderColor: 'rgb(0, 119, 190)',
                backgroundColor: 'rgba(0, 119, 190, 0.1)',
                tension: 0.4,
                fill: true
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true,
                    position: 'top',
                },
                title: {
                    display: false
                },
                tooltip: {
                    mode: 'index',
                    intersect: false,
                    callbacks: {
                        label: function(context) {
                            let label = context.dataset.label || '';
                            if (label) {
                                label += ': ';
                            }
                            label += context.parsed.y.toFixed(2) + '°C';
                            return label;
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: false,
                    title: {
                        display: true,
                        text: 'Temperature (°C)'
                    },
                    ticks: {
                        callback: function(value) {
                            return value.toFixed(1) + '°C';
                        }
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Date/Time'
                    },
                    ticks: {
                        maxRotation: 45,
                        minRotation: 45,
                        maxTicksLimit: 10
                    }
                }
            },
            interaction: {
                mode: 'nearest',
                axis: 'x',
                intersect: false
            }
        }
    });
}

/**
 * Create growth chart for coral measurements
 */
function createGrowthChart(data, canvasId) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return;
    
    const labels = data.map(d => new Date(d.measurement_date).toLocaleDateString());
    const sizes = data.map(d => d.size_cm);
    
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Size (cm)',
                data: sizes,
                borderColor: 'rgb(32, 178, 170)',
                backgroundColor: 'rgba(32, 178, 170, 0.1)',
                tension: 0.4,
                fill: true
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true
                },
                title: {
                    display: true,
                    text: 'Coral Growth Over Time'
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Size (cm)'
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Date'
                    }
                }
            }
        }
    });
}

/**
 * Create species distribution pie chart
 */
function createSpeciesDistributionChart(data, canvasId) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return;
    
    // Count species occurrences
    const speciesCounts = {};
    data.forEach(item => {
        const species = item.properties.species;
        speciesCounts[species] = (speciesCounts[species] || 0) + 1;
    });
    
    const labels = Object.keys(speciesCounts);
    const values = Object.values(speciesCounts);
    
    // Generate colors
    const colors = labels.map((_, i) => {
        const hue = (i * 360 / labels.length);
        return `hsl(${hue}, 70%, 60%)`;
    });
    
    new Chart(ctx, {
        type: 'pie',
        data: {
            labels: labels,
            datasets: [{
                data: values,
                backgroundColor: colors,
                borderWidth: 2,
                borderColor: '#fff'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true,
                    position: 'right'
                },
                title: {
                    display: true,
                    text: 'Species Distribution'
                }
            }
        }
    });
}

/**
 * Clear chart panel
 */
function clearCharts() {
    if (temperatureChart) {
        temperatureChart.destroy();
        temperatureChart = null;
    }
    const chartPanel = document.getElementById('chart-panel');
    if (chartPanel) {
        chartPanel.style.display = 'none';
    }
}

// Export functions
window.ChartHelpers = {
    createTemperatureChart,
    createGrowthChart,
    createSpeciesDistributionChart,
    clearCharts
};
