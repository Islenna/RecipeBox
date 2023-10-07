def convert_recipe_to_response(db_recipe):
    # Convert the SQLAlchemy ORM object to a dictionary
    recipe_data = {
        "id": db_recipe.id,
        "name": db_recipe.name,
        "type": db_recipe.type,
        "description": db_recipe.description,
        "created_at": db_recipe.created_at,
        "updated_at": db_recipe.updated_at,
        "tags": [tag.__dict__ for tag in db_recipe.tags],
        "steps": [step.__dict__ for step in db_recipe.steps],
        "ingredients": []
    }

    # Convert the ingredient associations to the desired format
    for assoc in db_recipe.ingredient_associations:
        ingredient_data = {
            "id": assoc.ingredient.id,
            "name": assoc.ingredient.name,
            "created_at": assoc.ingredient.created_at,
            "updated_at": assoc.ingredient.updated_at,
            "quantity": assoc.quantity,
            "unit": assoc.unit
        }
        recipe_data["ingredients"].append(ingredient_data)

    return recipe_data