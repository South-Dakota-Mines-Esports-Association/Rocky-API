from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError
from models import db, Match
from schemas import MatchSchema

matches_bp = Blueprint('matches', __name__, url_prefix='/api/v1/matches')

match_schema = MatchSchema()
matches_schema = MatchSchema(many=True)


@matches_bp.route('', methods=['GET'])
def list_matches():
    starts_after = request.args.get('starts_after')
    starts_before = request.args.get('starts_before')

    query = Match.query
    if starts_after:
        query = query.filter(Match.StartTime >= starts_after)
    if starts_before:
        query = query.filter(Match.StartTime <= starts_before)

    matches = query.all()
    return jsonify(matches_schema.dump(matches)), 200


@matches_bp.route('', methods=['POST'])
def create_match():
    try:
        data = match_schema.load(request.get_json())
        match = Match(**data)
        db.session.add(match)
        db.session.commit()
        return jsonify(match_schema.dump(match)), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Match already exists'}), 409
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


@matches_bp.route('/<int:match_id>', methods=['GET'])
def get_match(match_id):
    match = Match.query.get(match_id)
    if not match:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(match_schema.dump(match)), 200


@matches_bp.route('/<int:match_id>', methods=['PATCH'])
def update_match(match_id):
    match = Match.query.get(match_id)
    if not match:
        return jsonify({'error': 'Not found'}), 404

    try:
        data = match_schema.load(request.get_json(), partial=True)
        for key, value in data.items():
            setattr(match, key, value)
        db.session.commit()
        return jsonify(match_schema.dump(match)), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


@matches_bp.route('/<int:match_id>', methods=['DELETE'])
def delete_match(match_id):
    match = Match.query.get(match_id)
    if not match:
        return jsonify({'error': 'Not found'}), 404

    try:
        db.session.delete(match)
        db.session.commit()
        return '', 204
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400
