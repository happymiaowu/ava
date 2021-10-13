from gym_foo.model.action_list import ActionList
from gym_foo.model.battlefield_detail import BattleField
from gym_foo.model.action.teleport import Teleport
from gym_foo.model.action.attack import Attack
from gym_foo.model.action.recall_occupied import RecallOccupied
from gym_foo.model.action.scout import Scout

class Agent():

    def __init__(self, team):
        self._team = team

    def generate_action(self, state, score, detail: BattleField):
        if self._team == 1:
            action_list = []
            for hive in detail.get_self_hives():
                if hive.get_cord() is None:
                    action_list.append(Teleport(hive_id=hive.get_id(), new_cord=(8, 8)))
            return ActionList(team=1, action_list=action_list)

        action_list = []
        for hive in detail.get_self_hives():
            if hive.get_cord() is None:
                action_list.append(Teleport(hive_id=hive.get_id(), new_cord=(7, 7)))
            break

        for hive in detail.get_self_hives():
            if hive.get_cord() is not None and hive.get_using_march_num() == 0 and score[self._team] == 0:
                action_list.append(Attack(
                    hive_id=hive.get_id(),
                    target_cord=detail.get_towers()[0].get_cord(),
                    troops_num=hive.get_troops_num() // hive.get_max_march_num(),
                    target_type=Attack.TARGET_TYPE_TOWER,
                    target_id=detail.get_towers()[0].get_id()
                ))
            break

        for hive in detail.get_self_hives():
            if hive.get_cord() is not None and hive.get_using_march_num() == 0:
                action_list.append(Scout(hive_id=hive.get_id(), target_type=Scout.TARGET_TYPE_HIVE, target_id='1_0'))
            break

        if score[self._team] > 0:
            for tower in detail.get_towers():
                if tower.who_occupied() == self._team:
                    for occupied in tower.get_troops().get_troops_list():
                        action_list.append(RecallOccupied(hive_id=occupied.get_hive_id(), tower_id=tower.get_id()))





        return ActionList(team=self._team, action_list=action_list)


