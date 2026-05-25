from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError
from models import db, MemberGame
from schemas import MemberGameSchema

member_games_bp = Blueprint('member_games', __name__, url_prefix='/api/v1/member-games')

schema = MemberGameSchema()
schemas = MemberGameSchema(many=True)


@member_games_bp.route('', methods=['GET'])
def list_member_games():
    student_id = request.args.get('student_id', type=int)
    game_id = request.args.get('game_id', type=int)

    query = MemberGame.query
    if student_id:
        query = query.filter_by(StudentID=student_id)
    if game_id:
        query = query.filter_by(GameID=game_id)

    member_games = query.all()
    return jsonify(schemas.dump(member_games)), 200


@member_games_bp.route('', methods=['POST'])
def create_member_game():
    try:
        data = schema.load(request.get_json())
        mg = MemberGame(**data)
        db.session.add(mg)
        db.session.commit()
        return jsonify(schema.dump(mg)), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Member-Game already exists'}), 409
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


@member_games_bp.route('/<int:student_id>/<int:game_id>', methods=['GET'])
def get_member_game(student_id, game_id):
    mg = MemberGame.query.filter_by(StudentID=student_id, GameID=game_id).first()
    if not mg:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(schema.dump(mg)), 200


@member_games_bp.route('/<int:student_id>/<int:game_id>', methods=['PATCH'])
def update_member_game(student_id, game_id):
    mg = MemberGame.query.filter_by(StudentID=student_id, GameID=game_id).first()
    if not mg:
        return jsonify({'error': 'Not found'}), 404

    try:
        data = schema.load(request.get_json(), partial=True)
        for key, value in data.items():
            if key not in ['StudentID', 'GameID']:
                setattr(mg, key, value)
        db.session.commit()
        return jsonify(schema.dump(mg)), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


@member_games_bp.route('/<int:student_id>/<int:game_id>', methods=['DELETE'])
def delete_member_game(student_id, game_id):
    mg = MemberGame.query.filter_by(StudentID=student_id, GameID=game_id).first()
    if not mg:
        return jsonify({'error': 'Not found'}), 404

    try:
        db.session.delete(mg)
        db.session.commit()
        return '', 204
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400
