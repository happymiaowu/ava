from gym_foo.model.march import March
from gym_foo.model.troops_list import TroopsList

class RallyMarch(March):

    def __init__(self, start_cord, target_cord, hive_id, type, troops: TroopsList, target_type, target_id, march_id=None):
        super().__init__(
            start_cord=start_cord,
            target_cord=target_cord,
            hive_id=hive_id,
            type=type,
            target_type=target_type,
            target_id=target_id,
            march_id=march_id
        )
        self._troops = troops

    def get_troops(self):
        return self._troops

    def get_hiding_result(self):
        return RallyMarch(
            march_id=self._march_id,
            start_cord=self._start_cord,
            target_cord=self._target_cord,
            hive_id=self._hive_id,
            troops=None,  # 隐藏军队信息
            type=self._type,
            target_type=self._target_type,
            target_id=self._target_id
        )

    def occupied_tower(self, tower):
        tower.set_occupied(
            int(self._hive_id.split('_')[0]),
            self._troops
        )

    def get_troops_list(self):
        return self._troops

    # 战斗后减员调用
    def set_troops_list(self, troops_list: TroopsList):
        if len(troops_list.get_troops_list()) == 0:
            raise Exception('troops list', troops_list, 'invalid.')
        self._troops = troops_list.get_troops_list()

    def __repr__(self):
        return str({
            'march_id': self._march_id,
            'start_cord': self._start_cord,
            'target_cord': self._target_cord,
            'hive_id': self._hive_id,
            'troops': self._troops,
            'now_cord': self._now_cord,
            'speed': self._speed
        })