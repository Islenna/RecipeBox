from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from config.database import get_db, SessionLocal
from models.Tag import Tag as TagModel
from models.Recipe import Recipe as RecipeModel
from schemas.recipe_schemas import RecipeCreate, RecipeResponse
from schemas.tag_schemas import TagCreate, TagResponse

router = APIRouter()

#Create a new tag
@router.post("/tag/new", response_model=TagResponse, status_code=status.HTTP_201_CREATED)
def create_tag(tag: TagCreate, db: Session = Depends(get_db)):
    # Check if the tag name already exists
    existing_tag = db.query(TagModel).filter_by(name=tag.name).first()
    if existing_tag:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tag with this name already exists")

    # If the tag name is unique, create the new tag
    db_tag = TagModel(name=tag.name)
    
    # Use SessionLocal to create a new database session
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)

    return db_tag

#Get a tag
@router.get("/tag/{tag_id}", response_model=TagResponse)
def get_tag(tag_id: int, db: Session = Depends(get_db)):

    db_tag = (
        db.query(TagModel)
        .filter(TagModel.id == tag_id)
        .first()
    )

    if not db_tag:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found")

    return db_tag

#Get all tags
@router.get("/tags", response_model=List[TagResponse])
def get_all_tags(db: Session = Depends(get_db)):
    return db.query(TagModel).all()

#Update a tag
@router.put("/tag/{tag_id}", response_model=TagResponse)
def update_tag(tag_id: int, tag: TagCreate, db: Session = Depends(get_db)):
    db_tag = (
        db.query(TagModel)
        .filter(TagModel.id == tag_id)
        .first()
    )

    if not db_tag:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found")

    db_tag.name = tag.name
    db.commit()
    db.refresh(db_tag)

    return db_tag

#Delete a tag
@router.delete("/tag/{tag_id}", response_model=TagResponse)
def delete_tag(tag_id: int, db: Session = Depends(get_db)):
    db_tag = (
        db.query(TagModel)
        .filter(TagModel.id == tag_id)
        .first()
    )

    if not db_tag:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found")

    db.delete(db_tag)
    db.commit()

    return {"message": "Tag deleted"}

#Add a tag to a recipe
@router.post("/recipe/{recipe_id}/tag/{tag_id}", response_model=RecipeResponse)
def add_tag_to_recipe(recipe_id: int, tag_id: int, db: Session = Depends(get_db)):
    db_recipe = (
        db.query(RecipeModel)
        .filter(RecipeModel.id == recipe_id)
        .first()
    )

    db_tag = (
        db.query(TagModel)
        .filter(TagModel.id == tag_id)
        .first()
    )

    if not db_recipe:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipe not found")

    if not db_tag:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found")

    if db_tag in db_recipe.tags:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tag already added to recipe")
    
    db_recipe.tags.append(db_tag)
    db.commit()
    db.refresh(db_recipe)

    return db_recipe

#Remove a tag from a recipe
@router.delete("/recipe/{recipe_id}/tag/{tag_id}", response_model=RecipeResponse)
def remove_tag_from_recipe(recipe_id: int, tag_id: int, db: Session = Depends(get_db)):
    db_recipe = (
        db.query(RecipeModel)
        .filter(RecipeModel.id == recipe_id)
        .first()
    )

    db_tag = (
        db.query(TagModel)
        .filter(TagModel.id == tag_id)
        .first()
    )

    if not db_recipe:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipe not found")

    if not db_tag:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found")

    if db_tag not in db_recipe.tags:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tag not added to recipe")
    
    db_recipe.tags.remove(db_tag)
    db.commit()
    db.refresh(db_recipe)

    return {"message": "Tag removed from recipe"}

