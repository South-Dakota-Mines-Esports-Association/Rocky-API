from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError
import base64
from models import db, Game
from schemas import GameSchema

games_bp = Blueprint('games', __name__, url_prefix='/api/v1/games')

game_schema = GameSchema()
games_schema = GameSchema(many=True)


@games_bp.route('', methods=['GET'])
def list_games():
    games = Game.query.all()
    return jsonify(games_schema.dump(games)), 200


@games_bp.route('', methods=['POST'])
def create_game():
    try:
        data = request.get_json()
        if 'logo_base64' in data:
            data['Logo'] = base64.b64decode(data.pop('logo_base64'))

        game = Game(
            Name=data.get('name'),
            Logo=data.get('Logo', b'')
        )
        db.session.add(game)
        db.session.commit()
        return jsonify(game_schema.dump(game)), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Game already exists'}), 409
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


@games_bp.route('/<int:game_id>', methods=['GET'])
def get_game(game_id):
    game = Game.query.get(game_id)
    if not game:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(game_schema.dump(game)), 200


@games_bp.route('/<int:game_id>', methods=['PATCH'])
def update_game(game_id):
    game = Game.query.get(game_id)
    if not game:
        return jsonify({'error': 'Not found'}), 404

    try:
        data = request.get_json()
        if 'name' in data:
            game.Name = data['name']
        if 'logo_base64' in data:
            game.Logo = base64.b64decode(data['logo_base64'])
        db.session.commit()
        return jsonify(game_schema.dump(game)), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


@games_bp.route('/<int:game_id>', methods=['DELETE'])
def delete_game(game_id):
    game = Game.query.get(game_id)
    if not game:
        return jsonify({'error': 'Not found'}), 404

    try:
        db.session.delete(game)
        db.session.commit()
        return '', 204
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400
