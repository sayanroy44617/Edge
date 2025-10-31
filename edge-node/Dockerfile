FROM python:3.10-slim


ENV CENTRAL_SERVER_URL=http://central-server:8000

# Set non-root user and working directory for security
ARG USER=appuser
ARG GROUP=appuser
ARG UID=1000
ARG GID=1000

RUN groupadd -g $GID $GROUP && useradd -m -u $UID -g $GID $USER

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file and install dependencies
# This ensures Docker can cache this layer efficiently
COPY requirements.txt .

# Install dependencies needed for the Edge Node (primarily 'requests')
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire edge node source code (including the script and config)
# The source path is relative to the current directory where 'docker build' is executed
COPY . .

# Ensure the app runs as the non-root user
USER $USER

# Define the command to run the Edge Node script
# The script relies on config.json being in the current directory
CMD ["python", "edge_node.py"]
