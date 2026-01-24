from typing import Generic, TypeVar, Type, Optional, List, Any, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, update, delete
from sqlalchemy.sql import Select
from pydantic import BaseModel
from datetime import datetime

from app.models.base import BaseDBModel

ModelType = TypeVar("ModelType", bound=BaseDBModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """
    Base CRUD class with default methods for Create, Read, Update, Delete operations
    """
    
    def __init__(self, model: Type[ModelType]):
        """
        Initialize CRUD object with a SQLAlchemy model
        
        Args:
            model: SQLAlchemy model class
        """
        self.model = model
    
    async def get(self, db: AsyncSession, id: int) -> Optional[ModelType]:
        """
        Get a single record by ID
        
        Args:
            db: Database session
            id: Record ID
            
        Returns:
            Model instance or None
        """
        result = await db.execute(
            select(self.model).filter(self.model.id == id)
        )
        return result.scalar_one_or_none()
    
    async def get_by_field(
        self, 
        db: AsyncSession, 
        field_name: str, 
        field_value: Any
    ) -> Optional[ModelType]:
        """
        Get a single record by field name and value
        
        Args:
            db: Database session
            field_name: Name of the field
            field_value: Value to search for
            
        Returns:
            Model instance or None
        """
        result = await db.execute(
            select(self.model).filter(
                getattr(self.model, field_name) == field_value
            )
        )
        return result.scalar_one_or_none()
    
    async def get_multi(
        self,
        db: AsyncSession,
        *,
        skip: int = 0,
        limit: int = 100,
        filters: Optional[Dict[str, Any]] = None,
        order_by: Optional[str] = "created_at",
        order_desc: bool = True
    ) -> tuple[List[ModelType], int]:
        """
        Get multiple records with pagination and filtering
        
        Args:
            db: Database session
            skip: Number of records to skip
            limit: Maximum number of records to return
            filters: Dictionary of field:value pairs for filtering
            order_by: Field to order by
            order_desc: Whether to order descending
            
        Returns:
            Tuple of (list of records, total count)
        """
        # Build query
        query = select(self.model)
        
        # Apply filters
        if filters:
            for field, value in filters.items():
                if hasattr(self.model, field):
                    query = query.filter(getattr(self.model, field) == value)
        
        # Count total
        count_query = select(func.count()).select_from(self.model)
        if filters:
            for field, value in filters.items():
                if hasattr(self.model, field):
                    count_query = count_query.filter(
                        getattr(self.model, field) == value
                    )
        
        total_result = await db.execute(count_query)
        total = total_result.scalar()
        
        # Apply ordering
        if order_by and hasattr(self.model, order_by):
            order_field = getattr(self.model, order_by)
            query = query.order_by(
                order_field.desc() if order_desc else order_field.asc()
            )
        
        # Apply pagination
        query = query.offset(skip).limit(limit)
        
        # Execute query
        result = await db.execute(query)
        items = result.scalars().all()
        
        return items, total
    
    async def create(
        self, 
        db: AsyncSession, 
        *, 
        obj_in: CreateSchemaType,
        created_by: Optional[str] = None
    ) -> ModelType:
        """
        Create a new record
        
        Args:
            db: Database session
            obj_in: Pydantic schema with data to create
            created_by: User who created the record
            
        Returns:
            Created model instance
        """
        obj_in_data = obj_in.model_dump()
        
        # Add metadata
        obj_in_data["created_at"] = datetime.utcnow()
        if created_by:
            obj_in_data["created_by"] = created_by
        
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        await db.flush()
        await db.refresh(db_obj)
        return db_obj
    
    async def update(
        self,
        db: AsyncSession,
        *,
        db_obj: ModelType,
        obj_in: UpdateSchemaType | Dict[str, Any],
        updated_by: Optional[str] = None
    ) -> ModelType:
        """
        Update a record
        
        Args:
            db: Database session
            db_obj: Existing model instance
            obj_in: Pydantic schema or dict with update data
            updated_by: User who updated the record
            
        Returns:
            Updated model instance
        """
        obj_data = db_obj.__dict__
        
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        
        # Update fields
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        
        # Update metadata
        db_obj.last_modified_date = datetime.utcnow()
        if updated_by:
            db_obj.last_modified_by = updated_by
        
        await db.flush()
        await db.refresh(db_obj)
        return db_obj
    
    async def soft_delete(
        self,
        db: AsyncSession,
        *,
        id: int,
        deleted_by: Optional[str] = None
    ) -> Optional[ModelType]:
        """
        Soft delete a record (set is_deleted to True)
        
        Args:
            db: Database session
            id: Record ID
            deleted_by: User who deleted the record
            
        Returns:
            Deleted model instance or None
        """
        db_obj = await self.get(db, id=id)
        if db_obj:
            db_obj.is_deleted = True
            db_obj.is_active = False
            db_obj.last_modified_date = datetime.utcnow()
            if deleted_by:
                db_obj.last_modified_by = deleted_by
            await db.flush()
            await db.refresh(db_obj)
        return db_obj
    
    async def hard_delete(
        self, 
        db: AsyncSession, 
        *, 
        id: int
    ) -> bool:
        """
        Permanently delete a record from database
        
        Args:
            db: Database session
            id: Record ID
            
        Returns:
            True if deleted, False if not found
        """
        db_obj = await self.get(db, id=id)
        if db_obj:
            await db.delete(db_obj)
            await db.flush()
            return True
        return False
    
    async def restore(
        self,
        db: AsyncSession,
        *,
        id: int,
        restored_by: Optional[str] = None
    ) -> Optional[ModelType]:
        """
        Restore a soft-deleted record
        
        Args:
            db: Database session
            id: Record ID
            restored_by: User who restored the record
            
        Returns:
            Restored model instance or None
        """
        db_obj = await self.get(db, id=id)
        if db_obj:
            db_obj.is_deleted = False
            db_obj.is_active = True
            db_obj.last_modified_date = datetime.utcnow()
            if restored_by:
                db_obj.last_modified_by = restored_by
            await db.flush()
            await db.refresh(db_obj)
        return db_obj
    
    async def count(
        self, 
        db: AsyncSession,
        *,
        filters: Optional[Dict[str, Any]] = None
    ) -> int:
        """
        Count records with optional filtering
        
        Args:
            db: Database session
            filters: Dictionary of field:value pairs for filtering
            
        Returns:
            Count of records
        """
        query = select(func.count()).select_from(self.model)
        
        if filters:
            for field, value in filters.items():
                if hasattr(self.model, field):
                    query = query.filter(getattr(self.model, field) == value)
        
        result = await db.execute(query)
        return result.scalar()
    
    async def exists(
        self, 
        db: AsyncSession,
        *,
        filters: Dict[str, Any]
    ) -> bool:
        """
        Check if a record exists with given filters
        
        Args:
            db: Database session
            filters: Dictionary of field:value pairs for filtering
            
        Returns:
            True if exists, False otherwise
        """
        query = select(self.model)
        
        for field, value in filters.items():
            if hasattr(self.model, field):
                query = query.filter(getattr(self.model, field) == value)
        
        query = query.limit(1)
        result = await db.execute(query)
        return result.scalar_one_or_none() is not None