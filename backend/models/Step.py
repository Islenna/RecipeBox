from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship, Session
from config.database import Base
from models.Recipe import Recipe
from models.relationships.steps_and_recipes import RecipeSteps



class Step(Base):
    __tablename__="steps"
    id = Column(Integer, primary_key=True, index=True)
    recipe_id = Column(Integer, ForeignKey("recipes.id"), nullable=False)
    sequence = Column(Integer, nullable=False)
    description = Column(String(255), nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    recipe_id = Column(Integer, ForeignKey("recipes.id"), nullable=False)
    recipe = relationship("Recipe", back_populates="steps")