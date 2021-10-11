from gym_foo.model.common import common
from gym_foo.model.troops_list import TroopsList
import uuid
# 行军
class March():

    TYPE_REINFORCE = 0        # 防御
    TYPE_BACK = 1             # 返回
    TYPE_JOIN_RALLY = 2       # 加入集结
    TYPE_SCOUT = 3            # 侦查
    TYPE_ATTACK = 4           # 攻击


    TARGET_TYPE_TOWER = 0     # 目标为塔
    TARGET_TYPE_HIVE = 1      # 目标为堡
    TARGET_TYPE_RALLY = 2     # 目标为集结

    BASE_SPEED = 0.2
    SCOUT_SPEED = 1

    def __init__(self,
                 start_cord,  # 起始坐标
                 target_cord, # 目标坐标
                 hive_id,     # 军队所属城堡ID
                 type,        # 类型
                 target_type,
                 target_id,
                 march_id=None
                 ):
        if march_id is None:
            march_id = uuid.uuid4().hex
        self._target_type = target_type
        self._target_id = target_id
        self._march_id = march_id
        self._start_cord = start_cord
        self._target_cord = target_cord
        self._hive_id = hive_id
        if type not in (self.TYPE_REINFORCE, self.TYPE_ATTACK, self.TYPE_BACK, self.TYPE_JOIN_RALLY, self.TYPE_SCOUT):
            print('Type is invalid')
            raise Exception('March Type {} Invalid' % type)
        self._type = type

        # 行军时间
        self._during = common.dist(start_cord=start_cord, end_cord=target_cord)

        # 当前速度
        self._speed = self.SCOUT_SPEED if self._type == self.TYPE_SCOUT else self.BASE_SPEED

        # 当前坐标
        self._now_cord = start_cord

    def get_target_detail(self):
        return self._target_type, self._target_id

    def get_target_type(self):
        return self._target_type

    def get_target_id(self):
        return self._target_id

    def get_target_cord(self):
        return self._target_cord

    def get_hive_id(self):
        return self._hive_id

    def get_now_cord(self):
        return self._now_cord

    def get_march_id(self):
        return self._march_id

    def get_start_cord(self):
        return self._start_cord

    def get_type(self):
        return self._type

    def get_speed(self):
        return self._speed

    def next_round(self):
        self._now_cord = common.count_next_cord(self._now_cord, self._target_cord, self._speed)

    def recall(self, hive):
        if hive.get_cord == self.get_target_cord():
            return

        self._start_cord, self._target_cord = self._target_cord, self._start_cord

    def get_hiding_result(self):
        pass

    def occupied_tower(self, tower):
        pass

    def speedup(self):
        self._speed *= 1.5

    def get_troops_list(self):
        pass

    def set_troops_list(self, troops_list: TroopsList):
        pass