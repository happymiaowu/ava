import sys
import gym
import time
from gym import wrappers
from gym_foo.agent.agent import Agent
from gym_foo.agent.random_agent import RandomAgent
from gym_foo.agent.q_learning_agent_v2 import QLearnAgent_V2
from gym_foo.agent.attack_agent import TowerRushAgent, AttackTowerAgent, AttackMainTowerAgent
from gym_foo.model.battlefield_detail import BattleField
from gym_foo.Utils import *
import random
import os


object_path = os.path.dirname(__file__)
alpha = 0.5
gamma = 0.9
agent_model_path = os.path.join(object_path, 'agent_model_v2/train_0/agent0.pkl')

if __name__ == "__main__":
    win = 0
    total = 0
    agent_0 = QLearnAgent_V2(team=0, agent_model_path=agent_model_path)
    for iter in range(500):
        grid = gym.make('ava-v1')
        # grid = wrappers.Monitor(grid, './videos', force=True)  # 记录回放动画
        grid.reset()
        # grid.render()
        is_start = True
        agent_1 = random.choice([TowerRushAgent(team=1), AttackTowerAgent(team=1), AttackMainTowerAgent(team=1)])
        while True:
            if is_start:
                state, score, is_terminate, detail = grid.initial_state()
                is_start = False

            detail_for_agent0 = BattleField(
                battle_field_total=detail,
                team=0
            )

            detail_for_agent1 = BattleField(
                battle_field_total=detail,
                team=1
            )

            agent0_s0_list = []
            for hive in detail_for_agent0.get_self_hives():
                agent0_s0_list.append(get_status_rewards_from_detail_v2(detail_for_agent0, hive)[1])
            agent1_r11, agent1_s0 = get_status_rewards_from_detail(detail_for_agent1)
            agent0_a0_list, agent0_action_list = agent_0.generate_action(state, score, detail_for_agent0)
            action_list = [agent0_action_list, agent_1.generate_action(state, score, detail_for_agent1)]
            state, score, is_terminate, detail = grid.step(action_list)
            s1_detail_for_agent0 = BattleField(
                battle_field_total=detail,
                team=0
            )
            s1_detail_for_agent1 = BattleField(
                battle_field_total=detail,
                team=1
            )
            agent0_s1_list = []
            agent0_r0 = None
            for hive in detail_for_agent0.get_self_hives():
                agent0_r0, agent0_s1 = get_status_rewards_from_detail_v2(s1_detail_for_agent0, hive)
                agent0_s1_list.append(agent0_s1)
            agent1_r0, agent1_s1 = get_status_rewards_from_detail(s1_detail_for_agent1)
            # train agent0
            # s1处的最大动作
            a1_list = [agent_0.greedy(agent0_s1) for agent0_s1 in agent0_s1_list]
            key1 = ["%s_%s" % (agent0_s1, a1) for agent0_s1, a1 in zip(agent0_s1_list, a1_list)]
            key = ["%s_%s" % (agent0_s0, agent0_a0) for agent0_s0, agent0_a0 in zip(agent0_s0_list, agent0_a0_list)]
            # 利用qlearning方法更新值函数

            for k, k1 in zip(key, key1):
                agent_0.qfunc[k] = agent_0.qfunc.get(k, 0.0) + alpha * (agent0_r0 + gamma * agent_0.qfunc.get(k1, 0.0) - agent_0.qfunc.get(k, 0.0))

            if is_terminate:
                agent_0.save_agent_model(agent_model_path)
                # print('Over, score:', score, detail)
                s0, s1 = detail.get_score()
                if s0 >= s1:
                    win += 1
                total += 1
                print('iter: %d, score: %s, win: %d, total: %d, win_rate: %f, beat: %s, state_num: %d' % (iter, str(detail.get_score()), win, total, win / total, type(agent_1), len(agent_0.qfunc)))
                # print(detail.get_battle_reports())
                # print(detail_for_agent0.get_scout_reports())
                # print(detail_for_agent1.get_scout_reports())
                break

            else:
                # print('Round, score:', score, detail)
                pass

