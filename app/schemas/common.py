from pydantic import BaseModel, Field
from typing import Optional, Generic, TypeVar, List
from datetime import datetime

"""
Common Schemas
"""
from typing import Optional, List, Any, Generic, TypeVar
from pydantic import BaseModel, Field

T = TypeVar("T")


class PaginatedResponse(BaseModel, Generic[T]):
    """Generic paginated response schema"""
    items: List[T]
    total: int
    page: int
    page_size: int
    pages: int
    has_next: bool
    has_previous: bool


class SuccessResponse(BaseModel):
    """Generic success response schema"""
    message: str
    data: Optional[Any] = None


class ErrorDetail(BaseModel):
    """Error detail schema"""
    field: str
    message: str


class ErrorResponse(BaseModel):
    """Error response schema"""
    detail: str
    code: Optional[str] = None
    timestamp: str
    path: str
    errors: Optional[List[ErrorDetail]] = None
#===================================================


class PaginationParams(BaseModel):
    """Schema for pagination parameters"""
    page: int = Field(1, ge=1, description="Page number")
    page_size: int = Field(20, ge=1, le=100, description="Items per page")
    sort_by: str = Field("created_at", description="Field to sort by")
    sort_order: str = Field("desc", description="Sort order (asc or desc)")


class PaginatedResponse(BaseModel, Generic[T]):
    """Generic schema for paginated responses"""
    items: List[T]
    total: int = Field(..., description="Total number of items")
    page: int = Field(..., description="Current page number")
    page_size: int = Field(..., description="Number of items per page")
    pages: int = Field(..., description="Total number of pages")
    has_next: bool = Field(..., description="Whether there is a next page")
    has_previous: bool = Field(..., description="Whether there is a previous page")


class SuccessResponse(BaseModel):
    """Schema for success responses"""
    success: bool = True
    message: str
    data: Optional[dict] = None


class ErrorResponse(BaseModel):
    """Schema for error responses"""
    success: bool = False
    detail: str
    code: str
    timestamp: datetime
    path: Optional[str] = None
    errors: Optional[List[dict]] = None


class MessageResponse(BaseModel):
    """Schema for simple message responses"""
    message: str
    detail: Optional[str] = None


class HealthCheckResponse(BaseModel):
    """Schema for health check response"""
    status: str
    service: str
    version: str
    environment: str
    timestamp: float
    database: Optional[str] = None
    redis: Optional[str] = None


class StatusResponse(BaseModel):
    """Schema for status responses"""
    status: str
    message: Optional[str] = None


class CountResponse(BaseModel):
    """Schema for count responses"""
    count: int


class ExistsResponse(BaseModel):
    """Schema for existence check responses"""
    exists: bool


class TokenPayload(BaseModel):
    """Schema for JWT token payload"""
    sub: str  # Subject (usually email)
    role: str  # User role
    exp: Optional[datetime] = None  # Expiry
    type: Optional[str] = None  # Token type (access/refresh)


class FileUploadResponse(BaseModel):
    """Schema for file upload responses"""
    filename: str
    url: str
    size: int
    upload_date: datetime
    message: str = "File uploaded successfully"


class BulkOperationResponse(BaseModel):
    """Schema for bulk operation responses"""
    success_count: int
    failure_count: int
    total: int
    errors: Optional[List[dict]] = None
    message: str


class SortParams(BaseModel):
    """Schema for sorting parameters"""
    sort_by: str = Field("created_at", description="Field to sort by")
    sort_order: str = Field("desc", description="asc or desc")


class FilterParams(BaseModel):
    """Schema for filtering parameters"""
    is_active: Optional[bool] = None
    is_deleted: Optional[bool] = None
    created_after: Optional[datetime] = None
    created_before: Optional[datetime] = None


class DateRangeFilter(BaseModel):
    """Schema for date range filtering"""
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


class SearchParams(BaseModel):
    """Schema for search parameters"""
    query: str = Field(..., min_length=1, max_length=255)
    fields: Optional[List[str]] = None


class BaseTimestamps(BaseModel):
    """Base schema with timestamp fields"""
    created_at: datetime
    created_by: Optional[str]
    last_modified_date: Optional[datetime]
    last_modified_by: Optional[str]


class BaseStatus(BaseModel):
    """Base schema with status fields"""
    is_active: bool = True
    is_deleted: bool = False