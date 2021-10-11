from gym_foo.model.action.action import Action
from gym_foo.model.hive import Hive
from gym_foo.model.single_march import SingleMarch
from gym_foo.model.march import March
from gym_foo.model.tower import Tower

class Reinforce(Action):

    TARGET_TYPE_TOWER = March.TARGET_TYPE_TOWER  # 目标为塔
    TARGET_TYPE_HIVE = March.TARGET_TYPE_HIVE  # 目标为堡

    def __init__(self, hive_id, target_id, troops_num, target_type):
        super().__init__(hive_id)
        self._target_id = target_id
        self._troops_num = troops_num
        self._target_type = target_type

    def get_target_id(self):
        return self._target_id

    def get_troops_num(self):
        return self._troops_num

    def get_target_type(self):
        return self._target_type

    def do(self, start_hive: Hive, target_hive: Hive=None, target_tower: Tower=None):
        start_hive.attack(self._troops_num)
        if self._target_type == self.TARGET_TYPE_HIVE:
            return SingleMarch(
                start_cord=start_hive.get_cord(),
                target_cord=target_hive.get_cord(),
                hive_id=start_hive.get_id(),
                type=March.TYPE_REINFORCE,
                troops_num=self._troops_num,
                target_type=March.TARGET_TYPE_HIVE,
                target_id=target_hive.get_id()
            )
        elif self._target_type == self.TARGET_TYPE_TOWER:
            return SingleMarch(
                start_cord=start_hive.get_cord(),
                target_cord=target_tower.get_cord(),
                hive_id=start_hive.get_id(),
                type=March.TYPE_REINFORCE,
                troops_num=self._troops_num,
                target_type=March.TARGET_TYPE_TOWER,
                target_id=target_tower.get_id()
            )

    def __repr__(self):
        return str({
            'hive_id': self._hive_id,
            'target_id': self._target_id,
            'troops_num': self._troops_num,
            'target_type': self._target_type
        })