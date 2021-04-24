import json

from flask import request

from setup import create_app
from models import db, Recipe, Step, Event, EventType, Sensor, Measurement


app = create_app()


@app.route('/recipes', methods=['GET', 'POST'])
def recipes_endpoint():
    if request.method == 'GET':
        recipes = Recipe.query.all()
        response = list()
        for recipe in recipes:
            response.append({
                "id": recipe.id,
                "name": recipe.name,
            })
        return json.dumps(response), 200
    else:
        data = request.get_json()
        instance = Recipe(**data)
        db.session.add(instance)
        db.session.commit()
        return json.dumps("Added"), 201


@app.route('/recipes/<recipe_id>', methods=['GET', 'DELETE'])
def recipes_recipe_id_endpoint(recipe_id):
    recipe = Recipe.query.filter_by(id=recipe_id).one()
    if request.method == 'GET':
        response = {
            "id": recipe.id,
            "name": recipe.name,
        }
        return json.dumps(response), 200
    else:
        db.session.delete(recipe)
        return json.dumps("Deleted"), 204


if __name__ == '__main__':
    app.run(debug=True)
