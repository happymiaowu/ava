from gym_foo.model.action.action import Action
from gym_foo.model.troops import Troops
from gym_foo.model.march import March
from gym_foo.model.troops_list import TroopsList
from gym_foo.model.rally_march import RallyMarch
from gym_foo.model.rally_waiting import RallyWaiting

class Rally(Action):

    TARGET_TYPE_TOWER = 0     # 目标为塔
    TARGET_TYPE_HIVE = 1      # 目标为堡

    def __init__(self, hive_id, pending_times, troops_num, target_type, target_id):
        super().__init__(hive_id)
        self._pending_times = pending_times
        self._troops_num = troops_num
        self._target_type = target_type
        self._target_id = target_id

    def get_target_type(self):
        return self._target_type

    def get_target_id(self):
        return self._target_id

    def do(self, hive):
        print(hive.get_using_march_num(), hive.get_max_march_num())
        hive.attack(self._troops_num)
        return RallyWaiting(
            hive_id=self._hive_id,
            troops_num=self._troops_num,
            target_type=self._target_type,
            target_id=self._target_id,
            pending_times=self._pending_times
        )

    def __repr__(self):
        return str({
            'hive_id': self._hive_id,
            'troops_num': self._troops_num,
            'target_type': self._target_type,
            'target_id': self._target_id
        })
