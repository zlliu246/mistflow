from pydantic import BaseModel

class Input(BaseModel):
    number: int

class Output(BaseModel):
    squared_number: int
