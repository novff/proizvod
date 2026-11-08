from pydantic import BaseModel, Field
class TicketIn(BaseModel):
    title: str = Field(min_length=3, max_length=200)
    description: str = ""
    priority: str = "normal"
    component_id: int | None = None
class TicketStatusIn(BaseModel):
    status: str
class TicketOut(BaseModel):
    id: int; title: str; description: str; priority: str; status: str; component_id: int | None; creator_id: int
    model_config = {"from_attributes": True}
