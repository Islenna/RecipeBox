from sqlalchemy import Table, Column, String, Float, Integer, ForeignKey, CheckConstraint
from config.database import Base

class RecipeSteps(Base):
    __tablename__ = "recipe_steps"

    recipe_id = Column(Integer, ForeignKey("recipes.id"), primary_key=True)
    step_id = Column(Integer, ForeignKey("steps.id"), primary_key=True)
    sequence = Column(Integer, nullable=False)

    __table_args__ = (
        CheckConstraint(sequence > 0, name='check_sequence_positive'),
    )