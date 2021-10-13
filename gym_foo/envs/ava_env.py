import gym
from gym import spaces
import numpy as np
import random
from gym.envs.classic_control import rendering
import uuid
from gym_foo.model.tower import Tower
from gym_foo.model.hive import Hive
from gym_foo.model.march import March
from gym_foo.model.action.recall_march import RecallMarch
from gym_foo.model.action.recall_occupied import RecallOccupied
from gym_foo.model.action.attack import Attack
from gym_foo.model.battle_field_total import BattleFieldTotal
from gym_foo.model.single_march import SingleMarch
from gym_foo.model.action.teleport import Teleport
from gym_foo.model.troops import Troops
from gym_foo.model.troops_list import TroopsList
from gym_foo.model.action.speedup import SpeedUp
from gym_foo.model.action.rally import Rally
from gym_foo.model.common import battle
from gym_foo.model.common import common
from gym_foo.model.action_list import ActionList
from typing import List, Dict, Tuple
from gym_foo.model.action.scout import Scout
from gym_foo.model.action.reinforce import Reinforce
from gym_foo.model.rally_waiting import RallyWaiting
from gym_foo.model.action.rally_cancel import RallyCancel
import pyglet

class DrawText:
    def __init__(self, label:pyglet.text.Label):
        self.label=label
    def render(self):
        self.label.draw()


