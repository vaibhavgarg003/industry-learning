# Use official Python image
FROM python:3.12-slim

# Set working directory inside container
WORKDIR /app

# Copy requirements first (for caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# Create necessary directories
RUN mkdir -p data logs

# Run the pipeline
CMD ["python", "src/pipeline.py"]