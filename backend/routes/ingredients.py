from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from config.database import get_db, SessionLocal
from models.Ingredient import Ingredient as IngredientModel
from models.relationships.ingredients_and_recipes import IngredientsAndRecipes
from models.Recipe import Recipe as RecipeModel
from schemas.ingredient_schemas import IngredientCreate, IngredientResponse, RecipeIngredientResponse, AddIngredientToRecipe

router = APIRouter()

#Create a new ingredient
@router.post("/ingredient/new", response_model=IngredientResponse, status_code=status.HTTP_201_CREATED)
def create_ingredient(ingredient: IngredientCreate, db: Session = Depends(get_db)):
    # Check if the ingredient name already exists
    existing_ingredient = db.query(IngredientModel).filter_by(name=ingredient.name).first()
    if existing_ingredient:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Ingredient with this name already exists")

    # If the ingredient name is unique, create the new ingredient
    db_ingredient = IngredientModel(name=ingredient.name)
    
    # Use SessionLocal to create a new database session
    db.add(db_ingredient)
    db.commit()
    db.refresh(db_ingredient)

    return db_ingredient

#Add an ingredient to a recipe
@router.post("/ingredient/{ingredient_id}/recipe/{recipe_id}", status_code=status.HTTP_201_CREATED)
def add_ingredient_to_recipe(ingredient_id: int, recipe_id: int, ingredient_data: AddIngredientToRecipe, db: Session = Depends(get_db)):
    # Check if the ingredient exists
    db_ingredient = (
        db.query(IngredientModel)
        .filter(IngredientModel.id == ingredient_id)
        .first()
    )
    if not db_ingredient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ingredient not found")

    # Check if the recipe exists
    db_recipe = (
        db.query(RecipeModel)
        .filter(RecipeModel.id == recipe_id)
        .first()
    )
    if not db_recipe:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipe not found")

    # Check if the ingredient is already in the recipe
    existing_ingredient = (
        db.query(IngredientsAndRecipes)
        .filter(IngredientsAndRecipes.ingredient_id == ingredient_id)
        .filter(IngredientsAndRecipes.recipe_id == recipe_id)
        .first()
    )
    if existing_ingredient:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Ingredient already in recipe")

    # If the ingredient is not already in the recipe, add it
    db_recipe_ingredient = IngredientsAndRecipes(ingredient_id=ingredient_id, recipe_id=recipe_id, quantity=ingredient_data.quantity, unit=ingredient_data.unit)
    db.add(db_recipe_ingredient)
    db.commit()
    db.refresh(db_recipe_ingredient)

    return db_recipe_ingredient

#Get an ingredient
@router.get("/ingredient/{ingredient_id}", response_model=IngredientResponse)
def get_ingredient(ingredient_id: int, db: Session = Depends(get_db)):

    db_ingredient = (
        db.query(IngredientModel)
        .filter(IngredientModel.id == ingredient_id)
        .first()
    )

    if not db_ingredient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ingredient not found")

    return db_ingredient

#Get all ingredients
@router.get("/ingredients", response_model=List[IngredientResponse])
def get_all_ingredients(db: Session = Depends(get_db)):
    return db.query(IngredientModel).all()

#Update an ingredient
@router.put("/ingredient/{ingredient_id}", response_model=IngredientResponse)
def update_ingredient(ingredient_id: int, ingredient: IngredientCreate, db: Session = Depends(get_db)):
    db_ingredient = (
        db.query(IngredientModel)
        .filter(IngredientModel.id == ingredient_id)
        .first()
    )

    if not db_ingredient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ingredient not found")

    db_ingredient.name = ingredient.name


    db.add(db_ingredient)
    db.commit()
    db.refresh(db_ingredient)

    return db_ingredient

#Delete an ingredient
@router.delete("/ingredient/{ingredient_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_ingredient(ingredient_id: int, db: Session = Depends(get_db)):
    db_ingredient = (
        db.query(IngredientModel)
        .filter(IngredientModel.id == ingredient_id)
        .first()
    )

    if not db_ingredient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ingredient not found")
    
    db.delete(db_ingredient)
    db.commit()
    
    return {"detail": "Ingredient deleted"}
