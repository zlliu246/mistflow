from pydantic import BaseModel

class Input(BaseModel):
    number: int

class Output(BaseModel):
    new_number: int
