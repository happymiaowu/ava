from gym_foo.model.action.action import Action
from gym_foo.model.single_march import SingleMarch
from gym_foo.model.march import March
from gym_foo.model.hive import Hive
from gym_foo.model.tower import Tower


class Scout(Action):

    TARGET_TYPE_TOWER = March.TARGET_TYPE_TOWER  # 目标为塔
    TARGET_TYPE_HIVE = March.TARGET_TYPE_HIVE  # 目标为堡

    def __init__(self, hive_id, target_type, target_id):
        super().__init__(hive_id)
        self._target_type = target_type
        self._target_id = target_id

    def get_target_type(self):
        return self._target_type

    def get_target_id(self):
        return self._target_id

    def do(self, scout_hive: Hive, target_hive: Hive=None, target_tower: Tower=None):
        if self._target_type == self.TARGET_TYPE_HIVE:
            return SingleMarch(
                start_cord=scout_hive.get_cord(),
                target_cord=target_hive.get_cord(),
                hive_id=scout_hive.get_id(),
                type=March.TYPE_SCOUT,
                troops_num=0,
                target_type=March.TARGET_TYPE_HIVE,
                target_id=target_hive.get_id()
            )
        else:
            return SingleMarch(
                start_cord=scout_hive.get_cord(),
                target_cord=target_tower.get_cord(),
                hive_id=scout_hive.get_id(),
                type=March.TYPE_SCOUT,
                troops_num=0,
                target_type=March.TARGET_TYPE_TOWER,
                target_id=target_tower.get_id()
            )

    def __repr__(self):
        return str({
            'hive_id': self._hive_id,
            'target_type': self._target_type,
            'target_id': self._target_id
        })