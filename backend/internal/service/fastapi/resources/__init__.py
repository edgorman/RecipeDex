from typing import Generic, Optional, TypeVar
from pydantic import BaseModel


T = TypeVar("T")


class BaseRequest(BaseModel, Generic[T]):
    data: Optional[T] = None


class BaseResponse(BaseModel, Generic[T]):
    detail: str
    data: Optional[T] = None
