"""
Pagination Dependencies
"""
from fastapi import Query
from typing import Optional
from app.core.constants import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE


class PaginationParams:
    """Pagination parameters for list endpoints"""
    
    def __init__(
        self,
        page: int = Query(1, ge=1, description="Page number"),
        page_size: int = Query(
            DEFAULT_PAGE_SIZE,
            ge=1,
            le=MAX_PAGE_SIZE,
            description=f"Items per page (max: {MAX_PAGE_SIZE})"
        ),
        sort_by: str = Query("created_at", description="Field to sort by"),
        sort_order: str = Query(
            "desc",
            pattern="^(asc|desc)$",
            description="Sort order (asc or desc)"
        ),
    ):
        self.page = page
        self.page_size = page_size
        self.skip = (page - 1) * page_size
        self.sort_by = sort_by
        self.sort_order = sort_order


class SearchParams:
    """Search parameters for search endpoints"""
    
    def __init__(
        self,
        search: str = Query(..., min_length=1, description="Search term"),
        page: int = Query(1, ge=1, description="Page number"),
        page_size: int = Query(
            DEFAULT_PAGE_SIZE,
            ge=1,
            le=MAX_PAGE_SIZE,
            description=f"Items per page (max: {MAX_PAGE_SIZE})"
        ),
        sort_by: str = Query("created_at", description="Field to sort by"),
        sort_order: str = Query(
            "desc",
            pattern="^(asc|desc)$",
            description="Sort order (asc or desc)"
        ),
    ):
        self.search = search
        self.page = page
        self.page_size = page_size
        self.skip = (page - 1) * page_size
        self.sort_by = sort_by
        self.sort_order = sort_order