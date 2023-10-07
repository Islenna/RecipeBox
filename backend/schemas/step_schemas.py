from pydantic import BaseModel, validator
from datetime import datetime
from typing import Optional

class StepBase(BaseModel):
    step_number: int
    description: str

class StepCreate(StepBase):
    pass

class StepResponse(StepBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True

class StepUpdate(StepBase):
    pass

class StepDelete(StepBase):
    pass



