# Use an official Python runtime. Using a specific version is good practice.
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /code

# Install system-level build dependencies required by some Python packages
# This is the key fix: it installs cmake, pkg-config, and C++ compilers
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    cmake \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file first to leverage Docker layer caching
COPY ./requirements.txt /code/requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy the rest of your application code into the container
COPY . /code/

# Command to run the FastAPI application when the container starts
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]