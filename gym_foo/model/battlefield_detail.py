from gym_foo.model.march import March
from gym_foo.model.battle_field_total import BattleFieldTotal

class BattleField(BattleFieldTotal):

    def __init__(self, battle_field_total:BattleFieldTotal, team):

        super().__init__(
            width=battle_field_total.get_width(),
            height=battle_field_total.get_height(),
            marches=battle_field_total.get_marches(),
            towers=battle_field_total.get_towers(),
            hives=battle_field_total.get_hives(),
            round_left=battle_field_total.get_round_left(),
            battle_reports=battle_field_total.get_battle_reports(),
            scout_reports=battle_field_total.get_scout_reports(),
            rallies=battle_field_total.get_rallies()
        )
        self._team = team
        self._other_team = 1 - int(team)

    def get_hives(self):
        print('closed...')
        return None

    def get_rallies(self):
        print('closed...')
        return None

    def get_marches(self):
        print('closed...')
        return None

    def get_self_marches(self):
        marches = []
        for march in self._marches:
            if int(march.get_hive_id().split('_')[0]) == self._team:
                marches.append(march)

        return marches

    def get_opp_marches(self):
        marches = []
        for march in self._marches:
            if int(march.get_hive_id().split('_')[0]) != self._team:
                marches.append(march.get_hiding_result())
        return marches

    def get_towers(self):
        towers = []
        for tower in self._towers:
            # TODO: scout
            if tower.who_occupied() is not None and int(tower.who_occupied()) != self._team:
                towers.append(tower.generate_hiding_result())
            else:
                towers.append(tower)
        return towers

    def get_opp_hives(self):
        opp_hives = []
        for hive in self._hives[self._other_team]:
            opp_hives.append(hive.generate_hiding_result())
        return opp_hives

    def get_self_hives(self):
        return self._hives[self._team]

    def get_self_rallies(self):
        rallies = []
        for rally in self._rallies:
            if int(rally.get_hive_id().split('_')[0]) == self._team:
                rallies.append(rally)
        return rallies

    def get_opp_rallies(self):
        rallies = []
        for rally in self._rallies:
            if int(rally.get_hive_id().split('_')[0]) != self._team:
                rallies.append(rally)
        return rallies

    def get_scout_reports(self):
        reports = []
        for scout_report in self._scout_reports:
            if scout_report.get_team() == self._team:
                reports.append(scout_report)

        return reports
