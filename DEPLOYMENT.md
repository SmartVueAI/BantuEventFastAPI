# Deployment Guide - FastAPI E-Commerce API

This guide provides comprehensive instructions for deploying the FastAPI E-Commerce application.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Local Development Setup](#local-development-setup)
3. [Docker Deployment](#docker-deployment)
4. [Production Deployment](#production-deployment)
5. [Database Migrations](#database-migrations)
6. [Environment Configuration](#environment-configuration)
7. [Testing the API](#testing-the-api)
8. [Troubleshooting](#troubleshooting)

## Prerequisites

### Required Software

- Python 3.11 or higher
- PostgreSQL 15 or higher
- Redis 7 or higher
- Docker and Docker Compose (optional but recommended)
- Git

### Required Accounts

- SMTP email service (Gmail, SendGrid, etc.)
- Domain name (for production)
- SSL certificate (for production HTTPS)

## Local Development Setup

### 1. Clone and Navigate

```bash
git clone <repository-url>
cd ecommerce-api
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate (Linux/Mac)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure Environment

```bash
# Copy example environment file
cp .env.example .env

# Edit with your settings
nano .env  # or use your preferred editor
```

**Required environment variables:**

```env
# Database
DB_USER=ecommerce_user
DB_PASSWORD=your_secure_password_here
DB_HOST=localhost
DB_PORT=5432
DB_NAME=ecommerce_db
DATABASE_URL=postgresql+asyncpg://${DB_USER}:${DB_PASSWORD}@${DB_HOST}:${DB_PORT}/${DB_NAME}

# JWT (Generate a secure 32+ character secret)
JWT_SECRET_KEY=your_32_character_minimum_secret_key_here

# SMTP (Example: Gmail)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your.email@gmail.com
SMTP_PASSWORD=your_app_specific_password
SMTP_FROM=noreply@yourdomain.com
SMTP_FROM_NAME=E-Commerce Platform

# Redis
REDIS_URL=redis://localhost:6379/0

# Security
SECRET_KEY=another_secure_32_character_secret_key
ALLOWED_HOSTS=localhost,127.0.0.1

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:8080
```

### 5. Setup Database

```bash
# Create PostgreSQL database
createdb ecommerce_db

# Or using psql
psql -U postgres
CREATE DATABASE ecommerce_db;
CREATE USER ecommerce_user WITH PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE ecommerce_db TO ecommerce_user;
\q
```

### 6. Run Migrations

```bash
# Create initial migration
alembic revision --autogenerate -m "Initial migration"

# Apply migrations
alembic upgrade head

# Verify migration
alembic current
```

### 7. Start Redis

```bash
# If Redis is installed locally
redis-server

# Or using Docker
docker run -d -p 6379:6379 redis:7-alpine
```

### 8. Run Development Server

```bash
# Start the application
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# The API will be available at:
# - http://localhost:8000
# - Docs: http://localhost:8000/api/docs
# - ReDoc: http://localhost:8000/api/redoc
```

## Docker Deployment

### 1. Prepare Environment

```bash
# Create .env file (same as above)
cp .env.example .env

# Edit Docker-specific settings
nano .env
```

**Docker environment adjustments:**

```env
DB_HOST=db  # Docker service name
REDIS_URL=redis://redis:6379/0  # Docker service name
```

### 2. Build and Start Services

```bash
# Build and start all services
docker-compose up -d --build

# View logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f api
```

### 3. Run Migrations in Docker

```bash
# Run migrations
docker-compose exec api alembic upgrade head

# Create new migration (if needed)
docker-compose exec api alembic revision --autogenerate -m "Description"
```

### 4. Verify Deployment

```bash
# Check service status
docker-compose ps

# Test health endpoint
curl http://localhost:8000/health

# Access API documentation
# Open browser: http://localhost:8000/api/docs
```

### 5. Manage Services

```bash
# Stop services
docker-compose stop

# Start services
docker-compose start

# Restart services
docker-compose restart

# Stop and remove containers
docker-compose down

# Stop and remove volumes (⚠️ deletes data)
docker-compose down -v

# View service logs
docker-compose logs api
docker-compose logs db
docker-compose logs redis
```

## Production Deployment

### 1. Server Requirements

- **OS**: Ubuntu 22.04 LTS or similar
- **RAM**: Minimum 2GB, recommended 4GB+
- **CPU**: 2+ cores recommended
- **Storage**: 20GB+ available
- **Network**: Static IP or domain name

### 2. Install Docker on Server

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo apt install docker-compose-plugin -y

# Add user to docker group
sudo usermod -aG docker $USER
newgrp docker

# Verify installation
docker --version
docker compose version
```

### 3. Deploy Application

```bash
# Clone repository
git clone <repository-url>
cd ecommerce-api

# Create production environment file
cp .env.example .env
nano .env  # Configure with production settings
```

**Production environment settings:**

```env
ENVIRONMENT=production
DEBUG=False

# Use strong secrets (generate with: openssl rand -hex 32)
JWT_SECRET_KEY=$(openssl rand -hex 32)
SECRET_KEY=$(openssl rand -hex 32)

# Production database
DB_PASSWORD=strong_production_password_here

# Production SMTP
SMTP_HOST=smtp.sendgrid.net  # Or your SMTP provider
SMTP_PORT=587
SMTP_USER=apikey
SMTP_PASSWORD=your_sendgrid_api_key

# Production CORS (your frontend domain)
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# Production hosts
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

### 4. Start Production Services

```bash
# Build and start services
docker compose up -d --build

# Run migrations
docker compose exec api alembic upgrade head

# Check logs
docker compose logs -f api
```

### 5. Setup Nginx Reverse Proxy

```bash
# Install Nginx
sudo apt install nginx -y

# Create Nginx configuration
sudo nano /etc/nginx/sites-available/ecommerce-api
```

**Nginx configuration:**

```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    client_max_body_size 10M;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    location /static/ {
        alias /path/to/ecommerce-api/static/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/ecommerce-api /etc/nginx/sites-enabled/

# Test configuration
sudo nginx -t

# Restart Nginx
sudo systemctl restart nginx
```

### 6. Setup SSL with Let's Encrypt

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx -y

# Obtain SSL certificate
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Test automatic renewal
sudo certbot renew --dry-run
```

### 7. Setup Firewall

```bash
# Allow necessary ports
sudo ufw allow 22/tcp   # SSH
sudo ufw allow 80/tcp   # HTTP
sudo ufw allow 443/tcp  # HTTPS
sudo ufw enable

# Check status
sudo ufw status
```

### 8. Setup Auto-Restart

```bash
# Configure Docker services to restart automatically
docker compose up -d --restart=unless-stopped
```

## Database Migrations

### Create New Migration

```bash
# After modifying models
alembic revision --autogenerate -m "Description of changes"

# In Docker
docker-compose exec api alembic revision --autogenerate -m "Description"
```

### Apply Migrations

```bash
# Apply all pending migrations
alembic upgrade head

# In Docker
docker-compose exec api alembic upgrade head
```

### Rollback Migrations

```bash
# Rollback one version
alembic downgrade -1

# Rollback to specific version
alembic downgrade <revision_id>

# In Docker
docker-compose exec api alembic downgrade -1
```

### View Migration History

```bash
# Show current version
alembic current

# Show history
alembic history

# Show SQL without executing
alembic upgrade head --sql
```

## Environment Configuration

### Gmail SMTP Setup

1. Enable 2-Factor Authentication on your Google account
2. Generate App Password:
   - Go to: https://myaccount.google.com/apppasswords
   - Select "Mail" and "Other (Custom name)"
   - Copy the 16-character password
3. Use in .env:
   ```env
   SMTP_USER=your.email@gmail.com
   SMTP_PASSWORD=your_16_char_app_password
   ```

### Generate Secure Secrets

```bash
# Generate JWT secret
openssl rand -hex 32

# Generate security key
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

## Testing the API

### 1. Health Check

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "environment": "production",
  "timestamp": 1704067200.0
}
```

### 2. API Documentation

Open in browser:
- Swagger UI: http://localhost:8000/api/docs
- ReDoc: http://localhost:8000/api/redoc

### 3. Test Endpoints

```bash
# Check email existence (no auth required)
curl http://localhost:8000/api/v1/users/check-email/test@example.com

# Create user (requires auth)
curl -X POST http://localhost:8000/api/v1/users/create \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@example.com",
    "gender": "male",
    "phone_number": "1234567890",
    "location": "New York",
    "user_role": "customer"
  }'
```

## Troubleshooting

### Common Issues

#### 1. Database Connection Error

```bash
# Check PostgreSQL is running
docker-compose ps db
# or
sudo systemctl status postgresql

# Verify connection
psql -U ecommerce_user -d ecommerce_db -h localhost

# Check DATABASE_URL in .env
cat .env | grep DATABASE_URL
```

#### 2. Redis Connection Error

```bash
# Check Redis is running
docker-compose ps redis
# or
redis-cli ping

# Should return: PONG
```

#### 3. Email Not Sending

```bash
# Check SMTP settings in .env
cat .env | grep SMTP

# Test SMTP connection
python3 -c "
import aiosmtplib
import asyncio
from email.message import EmailMessage

async def test():
    message = EmailMessage()
    message['From'] = 'your@email.com'
    message['To'] = 'test@example.com'
    message['Subject'] = 'Test'
    message.set_content('Test email')
    
    await aiosmtplib.send(
        message,
        hostname='smtp.gmail.com',
        port=587,
        username='your@email.com',
        password='your_password',
        start_tls=True
    )
    print('Email sent successfully!')

asyncio.run(test())
"
```

#### 4. Migration Errors

```bash
# Reset migrations (⚠️ development only)
alembic downgrade base
alembic upgrade head

# Or recreate from scratch
dropdb ecommerce_db
createdb ecommerce_db
alembic upgrade head
```

#### 5. Port Already in Use

```bash
# Find process using port 8000
sudo lsof -i :8000

# Kill process
sudo kill -9 <PID>

# Or use different port
uvicorn app.main:app --port 8001
```

### View Logs

```bash
# Application logs
tail -f logs/app_$(date +%Y-%m-%d).log

# Docker logs
docker-compose logs -f api

# Nginx logs
sudo tail -f /var/log/nginx/error.log
sudo tail -f /var/log/nginx/access.log
```

### Performance Monitoring

```bash
# Check Docker resource usage
docker stats

# Check API response time
curl -w "@-" -o /dev/null -s http://localhost:8000/health << 'EOF'
    time_namelookup:  %{time_namelookup}\n
       time_connect:  %{time_connect}\n
    time_appconnect:  %{time_appconnect}\n
      time_redirect:  %{time_redirect}\n
   time_pretransfer:  %{time_pretransfer}\n
 time_starttransfer:  %{time_starttransfer}\n
                    ----------\n
         time_total:  %{time_total}\n
EOF
```

## Maintenance

### Backup Database

```bash
# Backup
docker-compose exec db pg_dump -U ecommerce_user ecommerce_db > backup_$(date +%Y%m%d).sql

# Restore
docker-compose exec -T db psql -U ecommerce_user ecommerce_db < backup_20240101.sql
```

### Update Application

```bash
# Pull latest code
git pull origin main

# Rebuild and restart
docker-compose down
docker-compose up -d --build

# Run migrations
docker-compose exec api alembic upgrade head
```

### Monitor Disk Space

```bash
# Check disk usage
df -h

# Clean Docker
docker system prune -a

# Clean logs older than 30 days
find logs/ -name "*.log" -mtime +30 -delete
```

## Support

For issues or questions:
- Create an issue in the repository
- Check documentation: README.md
- Contact support: support@yourdomain.com

---

**Security Note**: Always use strong passwords, keep secrets secure, and regularly update dependencies.