# kilnpi
A web-based Raspberry Pi controller for ceramic kilns. This is a FastAPI project that uses Python, HTML, and Vue.js. It uses a SQLite database for storing past firing runs and Node.js for installing JS packages.

[![codecov](https://codecov.io/gh/daharoni/kilnpi/graph/badge.svg?token=Y5YQZ08Y36)](https://codecov.io/gh/daharoni/kilnpi)


Technologies Used
* FastAPI
* Python
* HTML
* Vue.js
* SQLite
* Node.js

Features
* Web-based Raspberry Pi controller for ceramic kilns
* SQLite database for storing past firing runs
* Uses Node.js for installing JS packages

Feel free to contribute to this project by submitting a pull request.

## How to build the virtual environment
To set up the virtual environment and install the required Python packages, follow these steps:
1. Install Python: Ensure Python 3.8 or newer is installed on your system. You can download it from python.org.

2. Create a Virtual Environment: Navigate to the project's root directory in your terminal and run:

`python3 -m venv venv`
This command creates a new virtual environment named venv within your project directory.

3. Activate the Virtual Environment:

On Windows, activate the virtual environment by running:

`.\venv\Scripts\activate`

On Unix or MacOS, use:

`source venv/bin/activate`

4. Install Requirements: With the virtual environment activated, install the project dependencies by running:

`pip install -r requirements.txt`

## How to run the server
This project has Docker setup but I don't know enough yet for describing exactly how to use it.

1. With the virtual environment activated, start the FastAPI server by running:
`uvicorn app.main:app --host 0.0.0.0 --port 8000`

This command starts the server, making it accessible on the host device's IP address on port 8000.
2. To access the client-side webpage, open a web browser and navigate to `http://<host's IP address>:8000/static/index.html`, replacing `<host's IP address>` with your host/server's actual IP address.

## Using Docker
If you prefer to containerize your application with Docker, here's a basic guide to get you started:

1. Install Docker: Ensure Docker is installed on your system. You can download it from docker.com.

2. Create a Dockerfile: **This should already exist in the project** but if not -> In your project's root directory, create a file named Dockerfile with the following content to define your Docker image:
```
FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

This Dockerfile uses the official Python 3.8 image, installs your Python dependencies, copies your project files into the image, and specifies the command to start your FastAPI server.

3. Build the Docker Image: In your terminal navigate to the project root directory and run:

`docker build -t kilnpi`

This command builds a Docker image from your Dockerfile and tags it as kilnpi.

4. Run the Docker Container: In your terminal navigate to the project root directory and run:

`docker run -d -p 8000:8000 kilnpi`

This command runs your Docker container, mapping port 8000 of the container to port 8000 on your host, allowing you to access the web application as described above.

## Logging

The application uses Python's built-in logging module to log messages. The logger is configured in `main.py` and can be used across all modules in the application. 

### Log Levels

The logger supports different levels of severity for log messages, which are:

- `DEBUG`: Detailed information, typically of interest only when diagnosing problems.
- `INFO`: Confirmation that things are working as expected.
- `WARNING`: An indication that something unexpected happened, or indicative of some problem in the near future (e.g., 'disk space low'). The software is still working as expected.
- `ERROR`: Due to a more serious problem, the software has not been able to perform some function.
- `CRITICAL`: A serious error, indicating that the program itself may be unable to continue running.

### How to Log Messages

To log messages in any module, first import the `logging` module and obtain a logger instance:

```
import logging
logger = logging.getLogger(__name__)
```
