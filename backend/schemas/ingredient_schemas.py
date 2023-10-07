from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class IngredientBase(BaseModel):
    name: str
    
class IngredientCreate(IngredientBase):
    pass

class IngredientResponse(IngredientBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


    class Config:
        orm_mode = True

class RecipeIngredientResponse(IngredientResponse):
    quantity: float
    unit: str

    class Config:
        orm_mode = True

class AddIngredientToRecipe(BaseModel):
    quantity: float
    unit: str