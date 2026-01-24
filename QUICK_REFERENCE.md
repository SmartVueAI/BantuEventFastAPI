# FastAPI E-Commerce - Quick Reference Guide

## 🚀 Quick Start Commands

```bash
# Clone and setup
git clone <repo-url>
cd ecommerce-api
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt

# Configure
cp .env.example .env
# Edit .env with your settings

# Deploy with Docker
chmod +x deploy.sh
./deploy.sh deploy

# Or manually
docker-compose up -d --build
docker-compose exec api alembic upgrade head

# Create superadmin
docker-compose exec api python create_superadmin.py
```

## 📁 File Structure Quick Map

```
app/
├── main.py                      # Application entry point
├── api/v1/endpoints/
│   ├── user_profile.py          # User CRUD endpoints
│   └── user_access.py           # Auth endpoints
├── core/
│   ├── config.py                # Settings
│   ├── security.py              # JWT & auth
│   └── logging_config.py        # Logging setup
├── models/                      # SQLAlchemy models
├── schemas/                     # Pydantic schemas
├── services/                    # Business logic
├── middleware/                  # Custom middleware
└── utils/                       # Utility functions
```

## 🔑 Key Endpoints

### User Profile Management
```
POST   /api/v1/users/create                  Create user (STAFF+)
GET    /api/v1/users/check-email/{email}     Check email exists
GET    /api/v1/users/email/{email}           Get user by email (STAFF+)
GET    /api/v1/users/active                  List active users (STAFF+)
GET    /api/v1/users/active/count            Count active users (STAFF+)
POST   /api/v1/users/upload-profile-image    Upload image
PUT    /api/v1/users/update                  Update user
GET    /api/v1/users/search/{term}           Search users (STAFF+)
```

### User Access Management
```
POST   /api/v1/auth/login                    Login
POST   /api/v1/auth/resend-otp               Resend OTP
POST   /api/v1/auth/verify-otp               Verify OTP
POST   /api/v1/auth/forgot-password          Forgot password
POST   /api/v1/auth/reset-password           Reset password
POST   /api/v1/auth/change-password          Change password
POST   /api/v1/auth/verify-email             Verify email
POST   /api/v1/auth/resend-verification-email Resend verification
POST   /api/v1/auth/validate-guid            Validate GUID
```

## 🔐 User Roles & Permissions

```
SUPERADMIN    → Full system access
SUPERVISOR    → Management access
STAFF         → User management
Others        → Limited access
```

**Permission Hierarchy:**
```
SUPERADMIN > SUPERVISOR > STAFF > INVENTORYMANAGER > 
REPORTANALYST > CONTENTMANAGER > VENDOR > CUSTOMER > GUEST
```

## 🐳 Docker Commands

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f api
docker-compose logs -f db

# Stop all services
docker-compose down

# Rebuild and restart
docker-compose up -d --build

# Execute command in container
docker-compose exec api <command>

# Database shell
docker-compose exec db psql -U ecommerce_user -d ecommerce_db

# Redis CLI
docker-compose exec redis redis-cli
```

## 📊 Database Commands

```bash
# Alembic migrations
alembic revision --autogenerate -m "Message"
alembic upgrade head
alembic downgrade -1
alembic current
alembic history

# In Docker
docker-compose exec api alembic upgrade head
docker-compose exec api alembic current

# Database backup
docker-compose exec db pg_dump -U ecommerce_user ecommerce_db > backup.sql

# Database restore
docker-compose exec -T db psql -U ecommerce_user ecommerce_db < backup.sql
```

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_user_profile.py -v

# Run specific test
pytest tests/test_user_profile.py::test_create_user_success -v
```

## 📝 Logging

```bash
# View today's logs
tail -f logs/app_$(date +%Y-%m-%d).log

# View errors only
grep ERROR logs/app_$(date +%Y-%m-%d).log

# Docker logs
docker-compose logs -f api
docker-compose logs --tail=100 api

# Follow errors in Docker
docker-compose logs -f api | grep ERROR
```

## 🔧 Common Operations

