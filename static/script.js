document.addEventListener("DOMContentLoaded", function() {
    fetchProfiles();
});



function fetchProfiles() {
    fetch('/profiles/')
        .then(response => response.json())
        .then(profiles => {
            const selector = document.getElementById('profileSelector');
            
            // Clear existing options first
            while (selector.options.length > 0) {                
                selector.remove(0);
            }

            // Optionally, add a default or prompt option
            let defaultOption = new Option("Select a profile", "");
            selector.add(defaultOption);

            // Now append the fetched profiles
            profiles.forEach(profile => {
                let option = new Option(profile.name, profile.id);
                selector.add(option);
            });
        });
}

function fetchAndPlotProfile(profileId) {
    fetch(`/profiles/${profileId}/`)
        .then(response => response.json())
        .then(data => plotProfile(data));
}

function plotProfile(profileData) {
    const ctx = document.getElementById('firingChart').getContext('2d');
    if (window.myChart) {
        window.myChart.destroy(); // Destroy the previous chart if it exists
    }
    window.myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: profileData.temperature_profile.map(point => point.time.toString()),
            datasets: [{
                label: profileData.name,
                data: profileData.temperature_profile.map(point => point.temperature),
                fill: false,
                borderColor: 'rgb(75, 192, 192)',
                tension: 0.1
            }]
        },
        options: {
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Time'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Temperature'
                    }
                }
            }
        }
    });
}

// Event listener for profile selection change
document.getElementById('profileSelector').onchange = function() {
    const profileId = this.value;
    if (profileId) {
        fetchAndPlotProfile(profileId);
    } else {
        // Handle case where "Select a profile" option is chosen
        if (window.myChart) {
            window.myChart.destroy();
        }
    }
};
