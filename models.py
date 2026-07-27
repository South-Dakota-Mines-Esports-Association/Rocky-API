from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Member(db.Model):
    __tablename__ = 'MEMBERS'

    StudentID = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=False)
    FirstName = db.Column(db.String(100), nullable=False)
    LastName = db.Column(db.String(100), nullable=False)
    EmailAddress = db.Column(db.String(100), nullable=False)
    DiscordUserID = db.Column(db.String(32), nullable=False)
    DiscordUsername = db.Column(db.String(32), nullable=False)
    AcademicYear = db.Column(db.Enum('Freshman', 'Sophomore', 'Junior', 'Senior', 'Grad'), nullable=False)
    LastActive = db.Colum(db.Date, nullable=True)

    # Relationships
    games = db.relationship('MemberGame', back_populates='member', cascade='all, delete-orphan')
    teams = db.relationship('TeamMember', back_populates='member', cascade='all, delete-orphan')
    events = db.relationship('MemberEvent', back_populates='member', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Member {self.StudentID}: {self.FirstName} {self.LastName}>'


class Game(db.Model):
    __tablename__ = 'GAME'

    GameID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Name = db.Column(db.String(100), nullable=False)
    Logo = db.Column(db.LargeBinary, nullable=False)

    # Relationships
    teams = db.relationship('Team', back_populates='game')
    events = db.relationship('GameEvent', back_populates='game', cascade='all, delete-orphan')
    members = db.relationship('MemberGame', back_populates='game', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Game {self.GameID}: {self.Name}>'


class Event(db.Model):
    __tablename__ = 'EVENT'

    EventID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Name = db.Column(db.String(100), nullable=False)
    StartTime = db.Column(db.DateTime, nullable=False)
    EndTime = db.Column(db.DateTime, nullable=False)
    Location = db.Column(db.String(100), nullable=False)

    # Relationships
    games = db.relationship('GameEvent', back_populates='event', cascade='all, delete-orphan')
    members = db.relationship('MemberEvent', back_populates='event', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Event {self.EventID}: {self.Name}>'


class Match(db.Model):
    __tablename__ = 'MATCHES'

    MatchID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    StartTime = db.Column(db.DateTime, nullable=False)

    # Relationships
    performances = db.relationship('TeamMatchPerformance', back_populates='match', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Match {self.MatchID}>'


class Team(db.Model):
    __tablename__ = 'TEAM'

    TeamID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Name = db.Column(db.String(100), nullable=False)
    Wins = db.Column(db.Integer, default=0)
    Losses = db.Column(db.Integer, default=0)
    Ties = db.Column(db.Integer, default=0)
    Season = db.Column(db.String(4), nullable=False)
    GameID = db.Column(db.Integer, db.ForeignKey('GAME.GameID', ondelete='RESTRICT'), nullable=False)

    # Relationships
    game = db.relationship('Game', back_populates='teams', foreign_keys=[GameID])
    members = db.relationship('TeamMember', back_populates='team', cascade='all, delete-orphan')
    performances = db.relationship('TeamMatchPerformance', back_populates='team', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Team {self.TeamID}: {self.Name}>'


class MemberGame(db.Model):
    __tablename__ = 'MEMBER_GAME'

    StudentID = db.Column(db.Integer, db.ForeignKey('MEMBERS.StudentID', ondelete='CASCADE'), primary_key=True)
    GameID = db.Column(db.Integer, db.ForeignKey('GAME.GameID', ondelete='CASCADE'), primary_key=True)
    Username = db.Column(db.String(32), nullable=True)
    Rank = db.Column(db.String(32), nullable=True)

    # Relationships
    member = db.relationship('Member', back_populates='games', foreign_keys=[StudentID])
    game = db.relationship('Game', back_populates='members', foreign_keys=[GameID])

    def __repr__(self):
        return f'<MemberGame {self.StudentID}-{self.GameID}>'


class TeamMember(db.Model):
    __tablename__ = 'TEAM_MEMBER'

    StudentID = db.Column(db.Integer, db.ForeignKey('MEMBERS.StudentID', ondelete='CASCADE'), primary_key=True)
    TeamID = db.Column(db.Integer, db.ForeignKey('TEAM.TeamID', ondelete='CASCADE'), primary_key=True)
    Role = db.Column(db.Enum('Captain', 'Coach', 'Player', 'Sub'), nullable=False)

    # Relationships
    member = db.relationship('Member', back_populates='teams', foreign_keys=[StudentID])
    team = db.relationship('Team', back_populates='members', foreign_keys=[TeamID])

    def __repr__(self):
        return f'<TeamMember {self.StudentID}-{self.TeamID}: {self.Role}>'


class MemberEvent(db.Model):
    __tablename__ = 'MEMBER_EVENT'

    StudentID = db.Column(db.Integer, db.ForeignKey('MEMBERS.StudentID', ondelete='CASCADE'), primary_key=True)
    EventID = db.Column(db.Integer, db.ForeignKey('EVENT.EventID', ondelete='CASCADE'), primary_key=True)

    # Relationships
    member = db.relationship('Member', back_populates='events', foreign_keys=[StudentID])
    event = db.relationship('Event', back_populates='members', foreign_keys=[EventID])

    def __repr__(self):
        return f'<MemberEvent {self.StudentID}-{self.EventID}>'


class GameEvent(db.Model):
    __tablename__ = 'GAME_EVENT'

    GameID = db.Column(db.Integer, db.ForeignKey('GAME.GameID', ondelete='CASCADE'), primary_key=True)
    EventID = db.Column(db.Integer, db.ForeignKey('EVENT.EventID', ondelete='CASCADE'), primary_key=True)

    # Relationships
    game = db.relationship('Game', back_populates='events', foreign_keys=[GameID])
    event = db.relationship('Event', back_populates='games', foreign_keys=[EventID])

    def __repr__(self):
        return f'<GameEvent {self.GameID}-{self.EventID}>'


class TeamMatchPerformance(db.Model):
    __tablename__ = 'TEAM_MATCH_PERFORMANCE'

    TeamID = db.Column(db.Integer, db.ForeignKey('TEAM.TeamID', ondelete='CASCADE'), primary_key=True)
    MatchID = db.Column(db.Integer, db.ForeignKey('MATCHES.MatchID', ondelete='CASCADE'), primary_key=True)
    Score = db.Column(db.Integer, nullable=True)

    # Relationships
    team = db.relationship('Team', back_populates='performances', foreign_keys=[TeamID])
    match = db.relationship('Match', back_populates='performances', foreign_keys=[MatchID])

    def __repr__(self):
        return f'<TeamMatchPerformance {self.TeamID}-{self.MatchID}: {self.Score}>'
