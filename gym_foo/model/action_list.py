from gym_foo.model.action.speedup import SpeedUp
from gym_foo.model.action.scout import Scout
from gym_foo.model.action.attack import Attack
from gym_foo.model.action.recall_march import RecallMarch
from gym_foo.model.action.recall_occupied import RecallOccupied
from gym_foo.model.action.reinforce import Reinforce
from gym_foo.model.action.teleport import Teleport
from gym_foo.model.action.rally import Rally
from typing import List, Dict
from gym_foo.model.hive import Hive
from gym_foo.model.march import March
from gym_foo.model.tower import Tower
from gym_foo.model.action.rally_cancel import RallyCancel

class ActionList():

    def __init__(self, team, action_list=None):
        self._team = team
        if action_list is None:
            action_list = []
        self._action_list = action_list
        self._types2action = {
            SpeedUp: [],
            Scout: [],
            Attack: [],
            RecallMarch:[],
            RecallOccupied:[],
            Reinforce:[],
            Teleport: [],
            Rally: [],
            RallyCancel: []
        }
        for action in action_list:
            for t in self._types2action.keys():
                if type(action) == t:
                    self._types2action[t].append(action)
                    break

    def get_action_list(self):
        return self._action_list

    def get_team(self):
        return self._team

    def get_type2action(self):
        return self._types2action

    def __repr__(self):
        new_dict = {}
        if len(self._types2action[SpeedUp]) > 0:
            new_dict['Speedup'] = self._types2action[SpeedUp]
        if len(self._types2action[Scout]) > 0:
            new_dict['Scout'] = self._types2action[Scout]
        if len(self._types2action[Attack]) > 0:
            new_dict['Attack'] = self._types2action[Attack]
        if len(self._types2action[RecallMarch]) > 0:
            new_dict['RecallMarch'] = self._types2action[RecallMarch]
        if len(self._types2action[RecallOccupied]) > 0:
            new_dict['RecallOccupied'] = self._types2action[RecallOccupied]
        if len(self._types2action[Reinforce]) > 0:
            new_dict['Reinforce'] = self._types2action[Reinforce]
        if len(self._types2action[Teleport]) > 0:
            new_dict['Teleport'] = self._types2action[Teleport]
        if len(self._types2action[Rally]) > 0:
            new_dict['Rally'] = self._types2action[Rally]
        if len(self._types2action[RallyCancel]) > 0:
            new_dict['RallyCancel'] = self._types2action[RallyCancel]

        return str(new_dict)
