class Member:
    """
    Class containing information about a member, along with helper functions.
    """
    def __init__(self, StudentID, Email, DiscordID, Username, AcademicYear, FirstName=None, LastName=None):
        self.StudentID = StudentID
        self.FirstName = FirstName
        self.LastName = LastName
        self.EmailAddress = Email
        self.DiscordID = DiscordID
        self.Username = Username
        self.AcademicYear = AcademicYear

        # Check if the names were set
        if FirstName==None or LastName==None:
            # TODO: Check for it being a valid Mines email.
            pre, _ = Email.split("@") # "first.last" "mines.sdsmt.edu"
            self.FirstName, self.LastName = pre.split(".") # "first" "last"
        
        
class Game:
    """
    Class containing information about a Game, along with helper functions
    """

    def __init__(self, GameID, Name, Logo):
        self.GameID = GameID
        self.Name = Name
        self.Logo = Logo

class Event:
    """
    Class containing information about an Event, along with helpers
    """

    def __init__(self, EventID, Name, StartTime, EndTime, Location):
        self.EventID = EventID
        self.Name = Name
        self.StartTime = StartTime
        self.EndTime = EndTime
        self.Location = Location

class Match:
    """
    Class containing information about a Match, along with helpers
    """

    def __init__(self, MatchID, StartTime):
        self.MatchID = MatchID
        self.StartTime = StartTime

class Team:
    """
    Class containing information about a Team, along with helpers
    """

    def __init__(self, TeamID, Name, Wins, Losses, Ties, Season, GameID):
        self.TeamID = TeamID
        self.Name = Name
        self.Wins = Wins
        self.Losses = Losses
        self.Ties = Ties
        self.Season = Season
        self.GameID = GameID

class MEMBER_GAME:
    """
    Class for MEMBER_GAME linking table
    """

    def __init__(self, StudentID, GameID, Username=None, Rank=None):
        self.StudentID = StudentID
        self.GameID = GameID
        self.Username = Username
        self.Rank = Rank

class TEAM_MEMBER:
    """
    Class for TEAM_MEMBER linking table
    """

    valid_roles = ["Captain", "Coach", "Player", "Sub"]

    def __init__(self, StudentID, TeamID, Role):
        self.StudentID = StudentID
        self.TeamID = TeamID
        self.Role = Role
        # TODO: Include logic to validate Role before creating this


class MEMBER_EVENT:
    """
    Class for MEMBER_EVENT linking table
    """

    def __init__(self, StudentID, EventID):
        self.StudentID = StudentID
        self.EventID = EventID

class GAME_EVENT:
    """
    Class for GAME_EVENT linking table
    """

    def __init__(self, GameID, EventID):
        self.GameID = GameID
        self.EventID = EventID


class TEAM_MATCH_PERFORMANCE:
    """
    Class for TEAM_MATCH_PERFORMANCE Linking/info table
    """

    def __init__(self, TeamID, MatchID, Score=None):
        self.TeamID = TeamID
        self.MatchID = MatchID
        self.Score = Score

