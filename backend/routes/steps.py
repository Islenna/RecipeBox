from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from config.database import get_db
from models.Step import Step as StepModel
from schemas.step_schemas import StepCreate, StepResponse, StepUpdate

router = APIRouter()

# Create a new step
@router.post("/steps/new", response_model=List[StepResponse], status_code=status.HTTP_201_CREATED)
def create_steps(steps: List[StepCreate], db: Session = Depends(get_db)):
    # Create a list to store the created steps
    created_steps = []

    for step in steps:
        # Check if the step name already exists
        existing_step = db.query(StepModel).filter_by(name=step.name).first()
        if existing_step:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Step with this name already exists")

        # If the step name is unique, create the new step
        db_step = StepModel(name=step.name)

        # Add the step to the database session
        db.add(db_step)
        created_steps.append(db_step)

    # Commit all the changes to the database
    db.commit()

    # Refresh all the created steps to get their updated information
    for db_step in created_steps:
        db.refresh(db_step)

    return created_steps

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
