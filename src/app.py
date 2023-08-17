"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Person, Characters, Planets, Favorites
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def get_users ():
    user = User.query.all() #query.all trae todo lo que esta dentro de Planets en una lista
    user_serialized = [user.serialize() for user in user]
    return jsonify(user_serialized)

# def handle_hello():

#     response_body = {
#         "msg": "Hello, this is your GET /user response "
#     }

#     return jsonify(response_body), 200


@app.route('/person/<int:person_id>', methods=['PUT', 'GET'])
def get_single_person(person_id):
    """
    Single person
    """
    body = request.get_json()  # Input: {'username': 'new_username'}
    if request.method == 'PUT':
        user1 = Person.query.get(person_id)
        user1.username = body.username
        db.session.commit()
        return jsonify(user1.serialize()), 200
    if request.method == 'GET':
        user1 = Person.query.get(person_id)
        return jsonify(user1.serialize()), 200
    return "Invalid Method", 404


@app.route('/planets', methods=['GET'])
def get_planets ():
    planets = Planets.query.all() #query.all trae todo lo que esta dentro de Planets en una lista
    planets_serialized = [planet.serialize() for planet in planets]
    return jsonify(planets_serialized)


@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planets_id (planet_id):
    planet = Planets.query.get(planet_id)
    serialized_planet = planet.serialize()
    return jsonify(serialized_planet)


@app.route('/characters', methods=['GET'])
def get_people():
    characters = Characters.query.all()
    characters_serialized = [person.serialize() for person in characters]
    return jsonify(characters_serialized)


@app.route('/characters/<int:character_id>', methods=['GET'])
def get_characters_id (character_id):
    character = Characters.query.get(character_id)
    serialized_character = character.serialize()
    return jsonify(serialized_character)


@app.route('/user/favorites', methods=['GET'])
def get_user_favorites():
    current_user.id = 1  # Esto deberiamos obtenerlo de la autenticación.
    user_favorites = Favorites.query.filter_by(user_id=current_user.id).all()
    serialized_favorites = [favorite.serialize() for favorite in user_favorites]
    return jsonify(serialized_favorites), 200


@app.route('/favorites/planets/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    current_user.id = 1  # Esto deberiamos obtenerlo de la autenticación.
    planet = Planets.query.get(planet_id)
    new_favorite = Favorites(name=planet.name, url=planet.url, user_id=current_user.id)
    db.session.add(new_favorite)
    db.session.commit()

    return jsonify({'message': 'Planet added to favorites'}), 201


@app.route('/favorites/characters/<int:character_id>', methods=['POST'])
def add_favorite_character(character_id):
    current_user.id = 1  # Esto deberiamos obtenerlo de la autenticación.
    character = Characters.query.get(character_id)
    new_favorite2 = Favorites(name=character.name, url=character.url, user_id=current_user.id)
    db.session.add(new_favorite2)
    db.session.commit()

    return jsonify({'message': 'Character added to favorites'}), 201


@app.route('/favorites/planets/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    current_user.id = 1  # Esto deberiamos obtenerlo de la autenticación.
    current_planet = Planets.query.get(id = planet_id)
    favorite_to_delete = Favorites.query.filter_by(user_id=current_user.id, name=current_planet.name).first()

    # if favorite_to_delete is None:
    #     return jsonify({'error': 'Favorite not found'}), 404

    db.session.delete(favorite_to_delete)
    db.session.commit()

    return jsonify({'message': 'Favorite planet deleted'}), 200


@app.route('/favorites/characters/<int:character_id>', methods=['DELETE'])
def delete_favorite_character(character_id):
    current_user.id = 1  # Esto deberiamos obtenerlo de la autenticación.
    favorite_to_delete = Favorites.query.filter_by(user_id=current_user.id, id=character_id).first()

    db.session.delete(favorite_to_delete)
    db.session.commit()

    return jsonify({'message': 'Favorite character deleted'}), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)