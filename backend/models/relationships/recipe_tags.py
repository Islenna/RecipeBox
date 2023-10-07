from sqlalchemy import Table, Column, Integer, ForeignKey
from config.database import Base

class RecipeTags(Base):
    __tablename__ = "recipe_tags"

    recipe_id = Column(Integer, ForeignKey("recipes.id"), primary_key=True)
    tag_id = Column(Integer, ForeignKey("tags.id"), primary_key=True)