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
          firingName: '',
          isSoak: false,
          isDry: false,
        };
      },
      methods: {
         initEmptyChart() {
            const ctx = this.$refs.firingChart.getContext('2d');
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
        updateProfilePlot(profileId) {
          fetch(`/profiles/${profileId}/`)
            .then(response => response.json())
            .then(data => this.plotProfile(data))
            .catch(error => console.error('Error fetching profile data:', error));
        },
        plotProfile(profileData) {
          const ctx = this.$refs.firingChart.getContext('2d');
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
                  borderWidth: 2,
                  tension: 0.1
                },
                {
                  label: 'Kiln Temperature',
                  data: [],
                  fill: false,
                  borderColor: 'rgb(54, 162, 235)',
                  borderWidth: 4,
                  tension: 0.1
                }
              ]
            },
            options: {
              plugins: {
                zoom: {
                    zoom: {
                        wheel: {
                            enabled: true, // Enable zooming with the mouse wheel
                        },
                        pinch: {
                            enabled: true // Enable zooming with pinch gestures on touch devices
                        },
                        mode: 'xy', // Zoom both the x and y axes
                    },
                    pan: {
                        enabled: true, // Enable panning
                        mode: 'xy' // Pan in both the x and y axes
                    }
                }
              },
              scales: {
                x: {
                  title: {
                    display: true,
                    text: 'Time (hour)'
                  },
                  min: 0,
                  max: 16,
                  // Configure to use integer steps for the hours
                  type: 'linear',
                  ticks: {
                      stepSize: 1, // Set step size to 1 hour
                      callback: function(value, index, values) {
                        return Math.round(value);
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
                // The user clicked "OK", send the signal to the backend
                fetch('/start-firing/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({firingName: this.firingName})
              })
              .then(response => {
                  if (!response.ok) {
                      throw new Error('Failed to start the firing process');
                  }
                  return response.json();
              })
              .then(data => {
                  console.log(data.message);  // Log the success message
                  // Update any relevant component state here
              })
              .catch(error => {
                  console.error('Error:', error);
              });
                this.isFiring = true;
                this.fetchFiringStartTime();

                // clear plot
                if (this.chart) {
                  const dataset = this.chart.data.datasets.find(dataset => dataset.label == 'Kiln Temperature');
                  if (dataset) {
                    dataset.data = [];
                    this.chart.update();
                  }  
                }
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
                fetch('/abort-firing/', {
                  method: 'POST',
                  headers: {
                      'Content-Type': 'application/json'
                  },
                  // You can send additional data in the body if needed
                  // body: JSON.stringify({ key: 'value' })
                })
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Failed to start the firing process');
                    }
                    return response.json();
                })
                .then(data => {
                    console.log(data.message);  // Log the success message
                    // Update any relevant component state here
                })
                .catch(error => {
                    console.error('Error:', error);
                });
                this.isFiring = false;

                // Add your logic to start the firing process, e.g., making a POST request to the backend
                console.log('Firing process aborted');
                // ... your existing code to start the firing ...
            } else {
                // The user clicked "Cancel"
                console.log('Firing process not aborted');
            }
        },
          postDryChange(isDry) {
            fetch('/dry-change/', {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json'
              },
              body: JSON.stringify({ isDry: isDry })
            })
            .then(response => response.json())
            .then(data => this.plotProfile(data))
            .catch(error => console.error('Error:', error));
          },
          postSoakChange(isSoak) {
            fetch('/soak-change/', {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json'
              },
              body: JSON.stringify({ isSoak: isSoak })
            })
            .then(response => response.json())
            .then(data => this.plotProfile(data))
            .catch(error => console.error('Error:', error));
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
            this.updateProfilePlot(newVal);
          }
        },
        isDry(newVal, oldVal) {
          if (newVal !== oldVal) {
            this.postDryChange(newVal);
          }
        },
        isSoak(newVal, oldVal) {
          if (newVal !== oldVal) {
            this.postSoakChange(newVal);
          }
        },
      },
      mounted() {
        this.fetchProfiles();
        this.initEmptyChart();
        this.initWebSocket();
        this.$refs.firingChart.addEventListener('dblclick', () => {
          if (this.chart) { // Assuming this.chart is your Chart.js instance
            this.chart.resetZoom();
          }
        });
        // Additional mounted logic, e.g., fetching current temperature, can go here
      }
    }).mount('#app');
  });
  