"""
Address Router — Customer Address Management Endpoints

Base prefix: /api/v1/addresses  (registered in app/api/v1/api.py)

Endpoints:
    POST   /                        Create a new address
    GET    /                        List all addresses (paginated)
    GET    /{address_id}            Get a specific address by ID
    PUT    /{address_id}            Update an existing address
    DELETE /{address_id}            Soft-delete an address
    PATCH  /{address_id}/set-default  Set an address as the default
"""
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger

from app.dependencies.database import get_db
from app.dependencies.auth import get_current_user
from app.schemas.address_schema import (
    AddressCreate,
    AddressUpdate,
    AddressResponse,
    AddressListResponse,
)
from app.schemas.common import SuccessResponse
from app.services.address_service import AddressService

router = APIRouter()


# ---------------------------------------------------------------------------
# POST /  — Create address
# ---------------------------------------------------------------------------

@router.post(
    "/",
    response_model=SuccessResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new address",
    description="""
Create a new billing or shipping address for the authenticated customer.

**Business rules:**
- `address_type` is restricted to `billing` and `shipping`.
- If this is the customer's very first address it is automatically set as the default.
- Setting `is_default=true` on a new address will unset the previous default in the same transaction.

**Authentication required.**
    """,
    responses={
        201: {"description": "Address created successfully"},
        400: {"description": "Validation error (e.g. unsupported address_type)"},
        401: {"description": "Not authenticated"},
    },
)
async def create_address(
    address_data: AddressCreate,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Create a new customer address."""
    try:
        service = AddressService(db)
        address = await service.create_address(
            address_data=address_data,
            current_user=current_user,
        )
        return SuccessResponse(
            message="Address created successfully.",
            data=address.model_dump(mode="json"),
        )
    except Exception as e:
        logger.error(f"create_address endpoint error: {e}")
        raise


# ---------------------------------------------------------------------------
# GET /  — List addresses
# ---------------------------------------------------------------------------

@router.get(
    "/",
    response_model=AddressListResponse,
    status_code=status.HTTP_200_OK,
    summary="List customer addresses",
    description="""
Return a paginated list of addresses for the authenticated customer.

Soft-deleted addresses are excluded automatically.

**Authentication required.**
    """,
    responses={
        200: {"description": "Paginated list of addresses"},
        401: {"description": "Not authenticated"},
    },
)
async def list_addresses(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page (max 100)"),
    sort_by: str = Query("created_at", description="Field to sort by"),
    sort_order: str = Query("desc", pattern="^(asc|desc)$", description="Sort direction"),
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """List all addresses for the authenticated customer."""
    try:
        service = AddressService(db)
        skip = (page - 1) * page_size
        return await service.list_addresses(
            current_user=current_user,
            skip=skip,
            limit=page_size,
            sort_by=sort_by,
            sort_order=sort_order,
        )
    except Exception as e:
        logger.error(f"list_addresses endpoint error: {e}")
        raise


# ---------------------------------------------------------------------------
# GET /{address_id}  — Get single address
# ---------------------------------------------------------------------------

@router.get(
    "/{address_id}",
    response_model=AddressResponse,
    status_code=status.HTTP_200_OK,
    summary="Get address by ID",
    description="""
Fetch a specific address by its ID.

The address must belong to the authenticated customer.

**Authentication required.**
    """,
    responses={
        200: {"description": "Address details"},
        403: {"description": "Address belongs to a different user"},
        404: {"description": "Address not found"},
        401: {"description": "Not authenticated"},
    },
)
async def get_address(
    address_id: int,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Retrieve a single address by ID."""
    try:
        service = AddressService(db)
        return await service.get_address(
            address_id=address_id,
            current_user=current_user,
        )
    except Exception as e:
        logger.error(f"get_address endpoint error: {e}")
        raise


# ---------------------------------------------------------------------------
# PUT /{address_id}  — Update address
# ---------------------------------------------------------------------------

@router.put(
    "/{address_id}",
    response_model=SuccessResponse,
    status_code=status.HTTP_200_OK,
    summary="Update an address",
    description="""
Update one or more fields of an existing address.

Only fields included in the request body are changed (partial update).
`address_type` is restricted to `billing` and `shipping`.

The address must belong to the authenticated customer.

**Authentication required.**
    """,
    responses={
        200: {"description": "Address updated successfully"},
        400: {"description": "Validation error"},
        403: {"description": "Address belongs to a different user"},
        404: {"description": "Address not found"},
        401: {"description": "Not authenticated"},
    },
)
async def update_address(
    address_id: int,
    address_data: AddressUpdate,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Update an existing customer address."""
    try:
        service = AddressService(db)
        address = await service.update_address(
            address_id=address_id,
            address_data=address_data,
            current_user=current_user,
        )
        return SuccessResponse(
            message="Address updated successfully.",
            data=address.model_dump(mode="json"),
        )
    except Exception as e:
        logger.error(f"update_address endpoint error: {e}")
        raise


# ---------------------------------------------------------------------------
# DELETE /{address_id}  — Soft-delete address
# ---------------------------------------------------------------------------

@router.delete(
    "/{address_id}",
    response_model=SuccessResponse,
    status_code=status.HTTP_200_OK,
    summary="Delete an address",
    description="""
Soft-delete an address by setting `is_deleted=True` and `is_active=False`.

The row is retained in the database for audit purposes.
The address must belong to the authenticated customer.

**Authentication required.**
    """,
    responses={
        200: {"description": "Address deleted successfully"},
        403: {"description": "Address belongs to a different user"},
        404: {"description": "Address not found"},
        401: {"description": "Not authenticated"},
    },
)
async def delete_address(
    address_id: int,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Soft-delete a customer address."""
    try:
        service = AddressService(db)
        result = await service.delete_address(
            address_id=address_id,
            current_user=current_user,
        )
        return SuccessResponse(
            message="Address deleted successfully.",
            data=result,
        )
    except Exception as e:
        logger.error(f"delete_address endpoint error: {e}")
        raise


# ---------------------------------------------------------------------------
# PATCH /{address_id}/set-default  — Set default address
# ---------------------------------------------------------------------------

@router.patch(
    "/{address_id}/set-default",
    response_model=SuccessResponse,
    status_code=status.HTTP_200_OK,
    summary="Set address as default",
    description="""
Designate an address as the customer's primary / default address.

The previous default is unset atomically in the same database transaction,
so there is always exactly one default address after this call.

The address must belong to the authenticated customer.

**Authentication required.**
    """,
    responses={
        200: {"description": "Default address updated successfully"},
        403: {"description": "Address belongs to a different user"},
        404: {"description": "Address not found"},
        401: {"description": "Not authenticated"},
    },
)
async def set_default_address(
    address_id: int,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Set an address as the customer's default address."""
    try:
        service = AddressService(db)
        address = await service.set_default_address(
            address_id=address_id,
            current_user=current_user,
        )
        return SuccessResponse(
            message="Default address updated successfully.",
            data=address.model_dump(mode="json"),
        )
    except Exception as e:
        logger.error(f"set_default_address endpoint error: {e}")
        raise
