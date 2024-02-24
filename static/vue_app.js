document.addEventListener('DOMContentLoaded', () => {
    const app = Vue.createApp({
      data() {
        this.chart = null
        return {
          profiles: [],
          selectedProfileId: null,
          pastFirings: [],
          currentTemperature: '',
          currentDutyCycle: '',
          // chart: null,
          isFiring: false,
          firingStartTimestamp: '',
          firingName: '',
          isSoak: false,
          isDry: false,
          isHold: false,
          kilnTemperatureData: [],
          dutyCycleData: [],
        };
      },
      methods: {

        fetchProfiles() {
          fetch('/profiles/')
            .then(response => response.json())
            .then(data => {
              this.profiles = data;
            })
            .catch(error => console.error('Error fetching profiles:', error));
        },
        updateProfilePlot(profileId) {
          if (profileId !== null) {
            fetch(`/profiles/${profileId}/`)
              .then(response => response.json())
              .then(data => this.plotProfile(data))
              .catch(error => console.error('Error fetching profile data:', error));
          }
          else {
            const emptyProfile = {name:'', temperature_profile: []};
            this.plotProfile(emptyProfile);
          }
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
                  tension: 0.1,
                  yAxisID: 'y',
                },
                {
                  label: 'Kiln Temperature',
                  data: this.kilnTemperatureData.map(point => ({x: point.time, y: point.temperature})),
                  fill: false,
                  borderColor: 'rgb(54, 162, 235)',
                  borderWidth: 4,
                  tension: 0.1,
                  yAxisID: 'y',
                },
                {
                  label: 'Kiln Duty Cycle',
                  data: this.dutyCycleData.map(point => ({x: point.time, y: point.duty_cycle})),
                  fill: false,
                  borderColor: 'rgb(75, 192, 192)',
                  borderWidth: 4,
                  tension: 0.1,
                  yAxisID: 'y1',
                }
              ]
            },
            options: {
              plugins: {
                zoom: {
                  limits: {
                    x: {min: 0, max: 24},
                    y: {min: 0, max: 1300}
                  },
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
                },
                y1: {
                  title: {
                    display: true,
                    text: 'Duty Cycle (%)'
                  },
                  min: 0,
                  max: 1,
                  position: 'right',
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
                this.kilnTemperatureData = [];
                this.dutyCycleData = [];
                

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
                  this.firingStartTimestamp = data.firingStartTime
              })
              .catch(error => {
                  console.error('Error:', error);
              });
                this.isFiring = true;

                // clear plot
                if (this.chart) {
                  const dataset = this.chart.data.datasets.find(dataset => dataset.label == 'Kiln Temperature');
                  if (dataset) {
                    dataset.data = [];
                    this.chart.update();

                  const dataset2 = this.chart.data.datasets.find(dataset => dataset.label == 'Kiln Duty Cycle');
                  if (dataset2) {
                    dataset2.data = [];
                    this.chart.update();
                  }  
                  }  
                }
                //this.postStateUpdate();
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
                this.postStateUpdate()

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
        postHoldChange(isHold) {
          fetch('/hold-change/', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({ isHold: isHold })
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
          const host = window.location.hostname;
          const port = "8000"; // Specify the port your WebSocket server is running on
          const wsURL = `ws://${host}:${port}/ws/new_data_to_plot`;
          const ws = new WebSocket(wsURL); // Adjust URL to your WebSocket endpoint
          //const ws = new WebSocket("ws://localhost:8000/ws/new_data_to_plot"); // Adjust URL to your WebSocket endpoint
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
              // console.log(data)
              if (data.type == "temperature_data") {
                this.currentTemperature = data.temperature;
                this.updateChart("Kiln Temperature", data.temperature, data.timeSinceFiringStart);
              }
              if (data.type == "duty_cycle_data"){
                this.currentDutyCycle = data.duty_cycle;
                this.updateChart('Kiln Duty Cycle', data.duty_cycle, data.timeSinceFiringStart);
              }
          };
        },
        calculateTimeDifference(dateTimeStr1, dateTimeStr2) {

          const date1 = new Date(dateTimeStr1);
          const date2 = new Date(dateTimeStr2);
          const diffMilliseconds = date2 - date1;
          const diffHours = diffMilliseconds / (1000 * 60 * 60);
          return diffHours; // Or format it as needed
        },
        updateChart(curveName, yValue, timestamp) {
            // Assuming your temperature data includes a timestamp in a format suitable for the chart's x-axis
            if (this.isFiring) {
              if (this.chart) {
                const dataset = this.chart.data.datasets.find(dataset => dataset.label == curveName);
                if (dataset) {
                  
                  if (curveName == 'Kiln Temperature') {
                    dataset.data.push({x: timestamp, y: yValue});
                    this.kilnTemperatureData.push({time: timestamp, temperature: yValue});
                  }
                  if (curveName == 'Kiln Duty Cycle') {
                    dataset.data.push({x: timestamp, y: yValue});
                    this.dutyCycleData.push({time: timestamp, duty_cycle: yValue});
                  }
                  this.chart.update();
                }  
              }
            }
        },
        getState(){
          // Should try to only call this when the full set of data for refreshing the webpage is needed
          fetch('/state/')
          .then(response => response.json())  // Make sure this is called as a method
          .then(data => {
            this.isFiring = data.isFiring;
            this.firingName = data.firingName;
            this.isSoak = data.isSoak;
            this.isDry = data.isDry;
            this.isHold = data.isHold;
            this.selectedProfileId = data.profileID;
            this.kilnTemperatureData = data.kilnTemperatureData;
            this.dutyCycleData = data.dutyCycleData;
          })
          .catch(error => console.error('Error fetching initial state:', error));
        },
        postStateUpdate() {
          try {
              fetch('/update_state/', {
                  method: 'POST',
                  headers: {
                      'Content-Type': 'application/json',
                  },
                  body: JSON.stringify({
                      isFiring: this.isFiring,
                      firingName: this.firingName,
                      isSoak: this.isSoak,
                      isDry: this.isDry,
                      isHold: this.isHold,
                      profileID: this.selectedProfileId,
                      kilnTemperatureData: this.kilnTemperatureData,
                      dutyCycleData: this.dutyCycleData,
                  }),
              });
          } catch (error) {
              console.error('Error posting state update:', error);
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
        isHold(newVal, oldVal) {
          if (newVal !== oldVal) {
            this.postHoldChange(newVal);
          }
        },
      },
      mounted() {
        this.getState();
        this.fetchProfiles();
        this.updateProfilePlot(this.selectedProfileId);
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
  