from enum import Enum
from collections.abc import Iterable
from dataclasses import is_dataclass, asdict
from typing import Any, Dict, Optional, Generic, TypeVar
from uuid import UUID
from pydantic import BaseModel, model_serializer


T = TypeVar("T")


class BaseRequest(BaseModel, Generic[T]):
    data: Optional[T] = None


class BaseResponse(BaseModel, Generic[T]):
    detail: str
    data: Optional[T] = None

    @model_serializer
    def to_dict(self) -> Dict[str, Any]:
        def default(obj: Any) -> Any:
            if isinstance(obj, UUID):
                return str(obj)
            if isinstance(obj, Enum):
                return obj.value
            if isinstance(obj, BaseModel):
                return default(obj.model_dump())
            if is_dataclass(obj):
                return default(asdict(obj))
            if isinstance(obj, dict):
                return {default(k): default(v) for k, v in obj.items()}
            if isinstance(obj, Iterable) and not isinstance(obj, str):
                return [default(v) for v in obj]
            return obj

        return {"detail": self.detail, "data": default(self.data)}
