document.addEventListener('DOMContentLoaded', () => {
    const app = Vue.createApp({
      data() {
        this.chart = null
        return {
          profiles: [],
          selectedProfileId: null,
          pastFirings: [],
          currentTemperature: '',
          // chart: null,
          isFiring: false,
          firingStartTimestamp: '',
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
              datasets: [
                {
                  label: profileData.name,
                  data: profileData.temperature_profile.map(point => ({x: point.time, y: point.temperature})),
                  fill: false,
                  borderColor: 'rgb(255, 99, 132)',
                  tension: 0.1
                },
                {
                  label: 'Kiln Temperature',
                  data: [],
                  fill: false,
                  borderColor: 'rgb(54, 162, 235)',
                  tension: 0.1
                }
              ]
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
            // Ask for confirmation before starting
            if (confirm('Are you sure you want to start the firing process?')) {
                // The user clicked "OK"
                // Disable the profile selector dropdown
                this.isFiring = true;
                this.fetchFiringStartTime()

                // Add your logic to start the firing process, e.g., making a POST request to the backend
                console.log('Firing process started');
                // ... your existing code to start the firing ...
            } else {
                // The user clicked "Cancel"
                console.log('Firing process not started');
            }
        },
        abortFiring() {
            if (confirm('Are you sure you want to ABORT the firing process?')) {
                // The user clicked "OK"
                // Disable the profile selector dropdown
                this.isFiring = false;

                // Add your logic to start the firing process, e.g., making a POST request to the backend
                console.log('Firing process aborted');
                // ... your existing code to start the firing ...
            } else {
                // The user clicked "Cancel"
                console.log('Firing process not aborted');
            }
        },
        fetchPastFirings() {
          // Placeholder for fetching past firings
        },
        fetchFiringStartTime() {
          fetch('/firingStartTimestamp/')
              .then(response => response.json())
              .then(data => {
                  this.firingStartTimestamp = data.firingStartTime;  // Update the data property
              })
              .catch(error => console.error('Error fetching firing start time:', error));
        },
        initWebSocket() {
          const ws = new WebSocket("ws://localhost:8000/ws/temperature"); // Adjust URL to your WebSocket endpoint
          ws.onopen = () => {
            console.log("WebSocket connection established");
          };
        
          ws.onerror = (error) => {
              console.error("WebSocket error:", error);
          };
          
          ws.onclose = () => {
              console.log("WebSocket connection closed");
          };
          ws.onmessage = (event) => {
              const data = JSON.parse(event.data);
              this.currentTemperature = data.temperature
              // console.log(data.timestamp);
              // TODO: Only update when isFiring is true
              this.updateChart(data.temperature, data.timeSinceFiringStart);
          };
        },
        calculateTimeDifference(dateTimeStr1, dateTimeStr2) {

          const date1 = new Date(dateTimeStr1);
          const date2 = new Date(dateTimeStr2);
          const diffMilliseconds = date2 - date1;
          const diffHours = diffMilliseconds / (1000 * 60 * 60);
          return diffHours; // Or format it as needed
        },
        updateChart(temperature, timestamp) {
            // Assuming your temperature data includes a timestamp in a format suitable for the chart's x-axis
            if (this.isFiring) {
              if (this.chart) {
                const dataset = this.chart.data.datasets.find(dataset => dataset.label == 'Kiln Temperature');
                if (dataset) {
                  dataset.data.push({x: timestamp, y: temperature});
                  this.chart.update();
                }  
              }
            }
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
        this.initWebSocket();
        // Additional mounted logic, e.g., fetching current temperature, can go here
      }
    }).mount('#app');
  });
  