from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError
from models import db, GameEvent
from schemas import GameEventSchema

game_events_bp = Blueprint('game_events', __name__, url_prefix='/api/v1/game-events')

schema = GameEventSchema()
schemas = GameEventSchema(many=True)


@game_events_bp.route('', methods=['GET'])
def list_game_events():
    game_id = request.args.get('game_id', type=int)
    event_id = request.args.get('event_id', type=int)

    query = GameEvent.query
    if game_id:
        query = query.filter_by(GameID=game_id)
    if event_id:
        query = query.filter_by(EventID=event_id)

    game_events = query.all()
    return jsonify(schemas.dump(game_events)), 200


@game_events_bp.route('', methods=['POST'])
def create_game_event():
    try:
        data = schema.load(request.get_json())
        ge = GameEvent(**data)
        db.session.add(ge)
        db.session.commit()
        return jsonify(schema.dump(ge)), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Game-Event already exists'}), 409
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


@game_events_bp.route('/<int:game_id>/<int:event_id>', methods=['GET'])
def get_game_event(game_id, event_id):
    ge = GameEvent.query.filter_by(GameID=game_id, EventID=event_id).first()
    if not ge:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(schema.dump(ge)), 200


@game_events_bp.route('/<int:game_id>/<int:event_id>', methods=['PATCH'])
def update_game_event(game_id, event_id):
    ge = GameEvent.query.filter_by(GameID=game_id, EventID=event_id).first()
    if not ge:
        return jsonify({'error': 'Not found'}), 404

    try:
        data = schema.load(request.get_json(), partial=True)
        for key, value in data.items():
            setattr(ge, key, value)
        db.session.commit()
        return jsonify(schema.dump(ge)), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


@game_events_bp.route('/<int:game_id>/<int:event_id>', methods=['DELETE'])
def delete_game_event(game_id, event_id):
    ge = GameEvent.query.filter_by(GameID=game_id, EventID=event_id).first()
    if not ge:
        return jsonify({'error': 'Not found'}), 404

    try:
        db.session.delete(ge)
        db.session.commit()
        return '', 204
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400
