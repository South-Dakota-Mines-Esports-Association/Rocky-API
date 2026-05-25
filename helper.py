from flask import current_app
import api


APPLICATION_ROOT = "/api/v1/"

def getEndpoint(endpoint, method="DEBUG"):
    """
    Create a valid endpoint string using the APPLICATION_ROOT var
    """
    return f"{APPLICATION_ROOT}{endpoint}"
    
def convertMemberJSON(mem):
    """
    Converts a Member object to a Valid Dictionary, which follows the standard
    decided upon
    """
    result = {
        "academic_year": mem.get("AcademicYear"),
        "discord_user_id": mem.get("DiscordUserID"),
        "discord_username": mem.get("DiscordUsername"),
        "email_address": mem.get("EmailAddress"),
        "first_name": mem.get("FirstName"),
        "last_name": mem.get("LastName"),
        "student_id": mem.get("StudentID")
    }

    return result

def rowsToList(rows):
    result = []
    for row in rows:
        result.append(convertMemberJSON(row))

    return result

def convertGameJSON(row):
    """
    Converts a Game database row to a Valid Dictionary
    """
    logo = row.get("Logo")
    # Handle bytes from BLOB columns by decoding to string
    if isinstance(logo, bytes):
        logo = logo.decode('utf-8')
        
    result = {
        "game_id": row.get("GameID"),
        "name": row.get("Name"),
        "logo_base64": logo
    }
    return result


def convertEventJSON(row):
    """
    Converts an Event database row to a Valid Dictionary
    """
    result = {
        "event_id": row.get("EventID"),
        "name": row.get("Name"),
        "start_time": row.get("StartTime").isoformat() if row.get("StartTime") else None,
        "end_time": row.get("EndTime").isoformat() if row.get("EndTime") else None,
        "location": row.get("Location")
    }
    return result


def rowsToEventsList(rows):
    result = []
    for row in rows:
        result.append(convertEventJSON(row))
    return result


def convertMatchJSON(row):
    """
    Converts a Match database row to a Valid Dictionary
    """
    result = {
        "match_id": row.get("MatchID"),
        "start_time": row.get("StartTime").isoformat() if row.get("StartTime") else None
    }
    return result

def rowsToMatchesList(rows):
    result = []
    for row in rows:
        result.append(convertMatchJSON(row))
    return result

def rowsToGamesList(rows):
    result = []
    for row in rows:
        result.append(convertGameJSON(row))
    return result


def convertTeamJSON(row):
    """
    Converts a Team database row to a Valid Dictionary
    """
    result = {
        "team_id": row.get("TeamID"),
        "name": row.get("Name"),
        "wins": row.get("Wins"),
        "losses": row.get("Losses"),
        "ties": row.get("Ties"),
        "season": row.get("Season"),
        "game_id": row.get("GameID")
    }
    return result

def rowsToTeamsList(rows):
    result = []
    for row in rows:
        result.append(convertTeamJSON(row))
    return result


def convertMemberGameJSON(row):
    """
    Converts a MemberGame database row to a Valid Dictionary
    """
    result = {
        "student_id": row.get("StudentID"),
        "game_id": row.get("GameID"),
        "username": row.get("Username"),
        "rank": row.get("Rank")
    }
    return result

def rowsToMemberGamesList(rows):
    result = []
    for row in rows:
        result.append(convertMemberGameJSON(row))
    return result



def convertTeamMemberJSON(row):
    """
    Converts a TeamMember database row to a Valid Dictionary
    """
    result = {
        "student_id": row.get("StudentID"),
        "team_id": row.get("TeamID"),
        "role": row.get("Role")
    }
    return result

def rowsToTeamMembersList(rows):
    result = []
    for row in rows:
        result.append(convertTeamMemberJSON(row))
    return result


def convertMemberEventJSON(row):
    """
    Converts a MemberEvent database row to a Valid Dictionary
    """
    result = {
        "student_id": row.get("StudentID"),
        "event_id": row.get("EventID")
    }
    return result

def rowsToMemberEventsList(rows):
    result = []
    for row in rows:
        result.append(convertMemberEventJSON(row))
    return result

def convertGameEventJSON(row):
    """
    Converts a GameEvent database row to a Valid Dictionary
    """
    result = {
        "game_id": row.get("GameID"),
        "event_id": row.get("EventID")
    }
    return result

def rowsToGameEventsList(rows):
    result = []
    for row in rows:
        result.append(convertGameEventJSON(row))
    return result


def convertTeamMatchPerformanceJSON(row):
    """
    Converts a TeamMatchPerformance database row to a Valid Dictionary
    """
    result = {
        "team_id": row.get("TeamID"),
        "match_id": row.get("MatchID"),
        "score": row.get("Score")
    }
    return result

def rowsToTeamMatchPerformancesList(rows):
    result = []
    for row in rows:
        result.append(convertTeamMatchPerformanceJSON(row))
    return result
