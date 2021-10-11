from gym_foo.model.report.scout_report import ScoutReport


class ScoutTowerReport(ScoutReport):

    def __init__(self, scout_hive_id, target_tower_id, cord, team, round, rein_troops):
        super().__init__(scout_hive_id, cord, team, round, rein_troops)
        self._target_tower_id = target_tower_id

    def get_target_tower_id(self):
        return self._target_tower_id

    def __repr__(self):
        return str({
            'scout_hive_id': self._scout_hive_id,
            'target_tower_id': self._target_tower_id,
            'cord': self._cord,
            'round' : self._round,
            'rein_troops': self._rein_troops
        })