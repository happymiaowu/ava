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
            if hive.get_troops_num() == 0:
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
            if hive.get_troops_num() == 0:
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

# 城池循环移动到最靠近主塔的位置
class TowerRushMoreRangeAgent(Agent):
    def __init__(self, team):
        super().__init__(team)

    valid_action = ['attack', 'reinforce', 'rally', 'scout', 'speedup', 'teleport', 'recall_march', 'recall_occupied', 'join_rally', 'cancel_rally']
    now_index = 0

    # 离主塔最近的点
    nearest_list = [(5, 6), (7, 6), (6, 5), (6, 7), (5, 5), (5, 7), (7, 5), (7, 7), (4, 6), (8, 6), (6, 4), (6, 8), (5, 4), (5, 6), (7, 4), (7, 6), (4, 5), (4, 7), (6, 5), (6, 7)]
    nearest_set = set(((5, 6), (7, 6), (6, 5), (6, 7), (5, 5), (5, 7), (7, 5), (7, 7), (4, 6), (8, 6), (6, 4), (6, 8), (5, 4), (5, 6), (7, 4), (7, 6), (4, 5), (4, 7), (6, 5), (6, 7)))

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

        for hive in detail.get_self_hives():
            if self.is_march_num_full(hive):
                continue
            if hive.get_troops_num() == 0:
                continue
            # 不在最近的范围内且能移， 尝试往主塔移
            if hive.get_cord() not in self.nearest_set and hive.get_teleport_times() > 0:
                while True:
                    if self.nearest_list[self.now_index] in empty_cord:
                        break
                    self.now_index = (self.now_index + 1) % len(self.nearest_list)
                # 迁移
                action_list.append(
                    Teleport(
                        hive_id=hive.get_id(),
                        new_cord=self.nearest_list[self.now_index]
                    )
                )
                self.now_index = (self.now_index + 1) % len(self.nearest_list)
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

# 城池循环移动到最靠近主塔的位置，然后按比例分兵占领多个塔
class TowerRushMoreRangeWeightAgent(Agent):
    def __init__(self, team):
        super().__init__(team)

    valid_action = ['attack', 'reinforce', 'rally', 'scout', 'speedup', 'teleport', 'recall_march', 'recall_occupied', 'join_rally', 'cancel_rally']
    now_index = 0

    # 离主塔最近的点
    nearest_list = [(5, 6), (7, 6), (6, 5), (6, 7), (5, 5), (5, 7), (7, 5), (7, 7), (4, 6), (8, 6), (6, 4), (6, 8), (5, 4), (5, 8), (7, 4), (7, 8), (4, 5), (4, 7), (8, 5), (8, 7)]
    nearest_set = set(((5, 6), (7, 6), (6, 5), (6, 7), (5, 5), (5, 7), (7, 5), (7, 7), (4, 6), (8, 6), (6, 4), (6, 8), (5, 4), (5, 8), (7, 4), (7, 8), (4, 5), (4, 7), (8, 5), (8, 7)))

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

        random_tower_list = []
        for tower_item in tower:
            for i in range(0, int(tower_item.get_score_per_round())):
                random_tower_list.append(tower_item)

        opp_hives = detail.get_opp_hives()
        empty_cord = self.get_empty_cord(detail.get_width(), detail.get_height(), detail.get_self_hives(), detail.get_opp_hives(), detail.get_towers())

        for hive in detail.get_self_hives():
            if self.is_march_num_full(hive):
                continue
            if hive.get_troops_num() == 0:
                continue
            # 不在最近的范围内且能移， 尝试往主塔移
            if hive.get_cord() not in self.nearest_set and hive.get_teleport_times() > 0:
                while True:
                    if self.nearest_list[self.now_index] in empty_cord:
                        break
                    self.now_index = (self.now_index + 1) % len(self.nearest_list)
                # 迁移
                action_list.append(
                    Teleport(
                        hive_id=hive.get_id(),
                        new_cord=self.nearest_list[self.now_index]
                    )
                )
                self.now_index = (self.now_index + 1) % len(self.nearest_list)
                continue

            # 派兵
            target = random.choice(random_tower_list)
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

