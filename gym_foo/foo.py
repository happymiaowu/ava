import sys
import gym
import time
from gym import wrappers
from gym_foo.agent.agent import Agent
from gym_foo.agent.random_agent import RandomAgent
from gym_foo.model.battlefield_detail import BattleField
from gym_foo.agent.q_learning_agent_v2 import QLearnAgent_V2
from gym_foo.agent.attack_agent import TowerRushAgent
import os

#main函数
if __name__ == "__main__":
    grid = gym.make('ava-v1')
    #states = grid.getStates()  # 获得网格世界的状态空间
    #actions = grid.getAction()  # 获得网格世界的动作空间
    sleeptime = 1
    # 设置系统初始状态
    # s0 = 1
    # grid.setAction(s0)
    # 对训练好的策略进行测试
    grid = wrappers.Monitor(grid, './videos', force=True)  # 记录回放动画
    # 随机初始化，寻找金币的路径
    '''
    for i in range(20):
        #随机初始化
        s0 = grid.reset()
        grid.render()
        time.sleep(sleeptime)
        t = False
        count = 0
        #判断随机状态是否在终止状态中
        if s0 in terminate_states:
            print("reach the terminate state %d" % (s0))
        else:
            while False == t and count < 100:
                a1 = greedy(qfunc, s0)
                print(s0, a1)
                grid.render()
                time.sleep(sleeptime)
                key = "%d_%s" % (s0, a)
                # 与环境进行一次交互，从环境中得到新的状态及回报
                s1, r, t, i = grid.step(a1)
                if True == t:
                    #打印终止状态
                    print(s1)
                    grid.render()
                    time.sleep(sleeptime)
                    print("reach the terminate state %d" % (s1))
                # s1处的最大动作
                s0 = s1
                count += 1
    '''

    grid.reset()
    grid.render()
    time.sleep(sleeptime)
    is_start = True
    object_path = os.path.dirname(__file__)
    agent_1 = QLearnAgent_V2(team=0, agent_model_path='./agent_model_v2/train_0/agent0.pkl')
    agent_2 = TowerRushAgent(team=1)
    while True:
        if is_start:
            state, score, is_terminate, detail = grid.initial_state()
            is_start = False

        # action_list = [ActionList(team=0, action_list=[Teleport(hive_id='0_0', new_cord=(7, 7))]), ActionList(team=1, action_list=[])]

        detail_for_agent0 = BattleField(
            battle_field_total=detail,
            team=0
        )

        detail_for_agent1 = BattleField(
            battle_field_total=detail,
            team=1
        )

        _, act1 = agent_1.generate_action(state, score, detail_for_agent0)
        act2 = agent_2.generate_action(state, score, detail_for_agent1)
        action_list = [act1, act2]
        state, score, is_terminate, detail = grid.step(action_list)
        if True == is_terminate:
            print('Over, score:', score, detail)
            print(detail.get_battle_reports())
            print(detail_for_agent0.get_scout_reports())
            print(detail_for_agent1.get_scout_reports())
            break

        else:
            print('Round, score:', detail.get_score())


