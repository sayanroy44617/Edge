FROM python:3.10-slim

# Set non-root user and working directory for security
ARG USER=appuser
ARG GROUP=appuser
ARG UID=1000
ARG GID=1000

RUN groupadd -g $GID $GROUP && useradd -m -u $UID -g $GID $USER

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file and install dependencies

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire central server source code
COPY . .

EXPOSE 8000

# Ensure the app runs as the non-root user
USER $USER

# Define the command to run the Central Server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]