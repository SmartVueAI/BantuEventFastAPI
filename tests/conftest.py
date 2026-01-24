import pytest
import asyncio
from typing import AsyncGenerator
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.db.session import get_db
from app.models.base import Base
from app.core.security import create_access_token, get_password_hash
from app.enums.enums import UserRoleEnum, GenderEnum
from app.models.user import User
import uuid

# Test database URL
TEST_DATABASE_URL = "postgresql+asyncpg://test_user:test_pass@localhost:5432/test_ecommerce_db"

# Create test engine
test_engine = create_async_engine(
    TEST_DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
)

TestSessionLocal = sessionmaker(
    test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for async tests"""
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Create test database session
    Creates tables before test and drops them after
    """
    # Create all tables
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # Create session
    async with TestSessionLocal() as session:
        yield session
    
    # Drop all tables
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="function")
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """
    Create test client with database session override
    """
    async def override_get_db():
        yield db_session
    
    app.dependency_overrides[get_db] = override_get_db
    
    async with AsyncClient(app=app, base_url="http://test") as test_client:
        yield test_client
    
    app.dependency_overrides.clear()


# Token fixtures
@pytest.fixture
def superadmin_token() -> str:
    """Create JWT token for superadmin"""
    token_data = {
        "sub": "SUPERADMIN@EXAMPLE.COM",
        "role": UserRoleEnum.SUPERADMIN.value
    }
    return create_access_token(token_data)


@pytest.fixture
def supervisor_token() -> str:
    """Create JWT token for supervisor"""
    token_data = {
        "sub": "SUPERVISOR@EXAMPLE.COM",
        "role": UserRoleEnum.SUPERVISOR.value
    }
    return create_access_token(token_data)


@pytest.fixture
def staff_token() -> str:
    """Create JWT token for staff"""
    token_data = {
        "sub": "STAFF@EXAMPLE.COM",
        "role": UserRoleEnum.STAFF.value
    }
    return create_access_token(token_data)


@pytest.fixture
def customer_token() -> str:
    """Create JWT token for customer"""
    token_data = {
        "sub": "CUSTOMER@EXAMPLE.COM",
        "role": UserRoleEnum.CUSTOMER.value
    }
    return create_access_token(token_data)


@pytest.fixture
async def test_superadmin(db_session: AsyncSession) -> User:
    """Create test superadmin user in database"""
    user = User(
        first_name="Super",
        last_name="Admin",
        email="superadmin@example.com",
        normalized_email="SUPERADMIN@EXAMPLE.COM",
        gender=GenderEnum.UNKNOWN,
        user_role=UserRoleEnum.SUPERADMIN,
        hashed_password=get_password_hash("testpassword123"),
        security_stamp=str(uuid.uuid4()),
        email_confirmed=True,
        is_active=True,
        created_by="system"
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user


@pytest.fixture
async def test_staff(db_session: AsyncSession) -> User:
    """Create test staff user in database"""
    user = User(
        first_name="Staff",
        last_name="User",
        email="staff@example.com",
        normalized_email="STAFF@EXAMPLE.COM",
        gender=GenderEnum.MALE,
        user_role=UserRoleEnum.STAFF,
        hashed_password=get_password_hash("testpassword123"),
        security_stamp=str(uuid.uuid4()),
        email_confirmed=True,
        is_active=True,
        created_by="system"
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user


@pytest.fixture
async def test_customer(db_session: AsyncSession) -> User:
    """Create test customer user in database"""
    user = User(
        first_name="Customer",
        last_name="User",
        email="customer@example.com",
        normalized_email="CUSTOMER@EXAMPLE.COM",
        gender=GenderEnum.FEMALE,
        user_role=UserRoleEnum.CUSTOMER,
        hashed_password=get_password_hash("testpassword123"),
        security_stamp=str(uuid.uuid4()),
        email_confirmed=True,
        is_active=True,
        created_by="system"
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user


@pytest.fixture
def test_user_data() -> dict:
    """Sample user data for testing"""
    return {
        "first_name": "Test",
        "last_name": "User",
        "email": "test@example.com",
        "gender": "male",
        "phone_number": "+1234567890",
        "location": "Test City",
        "user_role": "customer",
        "job_title": "Tester"
    }


@pytest.fixture
def test_login_data() -> dict:
    """Sample login data for testing"""
    return {
        "email": "customer@example.com",
        "password": "testpassword123"
    }


# Cleanup fixture
@pytest.fixture(autouse=True)
async def cleanup():
    """Cleanup after each test"""
    yield
    # Cleanup code here if needed


# Markers for different test categories
def pytest_configure(config):
    """Configure custom pytest markers"""
    config.addinivalue_line(
        "markers", "unit: Unit tests"
    )
    config.addinivalue_line(
        "markers", "integration: Integration tests"
    )
    config.addinivalue_line(
        "markers", "slow: Slow running tests"
    )
    config.addinivalue_line(
        "markers", "auth: Authentication tests"
    )
    config.addinivalue_line(
        "markers", "profile: User profile tests"
    )