class AvaEnv(gym.Env):
    metadata = {
        'render.modes': ['human', 'rgb_array'],
        'video.frames_per_second': 1
    }

    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 800

    GRID_WIDTH = 50

    TEAM_0_COLOR = (0,1,0)
    TEAM_1_COLOR = (0,0,1)
    TOWER_COLOR = (1, 0.9, 0)

    def __init__(self):

        self.map =    [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                       [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                       [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                       [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                       [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 1],
                       [1, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                       [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                       [1, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 1],
                       [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                       [1, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 1],
                       [1, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                       [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                       [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                       [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                       [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

        # 队员个数
        self.members_num = [9, 9]

        # 地图大小
        self.map_width = 13
        self.map_height = 13

        # 队员生成
        self.hives = [[], []]
        cnt = 0
        for i in range(self.members_num[0]):
            self.hives[0].append(Hive(id='0_%d' % i, team=0, cord=(cnt // 3, cnt % 3)))
            cnt += 1
        cnt = 0
        for i in range(self.members_num[1]):
            self.hives[1].append(Hive(id='1_%d' % i, team=1, cord=((self.map_height - 1) - cnt // 3, (self.map_height - 1) - cnt % 3)))
            cnt += 1

        ### 王座 & 塔
        self.tower = []
        # 王座坐标
        self.wonder_cord = [(6, 6)]

        # 王座生成
        for cord in self.wonder_cord:
            self.tower.append(Tower(tower_id=str(len(self.tower)), score=30, cord=cord, is_wonder=True))

        # 塔坐标
        self.tower_cord = [(4, 4), (8, 8)]
        # 塔生成
        for cord in self.tower_cord:
            self.tower.append(Tower(tower_id=str(len(self.tower)), score=10, cord=cord, is_wonder=False))

        self.zombie_cord = [(1, 1), (11, 11)]

        # 行军
        self.march = []

        # 集结
        self.rally = []

        # round
        self.round_left = 100

        # 得分
        self.score = [0, 0]

        # 侦查报告
        self.scout_reports = []

        # 战斗报告
        self.battle_reports = []

        self.viewer = None

        self.logs = open('logs/log_%s.log' % (uuid.uuid4().hex), 'w')

    def __del__(self):
        self.logs.close()

    def grid2cord(self, x, y):
        return self.GRID_WIDTH * (x + 1), self.GRID_WIDTH * (y + 1)

    def get_hive_dict(self):
        hive_dict = {}
        for team_hive in self.hives:
            for hive in team_hive:
                hive_dict[hive.get_id()] = hive
        return hive_dict

    def get_rally_dict(self):
        rally_dict = {}
        for rally in self.rally:
            rally_dict[rally.get_id()] = rally
        return rally_dict

    def get_empty_cord(self):
        empty_cord = set([(w, h) for w in range(self.map_width) for h in range(self.map_height)])
        empty_cord -= set([hive.get_cord() for hive in self.get_hive_dict().values()])
        empty_cord -= set([tower.get_cord() for tower in self.tower])
        return list(empty_cord)

    def initial_state(self):
        return self.map, \
               0, \
               False, \
               BattleFieldTotal(
                   width=self.map_width,
                   height=self.map_height,
                   marches=self.march,
                   towers=self.tower,
                   hives=self.hives,
                   round_left=self.round_left,
                   scout_reports=self.scout_reports,
                   battle_reports=self.battle_reports,
                   rallies=self.rally,
                   score=self.score
               )

    def teleport_recall(self, hive_id):
        marches = []
        hive = self.get_hive_dict()[hive_id]
        # 召回行军
        for march in self.march:
            if march.get_hive_id() == hive_id:
                hive.recall_suddenly(troops_num=march.get_troops_num())
                continue
            marches.append(march)
        self.march = marches
        # 召回占领
        for tower in self.tower:
            tower.kick_march(hive=self.get_hive_dict()[hive_id])
        # 召回集结
        rallies = []
        for rally in self.rally:
            if rally.get_hive_id() == hive_id:
                rally.cancel(hive_dict=self.get_hive_dict())
                continue
            if rally.get_troops().is_hive_in(hive_id=hive_id):
                rm_troops = rally.get_troops().remove_troops(hive_id=hive_id)
                hive.recall_suddenly(rm_troops.get_troops_num())
                rallies.append(rally)
                continue
            rallies.append(rally)
        self.rally = rallies

    def step(self, action_lists: List[ActionList]):
        self.logs.write('Round: %s\n' % str(self.round_left))
        self.logs.write('Agent0 Action: %s\n' % str(action_lists[0]))
        self.logs.write('Agent1 Action: %s\n' % str(action_lists[1]))
        ### 行动
        # 召回行军

        for action_list in action_lists:
            for act in action_list.get_type2action()[RecallMarch]:
                for march in self.march:
                    if march.get_march_id() != act.get_march_id():
                        continue
                    act.do(march, hive=self.get_hive_dict()[march.get_hive_id()])
                    self.logs.write('March %s recall\n' % march.get_march_id())

        # 召回驻军
        for action_list in action_lists:
            for act in action_list.get_type2action()[RecallOccupied]:
                if act.get_target_type() == RecallOccupied.TARGET_TYPE_HIVE:
                    march = act.do(hive=self.get_hive_dict()[act.get_hive_id()], occupied_hive=self.get_hive_dict()[act.get_target_id()])
                    self.march.append(march)
                    self.logs.write('Hive %s reinforce hive %s recall, march: %s\n' % (act.get_hive_id(), act.get_target_id(), march))
                elif act.get_target_type() == RecallOccupied.TARGET_TYPE_TOWER:
                    march = act.do(hive=self.get_hive_dict()[act.get_hive_id()], occupied_tower=self.tower[int(act.get_target_id())])
                    self.march.append(march)
                    self.logs.write('Hive %s reinforce tower %s recall, march: %s\n' % (act.get_hive_id(), act.get_target_id(), march))

        ### 结算这一秒情况
        # 评分
        for tower in self.tower:
            occupied_team = tower.who_occupied()
            if occupied_team is None:
                self.logs.write('Tower %s no occupied.\n' % tower.get_id())
                continue
            self.score[occupied_team] += tower.get_score_per_round()
            self.logs.write('Tower %s occupied by team %s, score increase %s\n' % (str(tower.get_id()), str(occupied_team), str(tower.get_score_per_round())))

        # 加速
        for action_list in action_lists:
            for act in action_list.get_type2action()[SpeedUp]:
                for march in self.march:
                    if march.get_march_id() != act.get_march_id():
                        continue
                    act.do(march)
                    self.logs.write('March %s speedup, speed now: %s\n' % (march.get_march_id(), march.get_speed()))

        # 开始行军
        # 进攻
        for action_list in action_lists:
            for act in action_list.get_type2action()[Attack]:
                hive_id = act.get_hive_id()
                team, index = hive_id.split('_')
                attack_march = act.do(self.hives[int(team)][int(index)])
                self.march.append(attack_march)
                self.logs.write('Hive %s attacking, target type: %s, id: %s, march: %s.\n' % (hive_id, act.get_target_type(), act.get_target_id(), attack_march))

        # 支援
        for action_list in action_lists:
            for act in action_list.get_type2action()[Reinforce]:
                hive_id = act.get_hive_id()
                target_id = act.get_target_id()
                if act.get_target_type() == Reinforce.TARGET_TYPE_HIVE:
                    rein_march = act.do(start_hive=self.get_hive_dict()[hive_id], target_hive=self.get_hive_dict()[target_id])
                    self.march.append(rein_march)
                    self.logs.write('Hive %s reinforce hive %s, march: %s\n' % (hive_id, target_id, rein_march))
                else:
                    rein_march = act.do(start_hive=self.get_hive_dict()[hive_id], target_tower=self.tower[int(target_id)])
                    self.march.append(rein_march)
                    self.logs.write('Hive %s reinforce tower %s, march: %s\n' % (hive_id, target_id, rein_march))


        # 发起集结
        for action_list in action_lists:
            for act in action_list.get_type2action()[Rally]:
                hive_id = act.get_hive_id()
                rally = act.do(hive=self.get_hive_dict()[hive_id])
                self.rally.append(rally)
                self.logs.write('Hive %s rally for target type: %s, target id: %s, rally: %s\n' % (hive_id, act.get_target_type(), act.get_target_id(), rally))

        # 取消集结
        for action_list in action_lists:
            for act in action_list.get_type2action()[RallyCancel]:
                rally = self.get_rally_dict()[act.get_rally_id()]
                marches = act.do(rally, self.get_hive_dict())
                self.march.extend(marches)
                self.logs.write('Rally %s cancelled, marches back: %s\n' % (act.get_rally_id(), marches))

        # 侦查
        for action_list in action_lists:
            for act in action_list.get_type2action()[Scout]:
                hive_id = act.get_hive_id()
                target_type = act.get_target_type()
                target_id = act.get_target_id()
                if target_type == Scout.TARGET_TYPE_HIVE:
                    self.get_hive_dict()[hive_id].attack(0)
                    march = act.do(scout_hive=self.get_hive_dict()[hive_id], target_hive=self.get_hive_dict()[target_id])
                    self.march.append(march)
                    self.logs.write('Hive %s scout hive %s, march: %s\n' % (hive_id, target_id, march))
                elif target_type == Scout.TARGET_TYPE_TOWER:
                    self.get_hive_dict()[hive_id].attack(0)
                    march = act.do(scout_hive=self.get_hive_dict()[hive_id], target_tower=self.tower[int(target_id)])
                    self.march.append(march)
                    self.logs.write('Hive %s scout tower %s, march: %s\n' % (hive_id, target_id, march))


        # 传送
        for action_list in action_lists:
            for act in action_list.get_type2action()[Teleport]:
                hive_id = act.get_hive_id()
                start_cord = self.get_hive_dict()[hive_id].get_cord()
                try:
                    act.do(self.get_hive_dict()[hive_id], self.get_empty_cord())
                    self.teleport_recall(hive_id=hive_id)
                    self.logs.write('Hive %s teleport from %s to %s.\n' % (hive_id, start_cord, act.get_new_cord()))
                except Exception:
                    pass


        # 行军
        for march in self.march:
            march.next_round()
            self.logs.write('March %s move to %s\n' % (march.get_march_id(), march.get_now_cord()))

        # 集结
        new_rally = []
        for rally in self.rally:
            march = rally.next_round(
                start_hive=self.get_hive_dict()[rally.get_hive_id()],
                target_hive=None if rally.get_target_type() == RallyWaiting.TARGET_TYPE_TOWER else self.get_hive_dict()[rally.get_target_id()],
                target_tower=None if rally.get_target_type() == RallyWaiting.TARGET_TYPE_HIVE else self.tower[int(rally.get_target_id())]
            )
            if march is not None:
                self.march.append(march)
                self.logs.write('Rally %s march start, march: %s\n' %(rally.get_id(), march))
            elif rally.get_pending_times() > 0:
                self.logs.write('Rally %s timing down to %s\n' % (rally.get_id(), rally.get_pending_times()))
                new_rally.append(rally)
            else:
                self.logs.write('Rally %s nobody join, cancelled.\n' % (rally.get_id()) )
        self.rally = new_rally

        # 塔冷却
        for hives in self.hives:
            for hive in hives:
                hive.next_round()

        # 行军结算
        new_march_list = []
        self.march = sorted(self.march, key=lambda x: x.get_type())
        lose_hive_id = []
        for march in self.march:
            # 还未走到
            if march.get_target_cord() != march.get_now_cord():
                new_march_list.append(march)
                continue
            is_deal = False
            # 战斗地方为塔
            target_type, target_id = march.get_target_detail()
            if target_type == March.TARGET_TYPE_TOWER:
                if march.get_type() == March.TYPE_ATTACK:
                    is_deal = True
                    tower = self.tower[int(target_id)]
                    _march, _report = battle.occupied_tower(tower, march, self.get_hive_dict())
                    new_march_list.extend(_march)
                    if _report is not None:
                        self.battle_reports.append(_report)
                        self.logs.write('Battle in tower %s, march: %s, report: %s\n' % (target_id, march, _report))
                    else:
                        self.logs.write('Battle in tower %s, march: %s, no happened\n' % (target_id, march))

                if march.get_type() == March.TYPE_SCOUT:
                    is_deal = True
                    tower = self.tower[int(target_id)]
                    if tower.who_occupied() == None or tower.who_occupied() == int(march.get_hive_id().split('_')[0]):
                        self.logs.write('March %s scout to tower %s. failed because it not opp occupied.' % (march, target_id))
                        continue
                    report = tower.generate_scout_report(scout_hive_id=march.get_hive_id(), round=self.round_left)
                    self.scout_reports.append(report)
                    self.logs.write('March %s scout tower %s finished, scout report: %s.\n' % (march, tower.get_id(), report))
            # 战斗地方为城堡
            if target_type == March.TARGET_TYPE_HIVE:
                hive = self.get_hive_dict()[target_id]
                # 类型为进攻
                if march.get_type() == March.TYPE_ATTACK and hive.get_cord() == march.get_target_cord():
                    is_deal = True
                    lose_marches, report = battle.attack_hive(hive, march, self.get_hive_dict())
                    self.battle_reports.append(report)
                    self.logs.write('Battle in hive %s, march: %s, report: %s\n' % (target_id, march, report))
                    if not report.is_attack_win():
                        new_march_list.extend(lose_marches)
                    else:
                        # 直接回家
                        for m in lose_marches:
                            self.get_hive_dict()[m.get_hive_id()].recall_suddenly(m.get_troops_num())
                        lose_hive_id.append(hive.get_id())

                # 类型为回城
                if march.get_type() == March.TYPE_BACK and march.get_hive_id() == hive.get_id():
                    self.get_hive_dict()[march.get_hive_id()].recall_suddenly(march.get_troops_num())
                    self.logs.write('March %s back to hive.\n' % (march))
                    is_deal = True

                # 加入集结成功
                if march.get_type() == March.TYPE_JOIN_RALLY and hive.get_cord() == march.get_target_cord():
                    # 车不见了
                    if march.get_target_id() not in self.get_rally_dict():
                        self.logs.write('March %s join rally %s failed cause rally is disappear.\n' % (march, march.get_target_id()))
                        continue
                    self.get_rally_dict()[march.get_target_id()].join(hive_id=march.get_hive_id(), troops_num=march.get_troops_num())
                    self.logs.write('March %s join rally %s .\n' % (march, march.get_target_id()))
                    is_deal = True

                # 增援城堡成功
                if march.get_type() == March.TYPE_REINFORCE and hive.get_cord() == march.get_target_cord():
                    hive.add_rein_troops(march)
                    self.logs.write('March %s reinforce hive %s.\n' % (march, march.get_target_id()))
                    is_deal = True

                # 侦查
                if march.get_type() == March.TYPE_SCOUT and hive.get_cord() == march.get_target_cord():
                    report = hive.generate_scout_report(march.get_hive_id(), round=self.round_left)
                    self.scout_reports.append(report)
                    self.logs.write('March %s scout hive %s finished, scout report: %s.\n' % (march, march.get_target_id(), report))
                    new_march_list.append(SingleMarch(
                        start_cord=march.get_target_cord(),
                        target_cord=self.get_hive_dict()[march.get_hive_id()].get_cord(),
                        hive_id=march.get_hive_id(),
                        type=March.TYPE_BACK,
                        troops_num=march.get_troops_num(),
                        target_type=March.TARGET_TYPE_HIVE,
                        target_id=march.get_hive_id(),
                        is_scout_back=True
                    ))
                    is_deal = True


            # 行军发现目标已消失
            if not is_deal:
                print('target is disappear')
                hive = self.get_hive_dict()[march.get_hive_id()]
                new_march_list.append(SingleMarch(
                    start_cord=march.get_target_cord(),
                    target_cord=hive.get_cord(),
                    hive_id=march.get_hive_id(),
                    type=March.TYPE_BACK,
                    troops_num=march.get_troops_num(),
                    target_type=March.TARGET_TYPE_HIVE,
                    target_id=march.get_hive_id()
                ))

        self.march = new_march_list

        # 被打的堡随机传送
        for hive_id in lose_hive_id:
            self.get_hive_dict()[hive_id].random_teleport(self.get_empty_cord())
            self.teleport_recall(hive_id=hive_id)


        print(self.round_left)
        if self.round_left == 0:
            return self.map, 0, True, BattleFieldTotal(
                width=self.map_width,
                height=self.map_height,
                marches=self.march,
                towers=self.tower,
                hives=self.hives,
                round_left=self.round_left,
                scout_reports=self.scout_reports,
                battle_reports=self.battle_reports,
                rallies=self.rally,
                score=self.score
            )

        self.round_left -= 1

        return self.map, \
               0, \
               False, \
               BattleFieldTotal(
                   width=self.map_width,
                   height=self.map_height,
                   marches=self.march,
                   towers=self.tower,
                   hives=self.hives,
                   round_left=self.round_left,
                   scout_reports=self.scout_reports,
                   battle_reports=self.battle_reports,
                   rallies=self.rally,
                   score=self.score
               )


    def reset(self):
        print('reset')
        return self.map

    def render(self, mode='human', close=False):
        if close:
            if self.viewer is not None:
                self.viewer.close()
                self.viewer = None
            return


        if self.viewer is None:
            self.viewer = rendering.Viewer(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
            # 创建网格世界
            self.lines = []
            for x in range(1, 14):
                self.lines.append(rendering.Line((self.GRID_WIDTH, self.GRID_WIDTH * x), (self.GRID_WIDTH * 13, self.GRID_WIDTH * x)))
                self.lines.append(rendering.Line((self.GRID_WIDTH * x, self.GRID_WIDTH), (self.GRID_WIDTH * x, self.GRID_WIDTH * 13)))

            for line in self.lines:
                line.set_color(0, 0, 0)
                self.viewer.add_geom(line)

            # 建塔
            self.tower_view = []
            for tower in self.tower:
                tmp_view = rendering.make_circle(self.GRID_WIDTH / 2. if tower.is_wonder() else self.GRID_WIDTH / 3.)

                tmp_view.add_attr(rendering.Transform(translation=(self.grid2cord(*tower.get_cord()))))
                tmp_view.set_color(*self.TOWER_COLOR)
                self.tower_view.append(tmp_view)

            # 建城堡
            self.hive_view = []
            self.hive_trans = []
            for hives in self.hives:
                tmp_view_list = []
                tmp_trans_list = []
                for hive in hives:
                    tmp_view = rendering.make_circle(self.GRID_WIDTH / 4.)
                    tmp_trans = rendering.Transform(translation=(self.grid2cord(*hive.get_cord())))
                    tmp_view.add_attr(tmp_trans)
                    if hive.get_id().split('_')[0] == '0':
                        tmp_view.set_color(*self.TEAM_0_COLOR)
                    else:
                        tmp_view.set_color(*self.TEAM_1_COLOR)
                    tmp_view_list.append(tmp_view)
                    tmp_trans_list.append(tmp_trans)
                self.hive_view.append(tmp_view_list)
                self.hive_trans.append(tmp_trans_list)

            for view in self.tower_view:
                self.viewer.add_geom(view)

            for views in self.hive_view:
                for view in views:
                    self.viewer.add_geom(view)

            self.score_labels_view = [
                pyglet.text.Label(
                    "team_0 score: 0000",
                    font_size=18,
                    anchor_x='left',
                    anchor_y='top',
                    x=30, y=750,
                    color=(0, 255, 0, 255)
                ), pyglet.text.Label(
                    "team_1 score: 0000",
                    font_size=18,
                    anchor_x='left',
                    anchor_y='top',
                    x=400, y=750,
                    color=(0, 0, 255, 255)
                )
            ]

            for view in self.score_labels_view:
                self.viewer.add_geom(DrawText(view))

        if self.map is None: return None

        for hive in self.get_hive_dict().values():
            team_id, hive_id = hive.get_id().split('_')
            self.hive_trans[int(team_id)][int(hive_id)].set_translation(*self.grid2cord(*hive.get_cord()))

        for team_id in range(2):
            self.score_labels_view[team_id].text = 'team_%d score: %04d' %(team_id, self.score[team_id])

        for tower in self.tower:
            if tower.who_occupied() is None:
                self.tower_view[int(tower.get_id())].set_color(*self.TOWER_COLOR)
            elif tower.who_occupied() == 0:
                self.tower_view[int(tower.get_id())].set_color(*self.TEAM_0_COLOR)
            else:
                self.tower_view[int(tower.get_id())].set_color(*self.TEAM_1_COLOR)

        # 军队
        for march in self.march:
            line_color = self.TEAM_0_COLOR if march.get_hive_id().split('_')[0] == '0' else self.TEAM_1_COLOR
            march_line = rendering.Line(
                self.grid2cord(*march.get_start_cord()), self.grid2cord(*march.get_target_cord())
            )
            march_line.set_color(*line_color)
            self.viewer.add_onetime(march_line)

            march_point = rendering.make_circle(self.GRID_WIDTH / 8.)
            march_point.add_attr(rendering.Transform(translation=(self.grid2cord(*march.get_now_cord()))))
            march_point.set_color(*line_color)
            self.viewer.add_onetime(march_point)

        return self.viewer.render(return_rgb_array=mode == 'rgb_array')
