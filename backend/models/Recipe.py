#Recipe Model
from sqlalchemy import Column, Integer, String, DateTime, func, Enum
from sqlalchemy.orm import relationship, Session
from config.database import Base
from models.relationships.ingredients_and_recipes import IngredientsAndRecipes
from models.relationships.recipe_tags import RecipeTags
from models.relationships.steps_and_recipes import RecipeSteps
from enum import Enum as PyEnum

class RecipeType(PyEnum):
    MAIN = "Main"
    SIDE = "Side"
    DESSERT = "Dessert"
    DRINK = "Drink"
    BREAD = "Bread"
    SOUP = "Soup"
    SALAD = "Salad"
    SAUCE = "Sauce"
    MARINADE = "Marinade"
    FINGERFOOD = "Fingerfood"
    SNACK = "Snack"

class Recipe(Base):
    __tablename__="recipes"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, index=True)
    type = Column(String(255), Enum(RecipeType), index=True)
    description = Column(String(255))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    ingredients = relationship("Ingredient", secondary=IngredientsAndRecipes.__table__, back_populates="recipes")
    tags = relationship("Tag", secondary=RecipeTags, back_populates="recipes")
    steps = relationship("Step", secondary=RecipeSteps, back_populates="recipe")

