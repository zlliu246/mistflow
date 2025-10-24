from pydantic import BaseModel

class Input(BaseModel):
    number: int
    message: str

class Output(BaseModel):
    squared_number: int
    message: str
