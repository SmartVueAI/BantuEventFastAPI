FROM python:3.11-slim

WORKDIR /app

# Install system dependencies if needed
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy entire project
COPY . .

# Create non-root user FIRST
RUN useradd -m -u 1000 mcsmart1

# Create logs directory and give ownership to mcsmart1
RUN mkdir -p /app/logs && chown -R mcsmart1:mcsmart1 /app

# Switch to non-root user
USER mcsmart1

# Expose port
EXPOSE 8000

# Run from app directory - note "app.main:app"
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]