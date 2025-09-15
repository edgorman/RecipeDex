from uuid import UUID
from pydantic import BaseModel


class SessionState(BaseModel):
    """Object that will be stored in the state of a Session object"""
    recipe_id: UUID
    user_id: UUID
