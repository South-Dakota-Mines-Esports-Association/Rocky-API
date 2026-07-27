from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError
from models import db, Member
from schemas import MemberSchema
import datetime

members_bp = Blueprint('members', __name__, url_prefix='/api/v1/members')

member_schema = MemberSchema()
members_schema = MemberSchema(many=True)


@members_bp.route('', methods=['GET'])
def list_members():
    academic_year = request.args.get('academic_year')

    query = Member.query
    if academic_year:
        query = query.filter_by(AcademicYear=academic_year)

    members = query.all()
    return jsonify(members_schema.dump(members)), 200


@members_bp.route('', methods=['POST'])
def create_member():
    try:
        data = member_schema.load(request.get_json())
        member = Member(**data)
        db.session.add(member)
        db.session.commit()
        return jsonify(member_schema.dump(member)), 201
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({'error': 'Member already exists'}), 409
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


@members_bp.route('/<int:student_id>', methods=['GET'])
def get_member(student_id):
    member = Member.query.get(student_id)
    if not member:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(member_schema.dump(member)), 200


@members_bp.route('/<int:student_id>', methods=['PATCH'])
def update_member(student_id):
    member = Member.query.get(student_id)
    if not member:
        return jsonify({'error': 'Not found'}), 404

    try:
        data = member_schema.load(request.get_json(), partial=True)
        for key, value in data.items():
            setattr(member, key, value)
        db.session.commit()
        return jsonify(member_schema.dump(member)), 200
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Data conflict'}), 409
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


@members_bp.route('/<int:student_id>', methods=['DELETE'])
def delete_member(student_id):
    member = Member.query.get(student_id)
    if not member:
        return jsonify({'error': 'Not found'}), 404

    try:
        db.session.delete(member)
        db.session.commit()
        return '', 204
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


@members_bp.route('/ping/<int:student_id>', methods=['POST'])
def ping_member(student_id):
    member = Member.query.get(student_id)
    if not member:
        return jsonify({'error': 'Not found'}), 404

    try:
        data = member_schema.load(request.get_json(), partial=True)
        setattr(member, "LastActive", datetime.date().isoformat())
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Data conflict'}), 409
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400
        
        
