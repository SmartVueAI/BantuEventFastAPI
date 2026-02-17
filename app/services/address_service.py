"""
Address Service — Business Logic Layer

Enforces ownership rules, the single-default constraint, and audit logging.
All database mutations are committed (or rolled back) here.
"""
import json
import math
from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger

from app.repositories.address_repository import (
    get_address_by_id,
    get_addresses_by_user,
    count_user_addresses,
    create_address as repo_create_address,
    update_address as repo_update_address,
    soft_delete_address as repo_soft_delete_address,
    unset_user_default_addresses,
    set_address_as_default as repo_set_address_as_default,
)
from app.schemas.address_schema import (
    AddressCreate,
    AddressUpdate,
    AddressResponse,
    AddressListResponse,
)
from app.services.audit_service import AuditService
from app.enums import AuditTypeEnum
from app.exceptions import InsufficientPermissionsException, UserNotFoundException


class AddressService:
    """Business logic for customer address management."""

    def __init__(self, db: AsyncSession) -> None:
        self.db = db
        self.audit_service = AuditService(db)

    # ------------------------------------------------------------------
    # Create
    # ------------------------------------------------------------------

    async def create_address(
        self,
        address_data: AddressCreate,
        current_user: dict,
    ) -> AddressResponse:
        """Create a new address for the authenticated customer.

        Business rules:
        - If this is the user's first address, mark it as default regardless
          of the ``is_default`` flag in the request.
        - If ``is_default=True`` is requested, unset any existing default first.
        """
        try:
            user_id: int = current_user["id"]
            user_email: str = current_user["email"]

            existing_count = await count_user_addresses(self.db, user_id)
            is_first_address = existing_count == 0

            # If is_default requested (or it's the first address), clear the old default
            should_be_default = address_data.is_default or is_first_address
            if should_be_default and not is_first_address:
                await unset_user_default_addresses(self.db, user_id)

            # Override is_default when it's the very first address
            if is_first_address:
                address_data = address_data.model_copy(update={"is_default": True})

            db_address = await repo_create_address(
                db=self.db,
                address_data=address_data,
                user_id=user_id,
                user_email=user_email,
                created_by=user_email,
            )

            await self.audit_service.log_audit(
                audit_type=AuditTypeEnum.CREATE,
                user_role=current_user.get("user_role"),
                module_name="Address Management",
                table_name="addresses",
                processor_email=user_email,
                processed_by=user_email,
                new_values=json.dumps({
                    "id": db_address.id,
                    "user_id": db_address.user_id,
                    "address_type": db_address.address_type.value,
                    "is_default": db_address.is_default,
                }),
            )

            await self.db.commit()
            return AddressResponse.model_validate(db_address)

        except Exception as e:
            logger.error(f"AddressService.create_address error: {e}")
            await self.db.rollback()
            raise

    # ------------------------------------------------------------------
    # List
    # ------------------------------------------------------------------

    async def list_addresses(
        self,
        current_user: dict,
        skip: int = 0,
        limit: int = 20,
        sort_by: str = "created_at",
        sort_order: str = "desc",
    ) -> AddressListResponse:
        """Return a paginated list of the authenticated user's addresses."""
        try:
            user_id: int = current_user["id"]

            addresses, total = await get_addresses_by_user(
                db=self.db,
                user_id=user_id,
                skip=skip,
                limit=limit,
                sort_by=sort_by,
                sort_order=sort_order,
            )

            pages = math.ceil(total / limit) if total > 0 else 0
            current_page = (skip // limit) + 1 if limit > 0 else 1

            return AddressListResponse(
                items=[AddressResponse.model_validate(a) for a in addresses],
                total=total,
                page=current_page,
                page_size=limit,
                pages=pages,
                has_next=current_page < pages,
                has_previous=current_page > 1,
            )

        except Exception as e:
            logger.error(f"AddressService.list_addresses error: {e}")
            raise

    # ------------------------------------------------------------------
    # Get single
    # ------------------------------------------------------------------

    async def get_address(
        self,
        address_id: int,
        current_user: dict,
    ) -> AddressResponse:
        """Fetch a single address, verifying it belongs to the current user."""
        try:
            db_address = await get_address_by_id(self.db, address_id)
            if not db_address:
                from fastapi import HTTPException, status
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Address {address_id} not found.",
                )

            if db_address.user_id != current_user["id"]:
                raise InsufficientPermissionsException(
                    detail="You do not have permission to access this address."
                )

            return AddressResponse.model_validate(db_address)

        except Exception as e:
            logger.error(f"AddressService.get_address error: {e}")
            raise

    # ------------------------------------------------------------------
    # Update
    # ------------------------------------------------------------------

    async def update_address(
        self,
        address_id: int,
        address_data: AddressUpdate,
        current_user: dict,
    ) -> AddressResponse:
        """Update an existing address after verifying ownership."""
        try:
            user_email: str = current_user["email"]

            db_address = await get_address_by_id(self.db, address_id)
            if not db_address:
                from fastapi import HTTPException, status
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Address {address_id} not found.",
                )

            if db_address.user_id != current_user["id"]:
                raise InsufficientPermissionsException(
                    detail="You do not have permission to modify this address."
                )

            old_values = {
                "address_type": db_address.address_type.value,
                "address_line1": db_address.address_line1,
                "city": db_address.city,
                "state": db_address.state,
                "country": db_address.country,
                "postal_code": db_address.postal_code,
            }

            updated = await repo_update_address(
                db=self.db,
                db_address=db_address,
                address_data=address_data,
                modified_by=user_email,
            )

            await self.audit_service.log_audit(
                audit_type=AuditTypeEnum.UPDATE,
                user_role=current_user.get("user_role"),
                module_name="Address Management",
                table_name="addresses",
                processor_email=user_email,
                processed_by=user_email,
                old_values=json.dumps(old_values),
                new_values=json.dumps(address_data.model_dump(exclude_unset=True)),
            )

            await self.db.commit()
            return AddressResponse.model_validate(updated)

        except Exception as e:
            logger.error(f"AddressService.update_address error: {e}")
            await self.db.rollback()
            raise

    # ------------------------------------------------------------------
    # Delete (soft)
    # ------------------------------------------------------------------

    async def delete_address(
        self,
        address_id: int,
        current_user: dict,
    ) -> dict:
        """Soft-delete an address after verifying ownership."""
        try:
            user_email: str = current_user["email"]

            db_address = await get_address_by_id(self.db, address_id)
            if not db_address:
                from fastapi import HTTPException, status
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Address {address_id} not found.",
                )

            if db_address.user_id != current_user["id"]:
                raise InsufficientPermissionsException(
                    detail="You do not have permission to delete this address."
                )

            await repo_soft_delete_address(
                db=self.db,
                db_address=db_address,
                deleted_by=user_email,
            )

            await self.audit_service.log_audit(
                audit_type=AuditTypeEnum.DELETE,
                user_role=current_user.get("user_role"),
                module_name="Address Management",
                table_name="addresses",
                processor_email=user_email,
                processed_by=user_email,
                old_values=json.dumps({"id": address_id}),
            )

            await self.db.commit()
            return {"id": address_id, "is_deleted": True}

        except Exception as e:
            logger.error(f"AddressService.delete_address error: {e}")
            await self.db.rollback()
            raise

    # ------------------------------------------------------------------
    # Set default
    # ------------------------------------------------------------------

    async def set_default_address(
        self,
        address_id: int,
        current_user: dict,
    ) -> AddressResponse:
        """Set one address as the user's default in a single transaction.

        Steps (all within one transaction):
        1. Verify the address exists and belongs to the current user.
        2. Bulk-unset ``is_default`` on all other user addresses.
        3. Set ``is_default=True`` on the target address.
        """
        try:
            user_id: int = current_user["id"]
            user_email: str = current_user["email"]

            db_address = await get_address_by_id(self.db, address_id)
            if not db_address:
                from fastapi import HTTPException, status
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Address {address_id} not found.",
                )

            if db_address.user_id != user_id:
                raise InsufficientPermissionsException(
                    detail="You do not have permission to modify this address."
                )

            # Unset any existing default (bulk update, same transaction)
            await unset_user_default_addresses(self.db, user_id)

            # Set the new default
            updated = await repo_set_address_as_default(
                db=self.db,
                db_address=db_address,
                modified_by=user_email,
            )

            await self.audit_service.log_audit(
                audit_type=AuditTypeEnum.UPDATE,
                user_role=current_user.get("user_role"),
                module_name="Address Management",
                table_name="addresses",
                processor_email=user_email,
                processed_by=user_email,
                new_values=json.dumps({"id": address_id, "is_default": True}),
            )

            await self.db.commit()
            return AddressResponse.model_validate(updated)

        except Exception as e:
            logger.error(f"AddressService.set_default_address error: {e}")
            await self.db.rollback()
            raise
