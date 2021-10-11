from gym_foo.model.march import March

class BattleFieldTotal():

    def __init__(self, width, height, marches, towers, hives, round_left, battle_reports, scout_reports, rallies):
        self._width = width
        self._height = height
        self._marches = marches
        self._towers = towers
        self._hives = hives
        self._round_left = round_left
        self._battle_reports = battle_reports
        self._scout_reports = scout_reports
        self._rallies = rallies

    def get_width(self):
        return self._width

    def get_height(self):
        return self._height

    def get_marches(self):
        return self._marches

    def get_towers(self):
        return self._towers

    def get_round_left(self):
        return self._round_left

    def get_hives(self):
        return self._hives

    def get_battle_reports(self):
        return self._battle_reports

    def get_scout_reports(self):
        return self._scout_reports

    def get_rallies(self):
        return self._rallies

    def __repr__(self):
        return str({
            'marches': self._marches,
            'tower': self._towers,
            'hives': self._hives,
            'round_left': self._round_left
        })