### Create User Programmatically
```python
from app.services.user_service import UserService
from app.schemas.user import UserCreate
from app.enums.enums import UserRoleEnum, GenderEnum

user_data = UserCreate(
    first_name="John",
    last_name="Doe",
    email="john@example.com",
    gender=GenderEnum.MALE,
    user_role=UserRoleEnum.CUSTOMER
)

user, password = await UserService.create_user(db, user_data, "admin@example.com")
```

### Generate JWT Token
```python
from app.core.security import create_access_token

token_data = {"sub": "user@example.com", "role": "customer"}
token = create_access_token(token_data)
```

### Hash Password
```python
from app.core.security import get_password_hash, verify_password

hashed = get_password_hash("mypassword")
is_valid = verify_password("mypassword", hashed)
```

## 🔍 Troubleshooting Quick Fixes

### Database Connection Error
```bash
docker-compose restart db
docker-compose logs db
```

### Migration Error
```bash
alembic downgrade -1
alembic upgrade head
```

### Port Already in Use
```bash
# Find process using port 8000
lsof -ti:8000 | xargs kill -9  # Mac/Linux
netstat -ano | findstr :8000   # Windows

# Or change port in docker-compose.yml
ports:
  - "8001:8000"  # Use 8001 instead
```

### Clear All Data
```bash
docker-compose down -v
docker-compose up -d --build
docker-compose exec api alembic upgrade head
```

### Reset Database
```bash
docker-compose exec db psql -U ecommerce_user -d ecommerce_db -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"
docker-compose exec api alembic upgrade head
```

## 📈 Performance Monitoring

### Check Database Connections
```sql
-- In psql
SELECT count(*) FROM pg_stat_activity;
```

### Check Redis Memory
```bash
docker-compose exec redis redis-cli INFO memory
```

### Check API Response Time
```bash
curl -w "@curl-format.txt" -o /dev/null -s http://localhost:8000/health
```

Create `curl-format.txt`:
```
time_namelookup:  %{time_namelookup}\n
time_connect:  %{time_connect}\n
time_starttransfer:  %{time_starttransfer}\n
time_total:  %{time_total}\n
```

## 🔐 Security Checklist

- [ ] Change default JWT_SECRET_KEY
- [ ] Change default SECRET_KEY
- [ ] Update SMTP credentials
- [ ] Set DEBUG=False in production
- [ ] Configure CORS_ORIGINS properly
- [ ] Use strong database password
- [ ] Enable HTTPS/SSL
- [ ] Configure firewall rules
- [ ] Set up rate limiting
- [ ] Enable audit logging

## 📚 Useful URLs

```
Local Development:
- API:              http://localhost:8000
- Swagger Docs:     http://localhost:8000/api/docs
- ReDoc:            http://localhost:8000/api/redoc
- Health Check:     http://localhost:8000/health

Database:
- Host:             localhost
- Port:             5432
- Database:         ecommerce_db

Redis:
- Host:             localhost
- Port:             6379
```

## 💡 Pro Tips

1. **Use Swagger UI** for testing - it's interactive!
2. **Check logs first** when debugging issues
3. **Always backup database** before migrations
4. **Use .env for secrets** - never commit it
5. **Test in Docker** before deploying to production
6. **Monitor logs** in production regularly
7. **Set up alerts** for errors
8. **Regular security updates** for dependencies
9. **Database backups** daily in production
10. **Load testing** before going live

## 🆘 Emergency Commands

```bash
# Stop everything immediately
docker-compose down

# Full reset (WARNING: Deletes all data)
docker-compose down -v
rm -rf logs/* static/profile_images/*
docker-compose up -d --build

# Rollback last migration
docker-compose exec api alembic downgrade -1

# Check service health
docker-compose ps
docker-compose exec api curl http://localhost:8000/health

# View last 100 log lines
docker-compose logs --tail=100 api
```

## 📞 Support Resources

- Swagger Docs: http://localhost:8000/api/docs
- Application Logs: `logs/app_YYYY-MM-DD.log`
- Docker Logs: `docker-compose logs`
- Database Logs: `docker-compose logs db`
- GitHub Issues: [Your repo issues page]

---

**Quick Reference Version:** 1.0  
**Last Updated:** December 2024

For detailed documentation, see README.md and SETUP.md