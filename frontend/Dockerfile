# Use the official Node.js image from the Docker Hub
FROM node:21

# Set the working directory in the container
WORKDIR /app

# Copy package.json and package-lock.json (if present)
COPY package.json /app/

# Install dependencies
RUN npm install

# Copy the rest of the application code into the container
COPY . /app/

RUN npm run build

# Expose the port the app runs on
EXPOSE 3000

# Command to run the application
CMD ["npm", "run", "preview"]
