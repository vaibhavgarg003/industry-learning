# Base image — Python 3.12 on slim Linux
FROM python:3.12-slim

# Install Java — required for PySpark
RUN apt-get update && apt-get install -y \
    default-jre \
    && rm -rf /var/lib/apt/lists/*

# Set Java environment variable
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64

# Set working directory inside container
WORKDIR /app

# Copy requirements first — Docker layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ ./src/
COPY tests/ ./tests/

# Create directories for output
RUN mkdir -p data logs

# Set Python environment for PySpark workers
ENV PYSPARK_PYTHON=python3
ENV PYSPARK_DRIVER_PYTHON=python3

# Default command — run the pipeline
CMD ["python3", "src/pipeline.py"]