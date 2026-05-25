from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError
from models import db, Event, MemberEvent
from schemas import EventSchema, MemberSchema

events_bp = Blueprint('events', __name__, url_prefix='/api/v1/events')

event_schema = EventSchema()
events_schema = EventSchema(many=True)
member_schema = MemberSchema()


@events_bp.route('', methods=['GET'])
def list_events():
    starts_after = request.args.get('starts_after')
    starts_before = request.args.get('starts_before')

    query = Event.query
    if starts_after:
        query = query.filter(Event.StartTime >= starts_after)
    if starts_before:
        query = query.filter(Event.StartTime <= starts_before)

    events = query.all()
    return jsonify(events_schema.dump(events)), 200


@events_bp.route('', methods=['POST'])
def create_event():
    try:
        data = event_schema.load(request.get_json())
        event = Event(**data)
        db.session.add(event)
        db.session.commit()
        return jsonify(event_schema.dump(event)), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Event already exists'}), 409
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


@events_bp.route('/<int:event_id>', methods=['GET'])
def get_event(event_id):
    event = Event.query.get(event_id)
    if not event:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(event_schema.dump(event)), 200


@events_bp.route('/<int:event_id>', methods=['PATCH'])
def update_event(event_id):
    event = Event.query.get(event_id)
    if not event:
        return jsonify({'error': 'Not found'}), 404

    try:
        data = event_schema.load(request.get_json(), partial=True)
        for key, value in data.items():
            setattr(event, key, value)
        db.session.commit()
        return jsonify(event_schema.dump(event)), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


@events_bp.route('/<int:event_id>', methods=['DELETE'])
def delete_event(event_id):
    event = Event.query.get(event_id)
    if not event:
        return jsonify({'error': 'Not found'}), 404

    try:
        db.session.delete(event)
        db.session.commit()
        return '', 204
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


@events_bp.route('/<int:event_id>/members', methods=['GET'])
def get_event_members(event_id):
    event = Event.query.get(event_id)
    if not event:
        return jsonify({'error': 'Not found'}), 404

    member_events = MemberEvent.query.filter_by(EventID=event_id).all()
    result = [member_schema.dump(me.member) for me in member_events]
    return jsonify(result), 200
