# Use the official Python image as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application directory into the container
COPY . .

# Expose port 80 (the default port for FastAPI applications)
EXPOSE 80

# Command to run the FastAPI application using uvicorn
CMD ["python3", "main.py"]
