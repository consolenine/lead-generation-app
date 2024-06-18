# Use the official Python image from the Docker Hub
FROM python:3.11

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
# RUN apt-get update && \
#     apt-get install -y wget unzip && \
#     wget https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zip && \
#     unzip chromedriver_linux64.zip -d /usr/bin && \
#     rm chromedriver_linux64.zip && \
#     wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
#     dpkg -i google-chrome-stable_current_amd64.deb && \
#     apt-get -f install -y && \
#     rm google-chrome-stable_current_amd64.deb && \
#     apt-get clean && \
#     rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Set the environment variables for Django
ENV PYTHONUNBUFFERED 1

# Run Django migrations and start the server
CMD ["sh", "-c", "python lead_generator/manage.py migrate && python lead_generator/manage.py runserver 0.0.0.0:8000 --environment=prod"]