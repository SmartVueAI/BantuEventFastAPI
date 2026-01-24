import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.core.security import get_password_hash


@pytest.mark.asyncio
@pytest.mark.auth
class TestUserAccess:
    """Test suite for User Access Management endpoints"""
    
    async def test_login_success(
        self,
        client: AsyncClient,
        test_customer: User
    ):
        """Test successful login"""
        login_data = {
            "email": "customer@example.com",
            "password": "testpassword123"
        }
        
        response = await client.post(
            "/api/v1/auth/login",
            json=login_data
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"
        assert "user" in data
    
    async def test_login_invalid_email(self, client: AsyncClient):
        """Test login with non-existent email"""
        login_data = {
            "email": "nonexistent@example.com",
            "password": "testpassword123"
        }
        
        response = await client.post(
            "/api/v1/auth/login",
            json=login_data
        )
        
        assert response.status_code == 401
    
    async def test_login_wrong_password(
        self,
        client: AsyncClient,
        test_customer: User
    ):
        """Test login with wrong password"""
        login_data = {
            "email": "customer@example.com",
            "password": "wrongpassword"
        }
        
        response = await client.post(
            "/api/v1/auth/login",
            json=login_data
        )
        
        assert response.status_code == 401
    
    async def test_login_unverified_email(
        self,
        client: AsyncClient,
        db_session: AsyncSession
    ):
        """Test login with unverified email"""
        from app.models.user import User
        from app.enums.enums import UserRoleEnum, GenderEnum
        import uuid
        
        # Create user with unverified email
        user = User(
            first_name="Unverified",
            last_name="User",
            email="unverified@example.com",
            normalized_email="UNVERIFIED@EXAMPLE.COM",
            gender=GenderEnum.MALE,
            user_role=UserRoleEnum.CUSTOMER,
            hashed_password=get_password_hash("testpassword123"),
            security_stamp=str(uuid.uuid4()),
            email_confirmed=False,  # Not confirmed
            is_active=True,
            created_by="system"
        )
        db_session.add(user)
        await db_session.commit()
        
        login_data = {
            "email": "unverified@example.com",
            "password": "testpassword123"
        }
        
        response = await client.post(
            "/api/v1/auth/login",
            json=login_data
        )
        
        assert response.status_code == 403
        assert "email not confirmed" in response.json()["detail"].lower()
    
    async def test_login_account_lockout(
        self,
        client: AsyncClient,
        test_customer: User
    ):
        """Test account lockout after failed attempts"""
        login_data = {
            "email": "customer@example.com",
            "password": "wrongpassword"
        }
        
        # Make 3 failed login attempts
        for _ in range(3):
            response = await client.post(
                "/api/v1/auth/login",
                json=login_data
            )
            assert response.status_code == 401
        
        # Fourth attempt should result in account lockout
        response = await client.post(
            "/api/v1/auth/login",
            json=login_data
        )
        
        assert response.status_code == 403
        assert "locked" in response.json()["detail"].lower()
    
    async def test_forgot_password(
        self,
        client: AsyncClient,
        test_customer: User
    ):
        """Test forgot password request"""
        request_data = {
            "email": "customer@example.com"
        }
        
        response = await client.post(
            "/api/v1/auth/forgot-password",
            json=request_data
        )
        
        assert response.status_code == 200
        assert "email sent" in response.json()["message"].lower()
    
    async def test_forgot_password_nonexistent_email(
        self,
        client: AsyncClient
    ):
        """Test forgot password with non-existent email (should still return success)"""
        request_data = {
            "email": "nonexistent@example.com"
        }
        
        response = await client.post(
            "/api/v1/auth/forgot-password",
            json=request_data
        )
        
        # Should return success to avoid email enumeration
        assert response.status_code == 200
    
    async def test_change_password_success(
        self,
        client: AsyncClient,
        test_customer: User,
        customer_token: str
    ):
        """Test successful password change"""
        change_data = {
            "old_password": "testpassword123",
            "new_password": "NewSecureP@ss123",
            "confirm_password": "NewSecureP@ss123"
        }
        
        response = await client.post(
            "/api/v1/auth/change-password",
            json=change_data,
            headers={"Authorization": f"Bearer {customer_token}"}
        )
        
        assert response.status_code == 200
        assert "changed successfully" in response.json()["message"].lower()
    
    async def test_change_password_wrong_old_password(
        self,
        client: AsyncClient,
        customer_token: str
    ):
        """Test password change with wrong old password"""
        change_data = {
            "old_password": "wrongpassword",
            "new_password": "NewSecureP@ss123",
            "confirm_password": "NewSecureP@ss123"
        }
        
        response = await client.post(
            "/api/v1/auth/change-password",
            json=change_data,
            headers={"Authorization": f"Bearer {customer_token}"}
        )
        
        assert response.status_code == 401
    
    async def test_change_password_mismatch(
        self,
        client: AsyncClient,
        customer_token: str
    ):
        """Test password change with mismatched passwords"""
        change_data = {
            "old_password": "testpassword123",
            "new_password": "NewSecureP@ss123",
            "confirm_password": "DifferentP@ss123"
        }
        
        response = await client.post(
            "/api/v1/auth/change-password",
            json=change_data,
            headers={"Authorization": f"Bearer {customer_token}"}
        )
        
        assert response.status_code == 422
    
    async def test_change_password_weak_password(
        self,
        client: AsyncClient,
        customer_token: str
    ):
        """Test password change with weak password"""
        change_data = {
            "old_password": "testpassword123",
            "new_password": "weak",
            "confirm_password": "weak"
        }
        
        response = await client.post(
            "/api/v1/auth/change-password",
            json=change_data,
            headers={"Authorization": f"Bearer {customer_token}"}
        )
        
        assert response.status_code == 400
    
    async def test_change_password_unauthorized(
        self,
        client: AsyncClient
    ):
        """Test password change without authentication"""
        change_data = {
            "old_password": "testpassword123",
            "new_password": "NewSecureP@ss123",
            "confirm_password": "NewSecureP@ss123"
        }
        
        response = await client.post(
            "/api/v1/auth/change-password",
            json=change_data
        )
        
        assert response.status_code == 403
    
    async def test_verify_email_success(
        self,
        client: AsyncClient,
        db_session: AsyncSession
    ):
        """Test successful email verification"""
        from app.models.user import User
        from app.enums.enums import UserRoleEnum, GenderEnum
        from app.utils.password import generate_token
        import uuid
        
        # Create user with verification token
        token = generate_token(32)
        user = User(
            first_name="Verify",
            last_name="User",
            email="verify@example.com",
            normalized_email="VERIFY@EXAMPLE.COM",
            gender=GenderEnum.MALE,
            user_role=UserRoleEnum.CUSTOMER,
            hashed_password=get_password_hash("testpassword123"),
            security_stamp=str(uuid.uuid4()),
            email_confirmed=False,
            verification_token=token,
            is_active=True,
            created_by="system"
        )
        db_session.add(user)
        await db_session.commit()
        
        verify_data = {
            "email": "verify@example.com",
            "token": token
        }
        
        response = await client.post(
            "/api/v1/auth/verify-email",
            json=verify_data
        )
        
        assert response.status_code == 200
        assert "verified" in response.json()["message"].lower()
    
    async def test_verify_email_invalid_token(
        self,
        client: AsyncClient,
        test_customer: User
    ):
        """Test email verification with invalid token"""
        verify_data = {
            "email": "customer@example.com",
            "token": "invalidtoken123"
        }
        
        response = await client.post(
            "/api/v1/auth/verify-email",
            json=verify_data
        )
        
        assert response.status_code == 401
    
    async def test_resend_verification_email(
        self,
        client: AsyncClient,
        test_customer: User
    ):
        """Test resending verification email"""
        request_data = {
            "email": "customer@example.com"
        }
        
        response = await client.post(
            "/api/v1/auth/resend-verification-email",
            json=request_data
        )
        
        assert response.status_code == 200
    
    async def test_validate_guid_success(
        self,
        client: AsyncClient,
        db_session: AsyncSession,
        test_customer: User
    ):
        """Test successful GUID validation"""
        import uuid
        
        # Set GUID for user
        guid = str(uuid.uuid4())
        test_customer.user_GUID = guid
        await db_session.commit()
        
        validate_data = {
            "email": "customer@example.com",
            "guid": guid
        }
        
        response = await client.post(
            "/api/v1/auth/validate-guid",
            json=validate_data
        )
        
        assert response.status_code == 200
        assert response.json()["valid"] is True
    
    async def test_validate_guid_invalid(
        self,
        client: AsyncClient,
        test_customer: User
    ):
        """Test GUID validation with invalid GUID"""
        import uuid
        
        validate_data = {
            "email": "customer@example.com",
            "guid": str(uuid.uuid4())  # Random GUID
        }
        
        response = await client.post(
            "/api/v1/auth/validate-guid",
            json=validate_data
        )
        
        assert response.status_code == 200
        assert response.json()["valid"] is False


# Run tests with: pytest tests/test_user_access.py -v
