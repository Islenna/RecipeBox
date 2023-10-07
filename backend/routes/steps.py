from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from config.database import get_db
from models.Step import Step as StepModel
from schemas.step_schemas import StepCreate, StepResponse, StepUpdate

router = APIRouter()


@router.post("/steps/new/{recipe_id}", response_model=StepResponse, status_code=status.HTTP_201_CREATED)
def create_step(recipe_id: int, step: StepCreate, db: Session = Depends(get_db)):
    print("Recipe ID:", recipe_id)
    
    # Check if the step number already exists for the given recipe
    existing_step = db.query(StepModel).filter_by(sequence=step.step_number, recipe_id=recipe_id).first()
    if existing_step:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Step with this number already exists for this recipe")

    # Create the new step associated with the specified recipe
    db_step = StepModel(sequence=step.step_number, description=step.description, recipe_id=recipe_id)
    print("Created Step:", db_step)

    # Add the step to the database session
    db.add(db_step)
    db.commit()
    
    print("Step committed to the database")

    return db_step


# Update multiple steps
@router.put("/steps/update", response_model=List[StepResponse])
def update_steps(steps: List[StepUpdate], db: Session = Depends(get_db)):
    # Create a list to store the updated steps
    updated_steps = []

    for step_update in steps:
        db_step = (
            db.query(StepModel)
            .filter(StepModel.id == step_update.id)
            .first()
        )

        if not db_step:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Step with id {step_update.id} not found")

        # Update the step's name
        db_step.name = step_update.name
        updated_steps.append(db_step)

    # Commit all the changes to the database
    db.commit()

    # Refresh all the updated steps to get their updated information
    for db_step in updated_steps:
        db.refresh(db_step)

    return updated_steps

# Delete multiple steps
@router.delete("/steps/delete", response_model=List[StepResponse])
def delete_steps(steps: List[int], db: Session = Depends(get_db)):
    # Create a list to store the deleted steps
    deleted_steps = []

    for step_id in steps:
        db_step = (
            db.query(StepModel)
            .filter(StepModel.id == step_id)
            .first()
        )

        if not db_step:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Step with id {step_id} not found")

        # Delete the step
        db.delete(db_step)
        deleted_steps.append(db_step)

    # Commit all the changes to the database
    db.commit()

    return deleted_steps
