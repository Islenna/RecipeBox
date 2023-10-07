from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship, Session
from config.database import Base
from models.relationships.ingredients_and_recipes import IngredientsAndRecipes


class Ingredient(Base):
    __tablename__="ingredients"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    recipes = relationship("Recipe", secondary=IngredientsAndRecipes.__table__, back_populates="ingredients")