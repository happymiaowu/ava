from gym_foo.model.report.scout_report import ScoutReport


class ScoutHiveReport(ScoutReport):

    def __init__(self, scout_hive_id, target_hive_id, cord, team, round, buff, rein_troops, troops_num):
        super().__init__(scout_hive_id, cord, team, round, rein_troops)
        self._target_hive_id = target_hive_id
        self._buff = buff
        self._troops_num = troops_num

    def get_target_hive_id(self):
        return self._target_hive_id

    def get_buff(self):
        return self._buff

    def get_troops_num(self):
        return self._troops_num

    def __repr__(self):
        return str({
            'scout_hive_id': self._scout_hive_id,
            'target_hive_id': self._target_hive_id,
            'cord': self._cord,
            'round' : self._round,
            'buff': self._buff,
            'rein_troops': self._rein_troops,
            'troops_num': self._troops_num
        })
