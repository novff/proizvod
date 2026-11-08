from pydantic import BaseModel, Field
class ComponentIn(BaseModel):
    name: str = Field(min_length=2, max_length=160)
    version: str = Field(min_length=1, max_length=60)
    vendor: str = Field(default="Не указан", max_length=160)
    description: str = ""
    status: str = "active"
class ComponentOut(ComponentIn):
    id: int
    model_config = {"from_attributes": True}
