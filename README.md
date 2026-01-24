# E-Commerce FastAPI Application

A production-ready e-commerce platform API built with FastAPI, featuring comprehensive security measures, user management, and scalable architecture.

## 🚀 Features

### Phase 1 Modules
- **User Profile Management**: Complete CRUD operations for user accounts
- **User Access Management**: Authentication, authorization, OTP verification, password management

### Security Features
- ✅ JWT-based authentication (15-min access, 2-day refresh tokens)
- ✅ Argon2 password hashing
- ✅ SSRF protection and metadata endpoint blocking
- ✅ Rate limiting (per IP and per user)
- ✅ Role-based access control (RBAC)
- ✅ Account lockout after failed login attempts
- ✅ Email verification with secure tokens
- ✅ OTP support for two-factor authentication
- ✅ CORS protection
- ✅ Security headers

### Core Features
- ✅ Async PostgreSQL with SQLAlchemy
- ✅ Database migrations with Alembic
- ✅ Redis caching and rate limiting
- ✅ Comprehensive audit trail
- ✅ Email notifications (SMTP)
- ✅ Image upload and processing (WebP conversion)
- ✅ Pagination for list endpoints
- ✅ Structured logging with Loguru
- ✅ Docker containerization
- ✅ API documentation (Swagger/ReDoc)

## 📋 Prerequisites

- Python 3.11+
- Docker and Docker Compose
- PostgreSQL 15+
- Redis 7+
- SMTP server access (for emails)

## 🛠️ Installation

### Local Development Setup

1. **Clone the repository**
```bash
git clone <repository-url>
cd ecommerce-api
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Setup environment variables**
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. **Initialize database**
```bash
# Start PostgreSQL and Redis (or use Docker Compose)
docker-compose up -d db redis

# Run migrations
alembic upgrade head
```

6. **Run development server**
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Visit: http://localhost:8000/api/docs

### Docker Deployment

1. **Configure environment**
```bash
cp .env.example .env
# Update .env with production values
```

2. **Build and start services**
```bash
docker-compose up -d --build
```

3. **Check logs**
```bash
docker-compose logs -f api
```

4. **Run migrations**
```bash
docker-compose exec api alembic upgrade head
```

5. **Access the API**
- API: http://localhost:8000
- Swagger Docs: http://localhost:8000/api/docs
- ReDoc: http://localhost:8000/api/redoc
- Health Check: http://localhost:8000/health

## 📁 Project Structure

```
ecommerce-api/
├── app/
│   ├── api/v1/endpoints/       # API routes
│   ├── core/                   # Core configuration
│   ├── db/                     # Database setup
│   ├── models/                 # SQLAlchemy models
│   ├── schemas/                # Pydantic schemas
│   ├── services/               # Business logic
│   ├── crud/                   # Database operations
│   ├── dependencies/           # FastAPI dependencies
│   ├── middleware/             # Custom middleware
│   ├── utils/                  # Utility functions
│   ├── exceptions/             # Custom exceptions
│   └── enums/                  # Enum definitions
├── alembic/                    # Database migrations
├── static/                     # Static files
├── logs/                       # Application logs
├── tests/                      # Test suite
├── .env                        # Environment variables
├── Dockerfile                  # Docker configuration
├── docker-compose.yml          # Docker Compose setup
└── requirements.txt            # Python dependencies
```

## 🔐 Security Configuration

### Environment Variables
Critical security settings in `.env`:

```bash
# Generate secure keys
JWT_SECRET_KEY=$(openssl rand -hex 32)
SECRET_KEY=$(openssl rand -hex 32)

# Update database credentials
DB_PASSWORD=<strong-password>

# Configure SMTP
SMTP_USER=<your-email>
SMTP_PASSWORD=<app-specific-password>
```

### Security Measures Implemented

1. **SSRF Protection**: Blocks access to internal IPs and metadata endpoints
2. **Rate Limiting**: 
   - Login: 5 requests/minute per IP
   - General: 100 requests/minute per user
3. **Account Lockout**: After 3 failed login attempts
4. **Password Requirements**: 
   - Minimum 8 characters
   - Mixed case, numbers, special characters
5. **Token Expiry**: 
   - Access token: 15 minutes
   - Refresh token: 2 days

## 📚 API Documentation

### User Profile Management

| Endpoint | Method | Description | Auth Required |
|----------|--------|-------------|---------------|
| `/api/v1/users/create` | POST | Create new user | ✅ (STAFF+) |
| `/api/v1/users/check-email/{email}` | GET | Check email existence | ❌ |
| `/api/v1/users/email/{email}` | GET | Get user by email | ✅ (STAFF+) |
| `/api/v1/users/active` | GET | List active users | ✅ (STAFF+) |
| `/api/v1/users/active/count` | GET | Count active users | ✅ (STAFF+) |
| `/api/v1/users/upload-profile-image` | POST | Upload profile image | ✅ |
| `/api/v1/users/update` | PUT | Update user details | ✅ |
| `/api/v1/users/search/{search}` | GET | Search users | ✅ (STAFF+) |

### User Access Management

| Endpoint | Method | Description | Auth Required |
|----------|--------|-------------|---------------|
| `/api/v1/auth/login` | POST | User login | ❌ |
| `/api/v1/auth/resend-otp` | POST | Resend OTP | ❌ |
| `/api/v1/auth/verify-otp` | POST | Verify OTP | ❌ |
| `/api/v1/auth/forgot-password` | POST | Initiate password reset | ❌ |
| `/api/v1/auth/reset-password` | POST | Reset password | ❌ |
| `/api/v1/auth/change-password` | POST | Change password | ✅ |
| `/api/v1/auth/verify-email` | POST | Verify email | ❌ |
| `/api/v1/auth/resend-verification-email` | POST | Resend verification | ❌ |
| `/api/v1/auth/validate-guid` | POST | Validate user GUID | ❌ |

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_user_profile.py -v
```

