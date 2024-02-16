document.addEventListener("DOMContentLoaded", function() {
    fetchProfiles();
    initializeChart();
});

function initializeChart() {
    const ctx = document.getElementById('firingChart').getContext('2d');
    const temperatureChart = new Chart(ctx, {
        type: 'line', // Define the chart type
        data: {
            labels: ['Time 1', 'Time 2', 'Time 3', 'Time 4', 'Time 5'], // Placeholder labels for the x-axis
            datasets: [{
                label: 'Temperature',
                backgroundColor: 'rgb(255, 99, 132)',
                borderColor: 'rgb(255, 99, 132)',
                data: generateRandomData(5), // Generate 5 random data points
            }]
        },
        options: {}
    });
}

function generateRandomData(numPoints) {
    return Array.from({length: numPoints}, () => Math.floor(Math.random() * 1000));
}

function fetchProfiles() {
    fetch('/profiles/')
        .then(response => response.json())
        .then(data => {
            const selector = document.getElementById('profileSelector');
            data.forEach(profile => {
                let option = new Option(profile.name, profile.id);
                selector.add(option);
            });
        });
}

function fetchFiringData() {
    const profileId = document.getElementById('profileSelector').value;
    fetch(`/data/${profileId}/`)
        .then(response => response.json())
        .then(data => {
            document.getElementById('dataDisplay').textContent = JSON.stringify(data);
        });
}
