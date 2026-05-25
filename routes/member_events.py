from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError
from models import db, MemberEvent
from schemas import MemberEventSchema

member_events_bp = Blueprint('member_events', __name__, url_prefix='/api/v1/member-events')

schema = MemberEventSchema()
schemas = MemberEventSchema(many=True)


@member_events_bp.route('', methods=['GET'])
def list_member_events():
    student_id = request.args.get('student_id', type=int)
    event_id = request.args.get('event_id', type=int)

    query = MemberEvent.query
    if student_id:
        query = query.filter_by(StudentID=student_id)
    if event_id:
        query = query.filter_by(EventID=event_id)

    member_events = query.all()
    return jsonify(schemas.dump(member_events)), 200


@member_events_bp.route('', methods=['POST'])
def create_member_event():
    try:
        data = schema.load(request.get_json())
        me = MemberEvent(**data)
        db.session.add(me)
        db.session.commit()
        return jsonify(schema.dump(me)), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Member-Event already exists'}), 409
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


@member_events_bp.route('/<int:student_id>/<int:event_id>', methods=['GET'])
def get_member_event(student_id, event_id):
    me = MemberEvent.query.filter_by(StudentID=student_id, EventID=event_id).first()
    if not me:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(schema.dump(me)), 200


@member_events_bp.route('/<int:student_id>/<int:event_id>', methods=['PATCH'])
def update_member_event(student_id, event_id):
    me = MemberEvent.query.filter_by(StudentID=student_id, EventID=event_id).first()
    if not me:
        return jsonify({'error': 'Not found'}), 404

    try:
        data = schema.load(request.get_json(), partial=True)
        for key, value in data.items():
            setattr(me, key, value)
        db.session.commit()
        return jsonify(schema.dump(me)), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


@member_events_bp.route('/<int:student_id>/<int:event_id>', methods=['DELETE'])
def delete_member_event(student_id, event_id):
    me = MemberEvent.query.filter_by(StudentID=student_id, EventID=event_id).first()
    if not me:
        return jsonify({'error': 'Not found'}), 404

    try:
        db.session.delete(me)
        db.session.commit()
        return '', 204
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400
