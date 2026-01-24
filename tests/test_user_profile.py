import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import asyncio

from app.main import app
from app.db.session import get_db
from app.models.base import Base
from app.core.security import create_access_token
from app.enums.enums import UserRoleEnum

# Test database URL
TEST_DATABASE_URL = "postgresql+asyncpg://test_user:test_pass@localhost:5432/test_ecommerce_db"

# Create test engine
engine = create_async_engine(TEST_DATABASE_URL, echo=False)
TestSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for async tests"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def db_session():
    """Create test database session"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async with TestSessionLocal() as session:
        yield session
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="function")
async def client(db_session):
    """Create test client"""
    async def override_get_db():
        yield db_session
    
    app.dependency_overrides[get_db] = override_get_db
    
    async with AsyncClient(app=app, base_url="http://test") as test_client:
        yield test_client
    
    app.dependency_overrides.clear()


@pytest.fixture
def superadmin_token():
    """Create superadmin JWT token"""
    token_data = {
        "sub": "ADMIN@EXAMPLE.COM",
        "role": UserRoleEnum.SUPERADMIN.value
    }
    return create_access_token(token_data)


@pytest.fixture
def staff_token():
    """Create staff JWT token"""
    token_data = {
        "sub": "STAFF@EXAMPLE.COM",
        "role": UserRoleEnum.STAFF.value
    }
    return create_access_token(token_data)


@pytest.fixture
def customer_token():
    """Create customer JWT token"""
    token_data = {
        "sub": "CUSTOMER@EXAMPLE.COM",
        "role": UserRoleEnum.CUSTOMER.value
    }
    return create_access_token(token_data)


# Test Cases

@pytest.mark.asyncio
async def test_check_email_not_exists(client):
    """Test checking non-existent email"""
    response = await client.get("/api/v1/users/check-email/nonexistent@example.com")
    assert response.status_code == 200
    assert response.json()["exists"] is False


@pytest.mark.asyncio
async def test_create_user_success(client, superadmin_token):
    """Test successful user creation"""
    user_data = {
        "first_name": "Test",
        "last_name": "User",
        "email": "test@example.com",
        "gender": "male",
        "phone_number": "+1234567890",
        "location": "Test City",
        "user_role": "customer",
        "job_title": "Tester"
    }
    
    response = await client.post(
        "/api/v1/users/create",
        json=user_data,
        headers={"Authorization": f"Bearer {superadmin_token}"}
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == user_data["email"]
    assert data["first_name"] == user_data["first_name"]
    assert "hashed_password" not in data


@pytest.mark.asyncio
async def test_create_user_duplicate_email(client, superadmin_token):
    """Test creating user with duplicate email"""
    user_data = {
        "first_name": "Test",
        "last_name": "User",
        "email": "duplicate@example.com",
        "gender": "male",
        "user_role": "customer"
    }
    
    # Create first user
    await client.post(
        "/api/v1/users/create",
        json=user_data,
        headers={"Authorization": f"Bearer {superadmin_token}"}
    )
    
    # Try to create duplicate
    response = await client.post(
        "/api/v1/users/create",
        json=user_data,
        headers={"Authorization": f"Bearer {superadmin_token}"}
    )
    
    assert response.status_code == 409


@pytest.mark.asyncio
async def test_create_user_unauthorized(client, customer_token):
    """Test creating user without proper permissions"""
    user_data = {
        "first_name": "Test",
        "last_name": "User",
        "email": "test@example.com",
        "gender": "male",
        "user_role": "customer"
    }
    
    response = await client.post(
        "/api/v1/users/create",
        json=user_data,
        headers={"Authorization": f"Bearer {customer_token}"}
    )
    
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_get_active_users(client, staff_token, superadmin_token):
    """Test getting active users list"""
    # Create a test user first
    user_data = {
        "first_name": "Active",
        "last_name": "User",
        "email": "active@example.com",
        "gender": "female",
        "user_role": "customer"
    }
    
    await client.post(
        "/api/v1/users/create",
        json=user_data,
        headers={"Authorization": f"Bearer {superadmin_token}"}
    )
    
    # Get active users
    response = await client.get(
        "/api/v1/users/active?page=1&page_size=20",
        headers={"Authorization": f"Bearer {staff_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "total" in data
    assert "page" in data
    assert "page_size" in data


@pytest.mark.asyncio
async def test_get_active_users_count(client, staff_token):
    """Test getting active users count"""
    response = await client.get(
        "/api/v1/users/active/count",
        headers={"Authorization": f"Bearer {staff_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "count" in data
    assert isinstance(data["count"], int)


@pytest.mark.asyncio
async def test_update_user_success(client, superadmin_token):
    """Test updating user details"""
    # First create a user
    create_data = {
        "first_name": "Original",
        "last_name": "Name",
        "email": "update@example.com",
        "gender": "male",
        "user_role": "customer"
    }
    
    create_response = await client.post(
        "/api/v1/users/create",
        json=create_data,
        headers={"Authorization": f"Bearer {superadmin_token}"}
    )
    
    user_id = create_response.json()["id"]
    
    # Update the user
    update_data = {
        "id": user_id,
        "first_name": "Updated",
        "last_name": "Name",
        "phone_number": "+9876543210"
    }
    
    response = await client.put(
        "/api/v1/users/update",
        json=update_data,
        headers={"Authorization": f"Bearer {superadmin_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["first_name"] == "Updated"
    assert data["phone_number"] == "+9876543210"


@pytest.mark.asyncio
async def test_search_users(client, staff_token, superadmin_token):
    """Test searching users"""
    # Create test users
    test_users = [
        {"first_name": "John", "last_name": "Doe", "email": "john@example.com"},
        {"first_name": "Jane", "last_name": "Smith", "email": "jane@example.com"},
        {"first_name": "Bob", "last_name": "Johnson", "email": "bob@example.com"}
    ]
    
    for user_data in test_users:
        user_data.update({"gender": "male", "user_role": "customer"})
        await client.post(
            "/api/v1/users/create",
            json=user_data,
            headers={"Authorization": f"Bearer {superadmin_token}"}
        )
    
    # Search for "John"
    response = await client.get(
        "/api/v1/users/search/John",
        headers={"Authorization": f"Bearer {staff_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) > 0
    assert any(user["first_name"] == "John" for user in data["items"])


@pytest.mark.asyncio
async def test_invalid_email_format(client, superadmin_token):
    """Test creating user with invalid email format"""
    user_data = {
        "first_name": "Test",
        "last_name": "User",
        "email": "invalid-email",
        "gender": "male",
        "user_role": "customer"
    }
    
    response = await client.post(
        "/api/v1/users/create",
        json=user_data,
        headers={"Authorization": f"Bearer {superadmin_token}"}
    )
    
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_missing_required_fields(client, superadmin_token):
    """Test creating user with missing required fields"""
    user_data = {
        "first_name": "Test",
        # Missing last_name and email
        "gender": "male"
    }
    
    response = await client.post(
        "/api/v1/users/create",
        json=user_data,
        headers={"Authorization": f"Bearer {superadmin_token}"}
    )
    
    assert response.status_code == 422


# Run tests with: pytest tests/test_user_profile.py -v