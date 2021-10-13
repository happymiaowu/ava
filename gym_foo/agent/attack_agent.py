from gym_foo.model.action_list import ActionList
from gym_foo.model.battlefield_detail import BattleField
from gym_foo.model.action.teleport import Teleport
from gym_foo.model.action.attack import Attack
from gym_foo.model.action.recall_occupied import RecallOccupied
from gym_foo.model.action.scout import Scout
from gym_foo.agent.agent import Agent
from gym_foo.model.tower import Tower
from gym_foo.model.hide_hive import HideHive
from gym_foo.model.action.reinforce import Reinforce
from gym_foo.model.action.rally import Rally
import random
from gym_foo.model.action.speedup import SpeedUp
from gym_foo.model.hive import Hive
from typing import List, Dict
from gym_foo.model.action.recall_march import RecallMarch
from gym_foo.model.march import March
from gym_foo.model.action.join_rally import JoinRally
from gym_foo.model.action.rally_cancel import RallyCancel

# 抓着对方城池打，必输无疑的那种
class AttackOppAgent(Agent):

    def __init__(self, team):
        super().__init__(team)

    valid_action = ['attack', 'reinforce', 'rally', 'scout', 'speedup', 'teleport', 'recall_march', 'recall_occupied', 'join_rally', 'cancel_rally']

    # 行军数量是否满
    def is_march_num_full(self, hive):
        return hive.get_using_march_num() == hive.get_max_march_num()

    def is_teleport_left(self, hive):
        return hive.get_teleport_times() > 0

    def get_empty_cord(self, width, height, self_hives: List[Hive], opp_hives: List[Hive], towers: List[Tower]):
        empty_cord = set([(w, h) for w in range(width) for h in range(height)])
        empty_cord -= set([hive.get_cord() for hive in self_hives])
        empty_cord -= set([hive.get_cord() for hive in opp_hives])
        print(towers)
        empty_cord -= set([tower.get_cord() for tower in towers])
        return empty_cord

    def generate_action(self, state, score, detail: BattleField):
        action_list = []
        tower = detail.get_towers()
        opp_hives = detail.get_opp_hives()
        empty_cord = self.get_empty_cord(detail.get_width(), detail.get_height(), detail.get_self_hives(), detail.get_opp_hives(), detail.get_towers())

        for hive in detail.get_self_hives():

            if self.is_march_num_full(hive):
                    continue
            # 朝着对方城池打
            target = random.choice(opp_hives)
            action_list.append(
                Attack(
                    hive_id=hive.get_id(),
                    target_cord=target.get_cord(),
                    troops_num=random.randint(1, min(hive.get_max_troops_num(), hive.get_troops_num())),
                    target_type=Attack.TARGET_TYPE_TOWER if type(target) == Tower else Attack.TARGET_TYPE_HIVE,
                    target_id=target.get_id()
                )
            )

        return ActionList(team=self._team, action_list=action_list)

# 努力占塔
class AttackTowerAgent(Agent):

    def __init__(self, team):
        super().__init__(team)

    valid_action = ['attack', 'reinforce', 'rally', 'scout', 'speedup', 'teleport', 'recall_march', 'recall_occupied', 'join_rally', 'cancel_rally']

    # 行军数量是否满
    def is_march_num_full(self, hive):
        return hive.get_using_march_num() == hive.get_max_march_num()

    def is_teleport_left(self, hive):
        return hive.get_teleport_times() > 0

    def get_empty_cord(self, width, height, self_hives: List[Hive], opp_hives: List[Hive], towers: List[Tower]):
        empty_cord = set([(w, h) for w in range(width) for h in range(height)])
        empty_cord -= set([hive.get_cord() for hive in self_hives])
        empty_cord -= set([hive.get_cord() for hive in opp_hives])
        print(towers)
        empty_cord -= set([tower.get_cord() for tower in towers])
        return empty_cord

    def generate_action(self, state, score, detail: BattleField):
        action_list = []
        tower = detail.get_towers()
        opp_hives = detail.get_opp_hives()
        empty_cord = self.get_empty_cord(detail.get_width(), detail.get_height(), detail.get_self_hives(), detail.get_opp_hives(), detail.get_towers())

        for hive in detail.get_self_hives():
            if self.is_march_num_full(hive):
                    continue
            # 就算是己方的，也往里打，因为会自动被当作增援
            target = random.choice(tower)
            action_list.append(
                Attack(
                    hive_id=hive.get_id(),
                    target_cord=target.get_cord(),
                    troops_num=random.randint(1, min(hive.get_max_troops_num(), hive.get_troops_num())),
                    target_type=Attack.TARGET_TYPE_TOWER if type(target) == Tower else Attack.TARGET_TYPE_HIVE,
                    target_id=target.get_id()
                )
            )

        return ActionList(team=self._team, action_list=action_list)

