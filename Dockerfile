# Use a minimal Python base image
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Install system dependencies for PyMuPDF (fitz)
RUN apt-get update && apt-get install -y \
    libglib2.0-0 libgl1-mesa-glx libxrender1 libsm6 libxext6 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirement list and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY main.py .

# Default command
CMD ["python", "main.py"]
