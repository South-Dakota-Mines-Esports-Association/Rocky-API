from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError
from models import db, TeamMember
from schemas import TeamMemberSchema

team_members_bp = Blueprint('team_members', __name__, url_prefix='/api/v1/team-members')

schema = TeamMemberSchema()
schemas = TeamMemberSchema(many=True)


@team_members_bp.route('', methods=['GET'])
def list_team_members():
    student_id = request.args.get('student_id', type=int)
    team_id = request.args.get('team_id', type=int)
    role = request.args.get('role')

    query = TeamMember.query
    if student_id:
        query = query.filter_by(StudentID=student_id)
    if team_id:
        query = query.filter_by(TeamID=team_id)
    if role:
        query = query.filter_by(Role=role)

    team_members = query.all()
    return jsonify(schemas.dump(team_members)), 200


@team_members_bp.route('', methods=['POST'])
def create_team_member():
    try:
        data = schema.load(request.get_json())
        tm = TeamMember(**data)
        db.session.add(tm)
        db.session.commit()
        return jsonify(schema.dump(tm)), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Team-Member already exists'}), 409
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


@team_members_bp.route('/<int:student_id>/<int:team_id>', methods=['GET'])
def get_team_member(student_id, team_id):
    tm = TeamMember.query.filter_by(StudentID=student_id, TeamID=team_id).first()
    if not tm:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(schema.dump(tm)), 200


@team_members_bp.route('/<int:student_id>/<int:team_id>', methods=['PATCH'])
def update_team_member(student_id, team_id):
    tm = TeamMember.query.filter_by(StudentID=student_id, TeamID=team_id).first()
    if not tm:
        return jsonify({'error': 'Not found'}), 404

    try:
        data = schema.load(request.get_json(), partial=True)
        for key, value in data.items():
            if key not in ['StudentID', 'TeamID']:
                setattr(tm, key, value)
        db.session.commit()
        return jsonify(schema.dump(tm)), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


@team_members_bp.route('/<int:student_id>/<int:team_id>', methods=['DELETE'])
def delete_team_member(student_id, team_id):
    tm = TeamMember.query.filter_by(StudentID=student_id, TeamID=team_id).first()
    if not tm:
        return jsonify({'error': 'Not found'}), 404

    try:
        db.session.delete(tm)
        db.session.commit()
        return '', 204
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400
