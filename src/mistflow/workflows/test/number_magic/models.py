from pydantic import BaseModel

class Input(BaseModel):
    magic_number: int
    