# 只占主塔，不管其他
class AttackMainTowerAgent(Agent):

    def __init__(self, team):
        super().__init__(team)

    valid_action = ['attack', 'reinforce', 'rally', 'scout', 'speedup', 'teleport', 'recall_march', 'recall_occupied', 'join_rally', 'cancel_rally']

    # 行军数量是否满
    def is_march_num_full(self, hive):
        return hive.get_using_march_num() == hive.get_max_march_num()

    def is_teleport_left(self, hive):
        return hive.get_teleport_times() > 0

    def get_empty_cord(self, width, height, self_hives: List[Hive], opp_hives: List[Hive], towers: List[Tower]):
        empty_cord = set([(w, h) for w in range(width) for h in range(height)])
        empty_cord -= set([hive.get_cord() for hive in self_hives])
        empty_cord -= set([hive.get_cord() for hive in opp_hives])
        print(towers)
        empty_cord -= set([tower.get_cord() for tower in towers])
        return empty_cord

    def generate_action(self, state, score, detail: BattleField):
        action_list = []
        tower = detail.get_towers()
        opp_hives = detail.get_opp_hives()
        empty_cord = self.get_empty_cord(detail.get_width(), detail.get_height(), detail.get_self_hives(), detail.get_opp_hives(), detail.get_towers())

        for hive in detail.get_self_hives():
            if self.is_march_num_full(hive):
                    continue
            # 就算是己方的，也往里打，因为会自动被当作增援
            target = tower[0]
            action_list.append(
                Attack(
                    hive_id=hive.get_id(),
                    target_cord=target.get_cord(),
                    troops_num=random.randint(1, min(hive.get_max_troops_num(), hive.get_troops_num())),
                    target_type=Attack.TARGET_TYPE_TOWER if type(target) == Tower else Attack.TARGET_TYPE_HIVE,
                    target_id=target.get_id()
                )
            )

        return ActionList(team=self._team, action_list=action_list)

# 将城池移到最靠近主塔的位置，然后占主塔
class TowerRushAgent(Agent):
    def __init__(self, team):
        super().__init__(team)

    valid_action = ['attack', 'reinforce', 'rally', 'scout', 'speedup', 'teleport', 'recall_march', 'recall_occupied', 'join_rally', 'cancel_rally']

    # 离主塔最近的点
    nearest_list = [(5, 6), (7, 6), (6, 5), (6, 7), (5, 5), (5, 7), (7, 5), (7, 7), (4, 6), (8, 6), (6, 4), (6, 8)]
    nearest_set = set(((5, 6), (7, 6), (6, 5), (6, 7), (5, 5), (5, 7), (7, 5), (7, 7), (4, 6), (8, 6), (6, 4), (6, 8)))

    # 行军数量是否满
    def is_march_num_full(self, hive):
        return hive.get_using_march_num() == hive.get_max_march_num()

    def is_teleport_left(self, hive):
        return hive.get_teleport_times() > 0

    def get_empty_cord(self, width, height, self_hives: List[Hive], opp_hives: List[Hive], towers: List[Tower]):
        empty_cord = set([(w, h) for w in range(width) for h in range(height)])
        empty_cord -= set([hive.get_cord() for hive in self_hives])
        empty_cord -= set([hive.get_cord() for hive in opp_hives])
        empty_cord -= set([tower.get_cord() for tower in towers])
        return empty_cord

    def generate_action(self, state, score, detail: BattleField):
        action_list = []
        tower = detail.get_towers()
        opp_hives = detail.get_opp_hives()
        empty_cord = self.get_empty_cord(detail.get_width(), detail.get_height(), detail.get_self_hives(), detail.get_opp_hives(), detail.get_towers())

        i = 0
        for hive in detail.get_self_hives():
            if self.is_march_num_full(hive):
                continue
            if hive.get_troops_num() == 0:
                continue
            # 不在最近的范围内且能移， 尝试往主塔移
            if hive.get_cord() not in self.nearest_set and hive.get_teleport_times() > 0:
                while i < len(self.nearest_list):
                    if self.nearest_list[i] in empty_cord:
                        break
                    i += 1
                if i < len(self.nearest_list): # 迁移
                    action_list.append(
                        Teleport(
                            hive_id=hive.get_id(),
                            new_cord=self.nearest_list[i]
                        )
                    )
                    i += 1
                    continue

            # 往主塔派兵
            target = tower[0]
            action_list.append(
                Attack(
                    hive_id=hive.get_id(),
                    target_cord=target.get_cord(),
                    troops_num=min(hive.get_max_troops_num(), hive.get_troops_num()),
                    target_type=Attack.TARGET_TYPE_TOWER if type(target) == Tower else Attack.TARGET_TYPE_HIVE,
                    target_id=target.get_id()
                )
            )

        return ActionList(team=self._team, action_list=action_list)