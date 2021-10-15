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

class RandomAgent(Agent):

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
            random_action = random.choice(self.valid_action)
            if random_action == 'attack':
                if self.is_march_num_full(hive):
                    continue
                if hive.get_troops_num() == 0:
                    continue
                target = random.choice(tower + opp_hives)
                if type(target) == Tower and target.who_occupied() == self._team:
                    continue
                action_list.append(
                    Attack(
                        hive_id=hive.get_id(),
                        target_cord=target.get_cord(),
                        troops_num=random.randint(1, min(hive.get_max_troops_num(), hive.get_troops_num())),
                        target_type=Attack.TARGET_TYPE_TOWER if type(target) == Tower else Attack.TARGET_TYPE_HIVE,
                        target_id=target.get_id()
                    )
                )
            if random_action == 'reinforce':
                if self.is_march_num_full(hive):
                    continue
                if hive.get_troops_num() == 0:
                    continue
                target = random.choice(tower + detail.get_self_hives())
                if type(target) == Tower and target.who_occupied() != self._team:
                    continue
                action_list.append(
                    Reinforce(
                        hive_id=hive.get_id(),
                        target_id=target.get_id(),
                        target_type=Reinforce.TARGET_TYPE_TOWER if type(target) == Tower else Reinforce.TARGET_TYPE_HIVE,
                        troops_num=random.randint(1, min(hive.get_max_troops_num(), hive.get_troops_num()))
                    )
                )
            if random_action == 'rally':
                if self.is_march_num_full(hive):
                    continue
                if hive.get_troops_num() == 0:
                    continue
                target =random.choice(tower + detail.get_opp_hives())
                if type(target) == Tower and target.who_occupied() == self._team:
                    continue
                action_list.append(
                    Rally(
                        hive_id=hive.get_id(),
                        target_id=target.get_id(),
                        target_type=Rally.TARGET_TYPE_TOWER if type(target) == Tower else Rally.TARGET_TYPE_HIVE,
                        pending_times=30,
                        troops_num=random.randint(1, min(hive.get_max_troops_num(), hive.get_troops_num()))
                    )
                )
            if random_action == 'scout':
                if self.is_march_num_full(hive):
                    continue
                target = random.choice(tower + detail.get_opp_hives())
                if type(target) == Tower and target.who_occupied() is not None and target.who_occupied() != self._team:
                    continue
                action_list.append(
                    Scout(
                        hive_id=hive.get_id(),
                        target_id=target.get_id(),
                        target_type=Scout.TARGET_TYPE_TOWER if type(target) == Tower else Scout.TARGET_TYPE_HIVE,
                    )
                )
            if random_action == 'speedup':
                if len(detail.get_self_marches()) == 0:
                    continue
                target = random.choice(detail.get_self_marches())
                if target.get_hive_id() != hive.get_id():
                    continue
                action_list.append(
                    SpeedUp(
                        hive_id = hive.get_id(),
                        march_id=target.get_march_id()
                    )
                )
            if random_action == 'teleport':
                if not self.is_teleport_left(hive):
                    continue
                target = random.choice(list(empty_cord))
                action_list.append(
                    Teleport(
                        hive_id=hive.get_id(),
                        new_cord=target
                    )
                )
            if random_action == 'recall_march':
                if len(detail.get_self_marches()) == 0:
                    continue
                target = random.choice(detail.get_self_marches())
                if target.get_hive_id() != hive.get_id():
                    continue
                action_list.append(
                    RecallMarch(
                        hive_id=hive.get_id(),
                        march_id=target.get_march_id()
                    )
                )

            if random_action == 'recall_occupied':
                target = random.choice(detail.get_towers() + detail.get_self_hives())
                if type(target) == Tower:
                    if (target.get_troops() is None) or (not target.get_troops().is_hive_in(hive_id=hive.get_id())):
                        continue
                if type(target) == Hive and not target.get_rein_troops().is_hive_in(hive_id=hive.get_id()):
                    continue
                action_list.append(RecallOccupied(
                    hive_id=hive.get_id(),
                    target_type=RecallOccupied.TARGET_TYPE_TOWER if type(target) == Tower else RecallOccupied.TARGET_TYPE_HIVE,
                    target_id=target.get_id()
                ))


            if random_action == 'join_rally':
                if self.is_march_num_full(hive):
                    continue
                if hive.get_troops_num() == 0:
                    continue
                if len(detail.get_self_rallies()) == 0:
                    continue
                target = random.choice(detail.get_self_rallies())
                if target.get_troops().is_hive_in(hive_id=hive.get_id()):
                    continue
                is_already_join = False
                for march in detail.get_self_marches():
                    if march.get_hive_id() == hive.get_id() and march.get_target_type() == March.TARGET_TYPE_RALLY and march.get_target_id() == target.get_id():
                        is_already_join = True
                if is_already_join:
                    continue
                action_list.append(JoinRally(
                    hive_id=hive.get_id(),
                    rally_id=target.get_id(),
                    troops_num=random.randint(1, min(hive.get_max_troops_num(), hive.get_troops_num()))
                ))

            if random_action == 'cancel_rally':
                if len(detail.get_self_rallies()) == 0:
                    continue
                target = random.choice(detail.get_self_rallies())
                if target.get_hive_id() != hive.get_id():
                    continue
                action_list.append(RallyCancel(
                    hive_id=hive.get_id(),
                    rally_id=target.get_id()
                ))

        return ActionList(team=self._team, action_list=action_list)


