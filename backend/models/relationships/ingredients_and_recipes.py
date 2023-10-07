from sqlalchemy import Table, Column, String, Float, Integer, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from config.database import Base

class IngredientsAndRecipes(Base):
    __tablename__ = "ingredients_and_recipes"

    recipe_id = Column(Integer, ForeignKey("recipes.id"), primary_key=True)
    ingredient_id = Column(Integer, ForeignKey("ingredients.id"), primary_key=True)
    quantity = Column(Float, default=1)
    unit = Column(String(255), default="")

    __table_args__ = (
        CheckConstraint(quantity > 0, name='check_quantity_positive'),
    )
