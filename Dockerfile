# Use an official lightweight Python image.
# Pythons alpine images are small, but you might need to compile dependencies.
# If you encounter issues, you can switch to a full Python image.
FROM python:3.9-slim

# Set environment variables to minimize the number of layers and ensure that Python output is sent straight to terminal without being first buffered.
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the Docker container.
WORKDIR /app

# Copy the requirements file into the container at /app.
COPY ./requirements.txt /app/requirements.txt

# Install any needed packages specified in requirements.txt.
RUN pip install --no-cache-dir -r requirements.txt

# Copy the local directory contents into the container at /app.
COPY . /app

# Make port 80 available to the world outside this container
EXPOSE 80

# Define the command to run your app using uvicorn
# Here, main:app refers to the FastAPI "app" instance in the "main.py" file
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]

# Define a volume pointing to /app/data to store SQLite database file persistently
VOLUME ["/app/data"]
