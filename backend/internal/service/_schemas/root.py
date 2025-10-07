from pydantic import BaseModel


class GetRootResponse(BaseModel):
    name: str
    version: str
    message: str
