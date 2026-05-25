from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError
from models import db, TeamMatchPerformance
from schemas import TeamMatchPerformanceSchema

team_match_performances_bp = Blueprint('team_match_performances', __name__, url_prefix='/api/v1/team_match_performances')

schema = TeamMatchPerformanceSchema()
schemas = TeamMatchPerformanceSchema(many=True)


@team_match_performances_bp.route('', methods=['GET'])
def list_performances():
    performances = TeamMatchPerformance.query.all()
    return jsonify(schemas.dump(performances)), 200


@team_match_performances_bp.route('', methods=['POST'])
def create_performance():
    try:
        data = schema.load(request.get_json())
        perf = TeamMatchPerformance(**data)
        db.session.add(perf)
        db.session.commit()
        return jsonify(schema.dump(perf)), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Already exists'}), 409
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


@team_match_performances_bp.route('/<int:team_id>/<int:match_id>', methods=['GET'])
def get_performance(team_id, match_id):
    perf = TeamMatchPerformance.query.filter_by(TeamID=team_id, MatchID=match_id).first()
    if not perf:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(schema.dump(perf)), 200


@team_match_performances_bp.route('/<int:team_id>/<int:match_id>', methods=['PATCH'])
def update_performance(team_id, match_id):
    perf = TeamMatchPerformance.query.filter_by(TeamID=team_id, MatchID=match_id).first()
    if not perf:
        return jsonify({'error': 'Not found'}), 404

    try:
        data = schema.load(request.get_json(), partial=True)
        for key, value in data.items():
            setattr(perf, key, value)
        db.session.commit()
        return jsonify(schema.dump(perf)), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


@team_match_performances_bp.route('/<int:team_id>/<int:match_id>', methods=['DELETE'])
def delete_performance(team_id, match_id):
    perf = TeamMatchPerformance.query.filter_by(TeamID=team_id, MatchID=match_id).first()
    if not perf:
        return jsonify({'error': 'Not found'}), 404

    try:
        db.session.delete(perf)
        db.session.commit()
        return '', 204
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400
