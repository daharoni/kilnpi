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
         initEmptyChart() {
            const ctx = document.getElementById('firingChart').getContext('2d');
            if (this.chart) {
                this.chart.destroy(); // Destroy the previous chart if it exists
            }
            this.chart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: [], // Empty labels array
                    datasets: [{
                        label: 'No Data',
                        data: [], // Empty data array
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
                                text: 'Time (hour)'
                            }
                        },
                        y: {
                            title: {
                                display: true,
                                text: 'Temperature (°C)'
                            }
                        }
                    }
                }
            });
        },
        fetchProfiles() {
          fetch('/profiles/')
            .then(response => response.json())
            .then(data => {
              this.profiles = data;
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
              labels: profileData.temperature_profile.map(point => (point.time / 60).toString()),
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
                    text: 'Time (hour)'
                  },
                  min: 0,
                  max: 12,
                  // Configure to use integer steps for the hours
                  type: 'linear',
                  ticks: {
                      stepSize: 1, // Set step size to 1 hour
                      callback: function(value) {
                          if (value % 1 === 0) { // Show only integer hours
                              return value;
                          }
                      }
                  }
                },
                y: {
                  title: {
                    display: true,
                    text: 'Temperature (°C)'
                  },
                  min: 0,
                  max: 1300
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
        this.initEmptyChart();
        // Additional mounted logic, e.g., fetching current temperature, can go here
      }
    }).mount('#app');
  });
  