## 📊 Database Migrations

```bash
# Create new migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Rollback one version
alembic downgrade -1

# Show current version
alembic current

# Show migration history
alembic history
```

### In Docker
```bash
docker-compose exec api alembic upgrade head
docker-compose exec api alembic revision --autogenerate -m "Changes"
```

## 📝 Logging

Logs are stored in the `logs/` directory:
- `app_YYYY-MM-DD.log`: Application logs (30-day retention)
- `access.log`: HTTP access logs
- `error.log`: Error logs

View logs in real-time:
```bash
# Local
tail -f logs/app_$(date +%Y-%m-%d).log

# Docker
docker-compose logs -f api
```

## 🔄 Common Operations

### Create Superadmin User
```bash
docker-compose exec api python -c "
from app.db.session import async_session_maker
from app.services.user_service import UserService
from app.schemas.user import UserCreate
from app.enums.enums import UserRoleEnum, GenderEnum
import asyncio

async def create_superadmin():
    async with async_session_maker() as db:
        user_data = UserCreate(
            first_name='Super',
            last_name='Admin',
            email='admin@example.com',
            gender=GenderEnum.UNKNOWN,
            user_role=UserRoleEnum.SUPERADMIN
        )
        user, password = await UserService.create_user(db, user_data, 'system')
        await db.commit()
        print(f'Superadmin created: {user.email}')
        print(f'Password: {password}')

asyncio.run(create_superadmin())
"
```

### Backup Database
```bash
# Docker
docker-compose exec db pg_dump -U ecommerce_user ecommerce_db > backup.sql

# Restore
docker-compose exec -T db psql -U ecommerce_user ecommerce_db < backup.sql
```

### Clear Redis Cache
```bash
docker-compose exec redis redis-cli FLUSHALL
```

## 🚀 Production Deployment

### Pre-deployment Checklist

- [ ] Update all environment variables in `.env`
- [ ] Set `DEBUG=False` and `ENVIRONMENT=production`
- [ ] Generate strong `JWT_SECRET_KEY` and `SECRET_KEY`
- [ ] Configure SMTP with production credentials
- [ ] Update `CORS_ORIGINS` with production domains
- [ ] Set up SSL/TLS certificates
- [ ] Configure proper `ALLOWED_HOSTS`
- [ ] Review and adjust rate limits
- [ ] Set up monitoring and alerting
- [ ] Configure automated backups
- [ ] Test all security measures

### Deployment Steps

1. **Build production image**
```bash
docker-compose -f docker-compose.prod.yml build
```

2. **Start services**
```bash
docker-compose -f docker-compose.prod.yml up -d
```

3. **Run migrations**
```bash
docker-compose exec api alembic upgrade head
```

4. **Verify deployment**
```bash
curl http://your-domain.com/health
```

## 🔧 Troubleshooting

### Database Connection Issues
```bash
# Check if database is running
docker-compose ps db

# View database logs
docker-compose logs db

# Test connection
docker-compose exec db psql -U ecommerce_user -d ecommerce_db -c "SELECT 1;"
```

### Migration Errors
```bash
# Check current version
alembic current

# Downgrade and retry
alembic downgrade -1
alembic upgrade head
```

### Email Not Sending
- Verify SMTP credentials in `.env`
- Check firewall/port 587 is open
- For Gmail: Enable "Less secure app access" or use App Password
- Check logs: `docker-compose logs api | grep email`

## 📄 License

[Your License Here]

## 👥 Contributors

[Your Team Information]

## 📞 Support

For issues and questions:
- Email: support@yourdomain.com
- Issue Tracker: [GitHub Issues]

## 🗺️ Roadmap

### Phase 2 (Planned)
- Product catalog management
- Shopping cart functionality
- Order processing
- Payment gateway integration
- Inventory management
- Reports and analytics

---

**Note**: This is a Phase 1 implementation. Additional modules will be added in future phases as per the project requirements.