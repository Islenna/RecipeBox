from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config.database import Base, engine
from models.Recipe import Recipe
from models.Ingredient import Ingredient
from models.Tag import Tag
from models.Step import Step


app = FastAPI()

Base.metadata.create_all(bind=engine)  # Create the database tables

# Add middleware for CORS
origins = [
    "http://localhost:4200",  #Frontend URL for Angular is 4200, not 3000.
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



#Route Imports
from routes.recipes import router as RecipeRouter
from routes.ingredients import router as IngredientRouter
from routes.tags import router as TagRouter
from routes.steps import router as StepRouter

#Routes
app.include_router(RecipeRouter, prefix="/api", tags=["Recipes"])
app.include_router(IngredientRouter, prefix="/api", tags=["Ingredients"])
app.include_router(TagRouter, prefix="/api", tags=["Tags"])
app.include_router(StepRouter, prefix="/api", tags=["Steps"])

