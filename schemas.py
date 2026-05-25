from marshmallow import Schema, fields, pre_dump
import base64


class MemberSchema(Schema):
    student_id = fields.Int(attribute='StudentID', required=True)
    first_name = fields.Str(attribute='FirstName', required=True)
    last_name = fields.Str(attribute='LastName', required=True)
    email_address = fields.Email(attribute='EmailAddress', required=True)
    discord_user_id = fields.Int(attribute='DiscordUserID', allow_none=True)
    discord_username = fields.Str(attribute='DiscordUsername', allow_none=True)
    academic_year = fields.Str(attribute='AcademicYear', required=True)


class GameSchema(Schema):
    game_id = fields.Int(attribute='GameID', required=True)
    name = fields.Str(attribute='Name', required=True)
    logo_base64 = fields.Str(attribute='Logo', allow_none=True)

    @pre_dump
    def handle_logo(self, data, **kwargs):
        if hasattr(data, 'Logo') and data.Logo:
            if isinstance(data.Logo, bytes):
                data.Logo = base64.b64encode(data.Logo).decode('utf-8')
        return data


class EventSchema(Schema):
    event_id = fields.Int(attribute='EventID', required=True)
    name = fields.Str(attribute='Name', required=True)
    start_time = fields.DateTime(attribute='StartTime', required=True, format='iso')
    end_time = fields.DateTime(attribute='EndTime', required=True, format='iso')
    location = fields.Str(attribute='Location', required=True)


class MatchSchema(Schema):
    match_id = fields.Int(attribute='MatchID', required=True)
    start_time = fields.DateTime(attribute='StartTime', required=True, format='iso')


class TeamSchema(Schema):
    team_id = fields.Int(attribute='TeamID', required=True)
    name = fields.Str(attribute='Name', required=True)
    wins = fields.Int(attribute='Wins', allow_none=True)
    losses = fields.Int(attribute='Losses', allow_none=True)
    ties = fields.Int(attribute='Ties', allow_none=True)
    season = fields.Str(attribute='Season', required=True)
    game_id = fields.Int(attribute='GameID', required=True)


class MemberGameSchema(Schema):
    student_id = fields.Int(attribute='StudentID', required=True)
    game_id = fields.Int(attribute='GameID', required=True)
    username = fields.Str(attribute='Username', allow_none=True)
    rank = fields.Str(attribute='Rank', allow_none=True)


class TeamMemberSchema(Schema):
    student_id = fields.Int(attribute='StudentID', required=True)
    team_id = fields.Int(attribute='TeamID', required=True)
    role = fields.Str(attribute='Role', required=True)


class MemberEventSchema(Schema):
    student_id = fields.Int(attribute='StudentID', required=True)
    event_id = fields.Int(attribute='EventID', required=True)


class GameEventSchema(Schema):
    game_id = fields.Int(attribute='GameID', required=True)
    event_id = fields.Int(attribute='EventID', required=True)


class TeamMatchPerformanceSchema(Schema):
    team_id = fields.Int(attribute='TeamID', required=True)
    match_id = fields.Int(attribute='MatchID', required=True)
    score = fields.Int(attribute='Score', allow_none=True)


class TeamRecordSchema(Schema):
    team_id = fields.Int(attribute='TeamID', dump_only=True)
    season = fields.Str(attribute='Season')
    wins = fields.Int(attribute='Wins')
    losses = fields.Int(attribute='Losses')
    ties = fields.Int(attribute='Ties')


class TeamWithMembersSchema(Schema):
    student_id = fields.Int()
    first_name = fields.Str()
    last_name = fields.Str()
    email_address = fields.Email()
    role = fields.Str()
