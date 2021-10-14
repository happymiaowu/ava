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
from gym_foo.Utils import *
import pickle
import math
import os


class QLearnAgent_V2(Agent):

    def __init__(self, team: object, agent_model_path: object = None) -> object:
        super().__init__(team)
        self.qfunc = dict()
        self.valid_action = ['attack_wonder_full',
                             'attack_wonder_half',
                             'attack_tower_full',
                             'attack_tower_half',
                             'attack_hive_full',
                             'attack_hive_half',
                             'reinforce_tower_full',
                             'reinforce_tower_half',
                             'reinforce_hive',
                             'rally_tower_full',
                             'rally_tower_half',
                             'rally_hive_full',
                             'rally_hive_half',
                             'scout_tower',
                             'scout_hive',
                             'speedup',
                             'teleport_wonder_1',
                             'teleport_wonder_2',
                             'teleport_tower_1',
                             'teleport_tower_2',
                             'teleport_random',
                             'recall_march',
                             'recall_occupied',
                             'join_rally_full',
                             'join_rally_half',
                             'cancel_rally'
                             ]
        if agent_model_path:
            self.load_agent_model(agent_model_path)

    # 行军数量是否满
    def is_march_num_full(self, hive):
        return hive.get_using_march_num() == hive.get_max_march_num()

    def is_teleport_left(self, hive):
        return hive.get_teleport_times() > 0

    def get4place(self, cord):
        s = set()
        for x, y in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            s.add((cord[0] + x, cord[1] + y))
        return s

    def get_empty_cord(self, width, height, self_hives: List[Hive], opp_hives: List[Hive], towers: List[Tower]):
        empty_cord = set([(w, h) for w in range(width) for h in range(height)])
        empty_cord -= set([hive.get_cord() for hive in self_hives])
        empty_cord -= set([hive.get_cord() for hive in opp_hives])
        empty_cord -= set([tower.get_cord() for tower in towers])
        return empty_cord

    def greedy(self, state):
        amax = 0
        key = "%s_%s" % (state, self.valid_action[0])
        qmax = self.qfunc.get(key, 0.0)
        for i in range(len(self.valid_action)):  # 扫描动作空间得到最大动作值函数
            key = "%s_%s" % (state, self.valid_action[i])
            q = self.qfunc.get(key, 0.0)
            if qmax < q:
                qmax = q
                amax = i
        return self.valid_action[amax]

    def epsilon_greedy(self, state, epsilon):
        amax = 0
        key = "%s_%s" % (state, self.valid_action[0])
        qmax = self.qfunc.get(key, 0.0)
        for i in range(len(self.valid_action)):  # 扫描动作空间得到最大动作值函数
            key = "%s_%s" % (state, self.valid_action[i])
            q = self.qfunc.get(key, 0.0)
            if qmax < q:
                qmax = q
                amax = i
        # 概率部分
        pro = [0.0 for i in range(len(self.valid_action))]
        pro[amax] += 1 - epsilon
        for i in range(len(self.valid_action)):
            pro[i] += epsilon / len(self.valid_action)

        # #选择动作
        r = random.random()
        s = 0.0
        for i in range(len(self.valid_action)):
            s += pro[i]
            if s >= r: return self.valid_action[i]
        return self.valid_action[len(self.valid_action) - 1]

    def save_agent_model(self, agent_model_path):
        sss = os.path.dirname(agent_model_path)
        if not os.path.exists(sss):
            os.makedirs(sss)
        with open(agent_model_path, "wb") as wf:
            pickle.dump(self.qfunc, wf)

    def load_agent_model(self, agent_model_path):
        with open(agent_model_path, "rb") as rf:
            self.qfunc = pickle.load(rf)
        print(self.qfunc)

    def generate_action(self, state, score, detail: BattleField):
        action_list = []
        tower = detail.get_towers()
        opp_hives = detail.get_opp_hives()
        empty_cord = self.get_empty_cord(detail.get_width(), detail.get_height(), detail.get_self_hives(), detail.get_opp_hives(), detail.get_towers())

        for hive in detail.get_self_hives():

            # random_action = random.choice(self.valid_action)
            r, s = get_status_rewards_from_detail_v2(detail, hive)
            random_action = self.epsilon_greedy(s, 0.2)
            if random_action.startswith('attack_wonder'):
                if self.is_march_num_full(hive):
                    continue
                if hive.get_troops_num() == 0:
                    continue
                target = random.choice(list(filter(lambda x: x.is_wonder(), detail.get_towers())))
                if type(target) == Tower and target.who_occupied() == self._team:
                    continue
                action_list.append(
                    Attack(
                        hive_id=hive.get_id(),
                        target_cord=target.get_cord(),
                        troops_num=min(hive.get_max_troops_num(), hive.get_troops_num()) if random_action.endswith('full') else math.ceil(min(hive.get_max_troops_num(), hive.get_troops_num()) / 2),
                        target_type=Attack.TARGET_TYPE_TOWER,
                        target_id=target.get_id()
                    )
                )

            if random_action.startswith('attack_tower'):
                if self.is_march_num_full(hive):
                    continue
                if hive.get_troops_num() == 0:
                    continue
                target = random.choice(list(filter(lambda x: not x.is_wonder(), detail.get_towers())))
                if type(target) == Tower and target.who_occupied() == self._team:
                    continue
                action_list.append(
                    Attack(
                        hive_id=hive.get_id(),
                        target_cord=target.get_cord(),
                        troops_num=min(hive.get_max_troops_num(), hive.get_troops_num()) if random_action.endswith('full') else math.ceil(min(hive.get_max_troops_num(), hive.get_troops_num()) / 2),
                        target_type=Attack.TARGET_TYPE_TOWER,
                        target_id=target.get_id()
                    )
                )

            if random_action.startswith('attack_hive'):
                if self.is_march_num_full(hive):
                    continue
                if hive.get_troops_num() == 0:
                    continue
                target = random.choice(opp_hives)
                action_list.append(
                    Attack(
                        hive_id=hive.get_id(),
                        target_cord=target.get_cord(),
                        troops_num=min(hive.get_max_troops_num(), hive.get_troops_num()) if random_action.endswith('full') else math.ceil(min(hive.get_max_troops_num(), hive.get_troops_num()) / 2),
                        target_type=Attack.TARGET_TYPE_HIVE,
                        target_id=target.get_id()
                    )
                )
            if random_action.startswith('reinforce_tower'):
                if self.is_march_num_full(hive):
                    continue
                if hive.get_troops_num() == 0:
                    continue
                target = random.choice(tower)
                if type(target) == Tower and target.who_occupied() != self._team:
                    continue
                action_list.append(
                    Reinforce(
                        hive_id=hive.get_id(),
                        target_id=target.get_id(),
                        target_type=Reinforce.TARGET_TYPE_TOWER,
                        troops_num=min(hive.get_max_troops_num(), hive.get_troops_num()) if random_action.endswith('full') else math.ceil(min(hive.get_max_troops_num(), hive.get_troops_num()) / 2)
                    )
                )

            if random_action == 'reinforce_hive':
                if self.is_march_num_full(hive):
                    continue
                if hive.get_troops_num() == 0:
                    continue
                target = random.choice(detail.get_self_hives())
                action_list.append(
                    Reinforce(
                        hive_id=hive.get_id(),
                        target_id=target.get_id(),
                        target_type=Reinforce.TARGET_TYPE_HIVE,
                        troops_num=random.randint(1, min(hive.get_max_troops_num(), hive.get_troops_num()))
                    )
                )

            if random_action.startswith('rally_tower'):
                if self.is_march_num_full(hive):
                    continue
                if hive.get_troops_num() == 0:
                    continue
                target =random.choice(tower)
                action_list.append(
                    Rally(
                        hive_id=hive.get_id(),
                        target_id=target.get_id(),
                        target_type=Rally.TARGET_TYPE_TOWER,
                        pending_times=10,
                        troops_num=min(hive.get_max_troops_num(), hive.get_troops_num()) if random_action.endswith('full') else math.ceil(min(hive.get_max_troops_num(), hive.get_troops_num()) / 2)
                    )
                )
            if random_action.startswith('rally_hive'):
                if self.is_march_num_full(hive):
                    continue
                if hive.get_troops_num() == 0:
                    continue
                target =random.choice(detail.get_opp_hives())
                action_list.append(
                    Rally(
                        hive_id=hive.get_id(),
                        target_id=target.get_id(),
                        target_type=Rally.TARGET_TYPE_HIVE,
                        pending_times=10,
                        troops_num=min(hive.get_max_troops_num(), hive.get_troops_num()) if random_action.endswith('full') else math.ceil(min(hive.get_max_troops_num(), hive.get_troops_num()) / 2)
                    )
                )

            if random_action == 'scout_tower':
                if self.is_march_num_full(hive):
                    continue
                target = random.choice(tower)
                if type(target) == Tower and target.who_occupied() is not None and target.who_occupied() != self._team:
                    continue
                action_list.append(
                    Scout(
                        hive_id=hive.get_id(),
                        target_id=target.get_id(),
                        target_type=Scout.TARGET_TYPE_TOWER,
                    )
                )

            if random_action == 'scout_hive':
                if self.is_march_num_full(hive):
                    continue
                target = random.choice(detail.get_opp_hives())
                action_list.append(
                    Scout(
                        hive_id=hive.get_id(),
                        target_id=target.get_id(),
                        target_type=Scout.TARGET_TYPE_HIVE,
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
            if random_action == 'teleport_wonder_1':
                if not self.is_teleport_left(hive):
                    continue
                wonder = list(filter(lambda x: x.is_wonder(), detail.get_towers()))
                valid_cord = set()
                for w in wonder:
                    valid_cord |= self.get4place(w.get_cord())
                if len(list(valid_cord & empty_cord)) == 0:
                    continue
                target = random.choice(list(valid_cord & empty_cord))
                action_list.append(
                    Teleport(
                        hive_id=hive.get_id(),
                        new_cord=target
                    )
                )
            if random_action == 'teleport_tower_1':
                if not self.is_teleport_left(hive):
                    continue
                towers = list(filter(lambda x: not x.is_wonder(), detail.get_towers()))
                valid_cord = set()
                for t in towers:
                    valid_cord |= self.get4place(t.get_cord())
                if len(list(valid_cord & empty_cord)) == 0:
                    continue
                target = random.choice(list(valid_cord & empty_cord))
                action_list.append(
                    Teleport(
                        hive_id=hive.get_id(),
                        new_cord=target
                    )
                )
            if random_action == 'teleport_random':
                if not self.is_teleport_left(hive):
                    continue
                if len(list(empty_cord)) == 0:
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


            if random_action.startswith('join_rally'):
                if self.is_march_num_full(hive):
                    continue
                if len(detail.get_self_rallies()) == 0:
                    continue
                if hive.get_troops_num() == 0:
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
                    troops_num=min(hive.get_max_troops_num(), hive.get_troops_num()) if random_action.endswith('full') else math.ceil(min(hive.get_max_troops_num(), hive.get_troops_num()) / 2)
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
            # print(hive.get_id(), random_action)
        return random_action, ActionList(team=self._team, action_list=action_list)