'''
使用以下策略
1. 城池循环移动到最靠近主塔的位置, 然后按比例分兵占塔
2. 有队伍在路上时，令其加速跑
3. (可能违反规则，可以不用)buff高的先动
'''
class TowerRushOptimalAgent(Agent):
    def __init__(self, team):
        super().__init__(team)

    valid_action = ['attack', 'reinforce', 'rally', 'scout', 'speedup', 'teleport', 'recall_march', 'recall_occupied', 'join_rally', 'cancel_rally']
    now_index = 0
    has_laugh = False

    # 离主塔最近的点
    nearest_list = [(5, 6), (7, 6), (6, 5), (6, 7), (5, 5), (5, 7), (7, 5), (7, 7), (4, 6), (8, 6), (6, 4), (6, 8), (5, 4), (5, 8), (7, 4), (7, 8), (4, 5), (4, 7), (8, 5), (8, 7)]
    nearest_set = set(((5, 6), (7, 6), (6, 5), (6, 7), (5, 5), (5, 7), (7, 5), (7, 7), (4, 6), (8, 6), (6, 4), (6, 8), (5, 4), (5, 8), (7, 4), (7, 8), (4, 5), (4, 7), (8, 5), (8, 7)))

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

    def laugh_action(self, state, score, detail: BattleField):
        action_list = []
        if self.has_laugh:
            return ActionList(team=self._team, action_list=action_list)
        
        my_hives = detail.get_self_hives()
        can_lauth = True

        
        # 必须都剩名额
        for hive in my_hives:
            if hive.get_teleport_times() == 0:
                can_lauth = False
                break
        
        if not can_lauth:
            return ActionList(team=self._team, action_list=action_list)

        # 必须点为空
        # laugh_points = [(8, 1), (9, 0), (10, 1), (6, 3), (7, 4), (8, 3), (10, 3), (11, 4), (12, 3)]
        laugh_points = [(9, 1), (10, 0), (11, 1), (12, 2), (11, 3), (10, 2), (9, 3), (8, 2), (0, 12)]
        empty_cord = self.get_empty_cord(detail.get_width(), detail.get_height(), detail.get_self_hives(), detail.get_opp_hives(), detail.get_towers())
        for laugh_point in laugh_points:
            if laugh_point not in empty_cord:
                can_lauth = False
                break
        
        if not can_lauth:
            return ActionList(team=self._team, action_list=action_list)

        self.has_laugh = True

        
        i = 0
        for hive in my_hives:
            action_list.append(
                Teleport(
                    hive_id=hive.get_id(),
                    new_cord=laugh_points[i]
                )
            )
            i += 1

        return ActionList(team=self._team, action_list=action_list)

    def generate_action(self, state, score, detail: BattleField):
        action_list = []
        tower = detail.get_towers()

        random_tower_list = []
        for tower_item in tower:
            for i in range(0, int(tower_item.get_score_per_round())):
                random_tower_list.append(tower_item)

        opp_hives = detail.get_opp_hives()
        empty_cord = self.get_empty_cord(detail.get_width(), detail.get_height(), detail.get_self_hives(), detail.get_opp_hives(), detail.get_towers())

        my_hives = detail.get_self_hives()
        my_hives = sorted(my_hives, key=lambda s: s.get_buff(), reverse=True)

        # 已经赢了，开嘲讽
        round_total_scores = 0
        for tower_item in tower:
            round_total_scores += tower_item.get_score_per_round()

        if detail.get_score()[detail._team] - detail.get_score()[detail._other_team] > round_total_scores * detail.get_round_left():
            return self.laugh_action(state, score, detail)

        my_marches = detail.get_self_marches()
        for hive in my_hives:
            if self.is_march_num_full(hive) or hive.get_troops_num() == 0: # 没有移动的了
                # 看有没有自己的军队在路上，有则加速
                for march in my_marches:
                    if march.get_hive_id() == hive.get_id():
                        action_list.append(
                            SpeedUp(
                                hive_id = hive.get_id(),
                                march_id=march.get_march_id()
                            )
                        )
                        break
                continue
            # 不在最近的范围内且能移， 尝试往主塔移
            if hive.get_cord() not in self.nearest_set and hive.get_teleport_times() > 0:
                while True:
                    if self.nearest_list[self.now_index] in empty_cord:
                        break
                    self.now_index = (self.now_index + 1) % len(self.nearest_list)
                # 迁移
                action_list.append(
                    Teleport(
                        hive_id=hive.get_id(),
                        new_cord=self.nearest_list[self.now_index]
                    )
                )
                self.now_index = (self.now_index + 1) % len(self.nearest_list)
                continue

            # 派兵
            target = random.choice(random_tower_list)
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