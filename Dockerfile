FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Create necessary directories
RUN mkdir -p logs static/profile_images

# Create non-root user for security
RUN useradd -m -u 1000 mcsmart1 && chown -R mcsmart1:mcsmart1 /app
USER mcsmart1

# Expose port
EXPOSE 8000

# Use uvicorn with proper workers
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]