#Recipe Routes

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from typing import List
from config.database import get_db, SessionLocal
from models.Recipe import Recipe as RecipeModel
from schemas.recipe_schemas import RecipeCreate, RecipeResponse


router = APIRouter()

#Create a new recipe
@router.post("/recipe/new", response_model=RecipeResponse, status_code=status.HTTP_201_CREATED)
def create_recipe(recipe: RecipeCreate, db: Session = Depends(get_db)):
    # Check if the recipe name already exists
    existing_recipe = db.query(RecipeModel).filter_by(name=recipe.name).first()
    if existing_recipe:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Recipe with this name already exists")

    # If the recipe name is unique, create the new recipe
    db_recipe = RecipeModel(name=recipe.name, type=recipe.type, description=recipe.description)
    
    # Use SessionLocal to create a new database session
    db.add(db_recipe)
    db.commit()
    db.refresh(db_recipe)

    return db_recipe


#Get a recipe
@router.get("/recipe/{recipe_id}", response_model=RecipeResponse)
def get_recipe(recipe_id: int, db: Session = Depends(get_db)):

    db_recipe = (
        db.query(RecipeModel)
        .filter(RecipeModel.id == recipe_id)
        .first()
    )

    if not db_recipe:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipe not found")

    return db_recipe

#Get all recipes
@router.get("/recipes", response_model=List[RecipeResponse])
def get_all_recipes(db: Session = Depends(get_db)):
    return db.query(RecipeModel).all()

#Update a recipe
@router.put("/recipe/{recipe_id}", response_model=RecipeResponse)
def update_recipe(recipe_id: int, recipe: RecipeCreate, db: Session = Depends(get_db)):
    db_recipe = (
        db.query(RecipeModel)
        .filter(RecipeModel.id == recipe_id)
        .first()
    )

    if not db_recipe:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipe not found")

    db_recipe.name = recipe.name
    db_recipe.type = recipe.type
    db_recipe.description = recipe.description

    db.add(db_recipe)
    db.commit()
    db.refresh(db_recipe)

    return db_recipe

#Delete a recipe
@router.delete("/recipe/{recipe_id}", response_model=RecipeResponse)
def delete_recipe(recipe_id: int, db: Session = Depends(get_db)):
    db_recipe = (
        db.query(RecipeModel)
        .filter(RecipeModel.id == recipe_id)
        .first()
    )

    if not db_recipe:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipe not found")

    db.delete(db_recipe)
    db.commit()

    return db_recipe

# Get a recipe along with its associated tags
@router.get("/recipe/{recipe_id}/with_tags", response_model=RecipeResponse)
def get_recipe_with_tags(recipe_id: int, db: Session = Depends(get_db)):
    db_recipe = (
        db.query(RecipeModel)
        .filter(RecipeModel.id == recipe_id)
        .options(joinedload(RecipeModel.tags))
        .first()
    )

    if not db_recipe:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipe not found")

    return db_recipe