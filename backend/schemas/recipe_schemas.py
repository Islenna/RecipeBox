from pydantic import BaseModel, validator
from datetime import datetime
from typing import Optional, List, Union
from schemas.ingredient_schemas import IngredientResponse, RecipeIngredientResponse
from models.Recipe import RecipeType  
from schemas.tag_schemas import TagResponse
from schemas.step_schemas import StepResponse

class RecipeBase(BaseModel):
    name: str
    type: RecipeType
    description: str

class RecipeCreate(BaseModel):
    name: str
    type: Union[RecipeType, str]
    description: str
        
    @validator('type', pre=True, always=True)
    def convert_type(cls, v):
        if isinstance(v, RecipeType):
            return v.value
        return v

class RecipeResponse(RecipeBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    tags: List[TagResponse]
    steps: List[StepResponse]
    ingredients: Optional[List[RecipeIngredientResponse]] = []

    class Config:
        orm_mode = True

class RecipesWithIngredientsResponse(RecipeBase):
    id: int
    name: str
    type: RecipeType
    description: str
    ingredients: Optional[List[IngredientResponse]]

    class Config:
        orm_mode = True

class BulkAddRecipeRequest(BaseModel):
    recipes: List[int]

class RecipeUpdate(RecipeBase):
    pass

class RecipeDelete(RecipeBase):
    pass
