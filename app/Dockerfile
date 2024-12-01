# Base image with Python
FROM python:3.9-slim

# Install dependencies
RUN apt-get update && apt-get install -y \
    libx11-6 libglib2.0-0 libsm6 libxext6 libxrender1 \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV S3_BUCKET_NAME=${S3_BUCKET_NAME}

# Set working directory
WORKDIR /app

# Copy app files
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir boto3 flask

# Expose Flask port
EXPOSE 5000

# Run the app
CMD ["python", "app.py"]
