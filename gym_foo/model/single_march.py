from gym_foo.model.march import March
from gym_foo.model.troops_list import TroopsList
from gym_foo.model.troops import Troops

class SingleMarch(March):

    def __init__(self, start_cord, target_cord, hive_id, type, troops_num, target_type, target_id, march_id=None, is_scout_back=False):
        super().__init__(
            start_cord=start_cord,
            target_cord=target_cord,
            hive_id=hive_id,
            type=type,
            target_type=target_type,
            target_id=target_id,
            march_id=march_id
        )
        self._troops_num = troops_num
        if is_scout_back:
            self._speed = March.SCOUT_SPEED

    def get_troops_num(self):
        return self._troops_num

    def get_hiding_result(self):
        return SingleMarch(
            march_id=self._march_id,
            start_cord=self._start_cord,
            target_cord=self._target_cord,
            hive_id=self._hive_id,
            troops_num=None,  # 隐藏军队数量
            type=self._type,
            target_type=self._target_type,
            target_id= self._target_id
        )

    def occupied_tower(self, tower):
        tower.set_occupied(
            int(self._hive_id.split('_')[0]),
            TroopsList(
                troops_list=[Troops(self._hive_id, self._troops_num)],
                header_hive_id=self._hive_id
            )
        )

    def get_troops_list(self):
        return TroopsList([Troops(self._hive_id, self._troops_num)], self._hive_id)

    def set_troops_list(self, troops_list: TroopsList):
        if len(troops_list.get_troops_list()) != 1:
            raise Exception('troops list', troops_list, 'invalid.')
        troops = troops_list.get_troops_list()[0]
        self._troops_num = troops.get_troops_num()
        self._hive_id = troops.get_hive_id()


    def __repr__(self):
        return str({
            'march_id': self._march_id,
            'start_cord': self._start_cord,
            'target_cord': self._target_cord,
            'hive_id': self._hive_id,
            'troops_num': self._troops_num,
            'now_cord': self._now_cord,
            'speed': self._speed,
            'type': self._type
        })