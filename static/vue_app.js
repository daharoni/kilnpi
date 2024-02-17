document.addEventListener('DOMContentLoaded', () => {
    const app = Vue.createApp({
      data() {
        return {
          profiles: [],
          selectedProfileId: null,
          pastFirings: [],
          currentTemperature: '',
          chart: null,
        };
      },
      methods: {
        fetchProfiles() {
          fetch('/profiles/')
            .then(response => response.json())
            .then(data => {
              this.profiles = data;
              console.log('Profiles fetched:', this.profiles); // Log to console
            })
            .catch(error => console.error('Error fetching profiles:', error));
        },
        fetchAndPlotProfile(profileId) {
          fetch(`/profiles/${profileId}/`)
            .then(response => response.json())
            .then(data => this.plotProfile(data))
            .catch(error => console.error('Error fetching profile data:', error));
        },
        plotProfile(profileData) {
          const ctx = document.getElementById('firingChart').getContext('2d');
          if (this.chart) {
            this.chart.destroy(); // Destroy the previous chart if it exists
          }
          this.chart = new Chart(ctx, {
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
        },
        startFiring() {
          // Placeholder for start firing functionality
        },
        abortFiring() {
          // Placeholder for abort firing functionality
        },
        fetchPastFirings() {
          // Placeholder for fetching past firings
        },
      },
      watch: {
        selectedProfileId(newVal, oldVal) {
          if (newVal !== oldVal && newVal !== null) {
            this.fetchAndPlotProfile(newVal);
          }
        },
      },
      mounted() {
        this.fetchProfiles();
        // Additional mounted logic, e.g., fetching current temperature, can go here
      }
    }).mount('#app');
  });
  