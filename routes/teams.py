from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError
from models import db, Team, TeamMember, TeamMatchPerformance, MemberGame
from schemas import TeamSchema, TeamRecordSchema, MemberSchema

teams_bp = Blueprint('teams', __name__, url_prefix='/api/v1/teams')

team_schema = TeamSchema()
teams_schema = TeamSchema(many=True)
team_record_schema = TeamRecordSchema()
member_schema = MemberSchema()


@teams_bp.route('', methods=['GET'])
def list_teams():
    game_id = request.args.get('game_id', type=int)
    season = request.args.get('season')

    query = Team.query
    if game_id:
        query = query.filter_by(GameID=game_id)
    if season:
        query = query.filter_by(Season=season)

    teams = query.all()
    return jsonify(teams_schema.dump(teams)), 200


@teams_bp.route('', methods=['POST'])
def create_team():
    try:
        data = team_schema.load(request.get_json())
        team = Team(**data)
        db.session.add(team)
        db.session.commit()
        return jsonify(team_schema.dump(team)), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Team already exists'}), 409
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


@teams_bp.route('/<int:team_id>', methods=['GET'])
def get_team(team_id):
    team = Team.query.get(team_id)
    if not team:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(team_schema.dump(team)), 200


@teams_bp.route('/<int:team_id>', methods=['PATCH'])
def update_team(team_id):
    team = Team.query.get(team_id)
    if not team:
        return jsonify({'error': 'Not found'}), 404

    try:
        data = team_schema.load(request.get_json(), partial=True)
        for key, value in data.items():
            setattr(team, key, value)
        db.session.commit()
        return jsonify(team_schema.dump(team)), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


@teams_bp.route('/<int:team_id>', methods=['DELETE'])
def delete_team(team_id):
    team = Team.query.get(team_id)
    if not team:
        return jsonify({'error': 'Not found'}), 404

    try:
        db.session.delete(team)
        db.session.commit()
        return '', 204
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


@teams_bp.route('/<int:team_id>/members', methods=['GET'])
def get_team_members(team_id):
    team = Team.query.get(team_id)
    if not team:
        return jsonify({'error': 'Not found'}), 404

    team_members = TeamMember.query.filter_by(TeamID=team_id).all()

    result = []
    for tm in team_members:
        member_data = member_schema.dump(tm.member)
        member_data['role'] = tm.Role
        result.append(member_data)

    return jsonify(result), 200


@teams_bp.route('/<int:team_id>/matches', methods=['GET'])
def get_team_matches(team_id):
    from schemas import TeamMatchPerformanceSchema

    team = Team.query.get(team_id)
    if not team:
        return jsonify({'error': 'Not found'}), 404

    performances = TeamMatchPerformance.query.filter_by(TeamID=team_id).all()
    schema = TeamMatchPerformanceSchema(many=True)
    return jsonify(schema.dump(performances)), 200


@teams_bp.route('/<int:team_id>/record', methods=['GET'])
def get_team_record(team_id):
    season = request.args.get('season')

    query = Team.query.filter_by(TeamID=team_id)
    if season:
        query = query.filter_by(Season=season)

    team = query.first()
    if not team:
        return jsonify({'error': 'Not found'}), 404

    return jsonify(team_record_schema.dump(team)), 200
