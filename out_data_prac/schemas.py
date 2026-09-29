from pydantic import BaseModel

class Requirement(BaseModel):
    id: str
    section: str
    text: str