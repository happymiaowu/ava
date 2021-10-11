

class HideHive():

    def __init__(self, id, team, cord, is_scout=False):
        self._id = id
        self._team = team
        self._is_scout = None
        self._cord = cord
        self._is_scout = is_scout

    def get_id(self):
        return self._id

    def get_team(self):
        return self._team

    def get_cord(self):
        return self._cord

    def is_scout(self):
        return self._is_scout