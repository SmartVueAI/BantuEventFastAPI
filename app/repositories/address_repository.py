"""
Address Repository — Database Operations

All queries exclude soft-deleted records (is_deleted=False).
"""
from typing import List, Optional, Tuple
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, update
from loguru import logger

from app.models.address import Addresses
from app.schemas.address_schema import AddressCreate, AddressUpdate


async def get_address_by_id(
    db: AsyncSession,
    address_id: int,
) -> Optional[Addresses]:
    """Fetch a single address by primary key, excluding soft-deleted rows."""
    try:
        result = await db.execute(
            select(Addresses).where(
                Addresses.id == address_id,
                Addresses.is_deleted == False,
            )
        )
        return result.scalar_one_or_none()
    except Exception as e:
        logger.error(f"Error fetching address {address_id}: {e}")
        raise


async def get_addresses_by_user(
    db: AsyncSession,
    user_id: int,
    skip: int = 0,
    limit: int = 20,
    sort_by: str = "created_at",
    sort_order: str = "desc",
) -> Tuple[List[Addresses], int]:
    """Return paginated list of active (non-deleted) addresses for a user."""
    try:
        base_filter = (
            Addresses.user_id == user_id,
            Addresses.is_deleted == False,
        )

        # Count
        count_query = select(func.count()).select_from(Addresses).where(*base_filter)
        total: int = await db.scalar(count_query) or 0

        # Data
        sort_column = getattr(Addresses, sort_by, Addresses.created_at)
        order_clause = sort_column.desc() if sort_order == "desc" else sort_column.asc()

        query = (
            select(Addresses)
            .where(*base_filter)
            .order_by(order_clause)
            .offset(skip)
            .limit(limit)
        )
        result = await db.execute(query)
        addresses = list(result.scalars().all())

        return addresses, total
    except Exception as e:
        logger.error(f"Error listing addresses for user {user_id}: {e}")
        raise


async def count_user_addresses(db: AsyncSession, user_id: int) -> int:
    """Count non-deleted addresses that belong to a user."""
    try:
        result = await db.scalar(
            select(func.count())
            .select_from(Addresses)
            .where(
                Addresses.user_id == user_id,
                Addresses.is_deleted == False,
            )
        )
        return result or 0
    except Exception as e:
        logger.error(f"Error counting addresses for user {user_id}: {e}")
        raise


async def create_address(
    db: AsyncSession,
    address_data: AddressCreate,
    user_id: int,
    user_email: str,
    created_by: str,
) -> Addresses:
    """Persist a new address record and return the refreshed ORM instance."""
    try:
        db_address = Addresses(
            user_id=user_id,
            user_email=user_email,
            address_type=address_data.address_type,
            address_line1=address_data.address_line1,
            address_line2=address_data.address_line2,
            city=address_data.city,
            state=address_data.state,
            country=address_data.country,
            postal_code=address_data.postal_code,
            contact_name=address_data.contact_name,
            contact_phone=address_data.contact_phone,
            contact_email=address_data.contact_email,
            is_default=address_data.is_default,
            created_by=created_by,
            is_active=True,
            is_deleted=False,
        )
        db.add(db_address)
        await db.flush()
        await db.refresh(db_address)
        logger.info(f"Address created: id={db_address.id} user_id={user_id}")
        return db_address
    except Exception as e:
        logger.error(f"Error creating address for user {user_id}: {e}")
        raise


async def update_address(
    db: AsyncSession,
    db_address: Addresses,
    address_data: AddressUpdate,
    modified_by: str,
) -> Addresses:
    """Apply partial updates to an existing address record."""
    try:
        update_fields = address_data.model_dump(exclude_unset=True)
        for field, value in update_fields.items():
            setattr(db_address, field, value)

        db_address.last_modified_by = modified_by
        db_address.last_modified_date = datetime.utcnow()

        await db.flush()
        await db.refresh(db_address)
        logger.info(f"Address updated: id={db_address.id}")
        return db_address
    except Exception as e:
        logger.error(f"Error updating address {db_address.id}: {e}")
        raise


async def soft_delete_address(
    db: AsyncSession,
    db_address: Addresses,
    deleted_by: str,
) -> Addresses:
    """Mark an address as deleted and inactive without removing the row."""
    try:
        db_address.is_deleted = True
        db_address.is_active = False
        db_address.last_modified_by = deleted_by
        db_address.last_modified_date = datetime.utcnow()

        await db.flush()
        await db.refresh(db_address)
        logger.info(f"Address soft-deleted: id={db_address.id}")
        return db_address
    except Exception as e:
        logger.error(f"Error soft-deleting address {db_address.id}: {e}")
        raise


async def unset_user_default_addresses(db: AsyncSession, user_id: int) -> None:
    """Clear the is_default flag on every non-deleted address for a user.

    Runs as a bulk UPDATE so the entire operation fits within a single
    transaction managed by the calling service.
    """
    try:
        await db.execute(
            update(Addresses)
            .where(
                Addresses.user_id == user_id,
                Addresses.is_deleted == False,
                Addresses.is_default == True,
            )
            .values(is_default=False)
        )
        logger.debug(f"Cleared default flag for all addresses of user {user_id}")
    except Exception as e:
        logger.error(f"Error clearing default addresses for user {user_id}: {e}")
        raise


async def set_address_as_default(
    db: AsyncSession,
    db_address: Addresses,
    modified_by: str,
) -> Addresses:
    """Mark a specific address as the default."""
    try:
        db_address.is_default = True
        db_address.last_modified_by = modified_by
        db_address.last_modified_date = datetime.utcnow()

        await db.flush()
        await db.refresh(db_address)
        logger.info(f"Address set as default: id={db_address.id}")
        return db_address
    except Exception as e:
        logger.error(f"Error setting address {db_address.id} as default: {e}")
        raise
