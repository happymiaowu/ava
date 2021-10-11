from gym_foo.model.action.action import Action
from gym_foo.model.hive import Hive
from gym_foo.model.tower import Tower

class RecallOccupied(Action):

    TARGET_TYPE_TOWER = 0  # 目标为塔
    TARGET_TYPE_HIVE = 1  # 目标为堡

    def __init__(self, hive_id, target_type, target_id):
        super().__init__(hive_id)
        self._target_type = target_type
        self._target_id = target_id

    def get_target_type(self):
        return self._target_type

    def get_target_id(self):
        return self._target_id

    def do(self, hive: Hive, occupied_hive: Hive=None, occupied_tower: Tower=None):
        if self._target_type == self.TARGET_TYPE_TOWER:
            return occupied_tower.recall_march(hive)
        elif self._target_type == self.TARGET_TYPE_HIVE:
            return occupied_hive.recall_march(hive)

    def __repr__(self):
        return str({
            'hive_id': self._hive_id,
            'target_id': self._target_id,
            'target_type': self._target_type
        })