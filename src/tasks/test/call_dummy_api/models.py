from typing import Any
from pydantic import BaseModel

class Input(BaseModel):
    url: str

class Output(BaseModel):
    response: dict[Any, Any]
