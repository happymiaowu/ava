import sys
import gym
import time
from gym import wrappers
from gym_foo.agent.agent import Agent
from gym_foo.agent.random_agent import RandomAgent
from gym_foo.agent.q_learning_agent import QLearnAgent
from gym_foo.agent.q_learning_agent_v2 import QLearnAgent_V2
from gym_foo.model.battlefield_detail import BattleField
from Utils import *
import os


object_path = os.path.dirname(__file__)
alpha = 0.5
gamma = 0.9
agent_model_path_0 = os.path.join(object_path, 'agent_model/train_1/agent0.pkl')
agent_model_path_1 = os.path.join(object_path, 'agent_model/train_1/agent1.pkl')
if __name__ == "__main__":
    grid = gym.make('ava-v1')
    sleeptime = 1

    grid = wrappers.Monitor(grid, './videos', force=True)  # 记录回放动画
    grid.reset()
    grid.render()
    time.sleep(sleeptime)
    is_start = True
    agent_0 = QLearnAgent_V2(team=0, agent_model_path=None)
    agent_1 = QLearnAgent(team=1, agent_model_path=os.path.join(object_path, 'agent_model/train_0/agent0.pkl'))
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
        agent0_r11, agent0_s0 = get_status_rewards_from_detail(detail_for_agent0)
        agent1_r11, agent1_s0 = get_status_rewards_from_detail(detail_for_agent1)
        agent0_a0, agent0_action_list = agent_0.generate_action(state, score, detail_for_agent0)
        agent1_a0, agent1_action_list = agent_0.generate_action(state, score, detail_for_agent0)
        action_list = [agent0_action_list, agent1_action_list]
        state, score, is_terminate, detail = grid.step(action_list)
        s1_detail_for_agent0 = BattleField(
            battle_field_total=detail,
            team=0
        )
        s1_detail_for_agent1 = BattleField(
            battle_field_total=detail,
            team=1
        )
        agent0_r0, agent0_s1 = get_status_rewards_from_detail(s1_detail_for_agent0)
        agent1_r0, agent1_s1 = get_status_rewards_from_detail(s1_detail_for_agent1)
        # train agent0
        # s1处的最大动作
        a1 = agent_0.greedy(agent0_s1)
        key1 = "%s_%s" % (agent0_s1, a1)
        key = "%s_%s" % (agent0_s0, agent0_a0)
        # 利用qlearning方法更新值函数
        agent_0.qfunc[key] = agent_0.qfunc.get(key, 0.0) + alpha * (agent0_r0 + gamma * agent_0.qfunc.get(key, 0.0) - agent_0.qfunc.get(key, 0.0))
        if is_terminate:
            agent_0.save_agent_model(agent_model_path_0)
            agent_1.save_agent_model(agent_model_path_1)
            print('Over, score:', score, detail)
            print(detail.get_battle_reports())
            print(detail_for_agent0.get_scout_reports())
            print(detail_for_agent1.get_scout_reports())
            break

        else:
            print('Round, score:', score, detail)


