
class ScoutReport():

    def __init__(self, scout_hive_id, cord, team, round, rein_troops):
        self._scout_hive_id = scout_hive_id
        self._cord = cord
        self._team = team
        self._round = round
        self._rein_troops = rein_troops


    def get_scout_hive_id(self):
        return self._scout_hive_id

    def get_team(self):
        return self._team

    def get_round(self):
        return self._round

    def get_rein_troops(self):
        return self._rein_troops
