from flask import Flask, jsonify
import sys
import os

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from models import db
from config import config


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)

    with app.app_context():
        db.create_all()

    # Register blueprints
    from routes.members import members_bp
    from routes.games import games_bp
    from routes.events import events_bp
    from routes.matches import matches_bp
    from routes.teams import teams_bp
    from routes.member_games import member_games_bp
    from routes.team_members import team_members_bp
    from routes.member_events import member_events_bp
    from routes.game_events import game_events_bp
    from routes.team_match_performances import team_match_performances_bp

    app.register_blueprint(members_bp)
    app.register_blueprint(games_bp)
    app.register_blueprint(events_bp)
    app.register_blueprint(matches_bp)
    app.register_blueprint(teams_bp)
    app.register_blueprint(member_games_bp)
    app.register_blueprint(team_members_bp)
    app.register_blueprint(member_events_bp)
    app.register_blueprint(game_events_bp)
    app.register_blueprint(team_match_performances_bp)

    # Error handlers
    @app.errorhandler(404)
    def not_found(e):
        return jsonify({'error': 'Not found'}), 404

    @app.errorhandler(422)
    def validation_error(e):
        return jsonify({'error': 'Validation failed'}), 422

    return app
