# Use the official Python image from the Docker Hub with Python 3.11-bookworm
FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /usr/src/app

# Install system dependencies
RUN apt-get update && apt-get install -y gcc wget gnupg curl unzip libffi-dev postgresql-client supervisor; \
    wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb; \
    apt-get install -y ./google-chrome-stable_current_amd64.deb;

# Copy the requirements file into the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Run supervisord to manage processes
CMD ["supervisord", "-c", "supervisord.conf"]
