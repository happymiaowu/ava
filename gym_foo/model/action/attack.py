from gym_foo.model.action.action import Action
from gym_foo.model.single_march import SingleMarch
from gym_foo.model.march import March

class Attack(Action):

    TARGET_TYPE_TOWER = March.TARGET_TYPE_TOWER     # 目标为塔
    TARGET_TYPE_HIVE = March.TARGET_TYPE_HIVE      # 目标为堡

    def __init__(self, hive_id, target_cord, troops_num, target_type, target_id):
        super().__init__(hive_id)
        self._target_cord = target_cord
        self._troops_num = troops_num
        self._target_type = target_type
        self._target_id = target_id


    def get_troops_num(self):
        return self._troops_num

    def get_target_type(self):
        return self._target_type

    def get_target_id(self):
        return self._target_id

    def do(self, hive):
        march = SingleMarch(
            start_cord=hive.get_cord(),
            target_cord=self._target_cord,
            hive_id=hive.get_id(),
            troops_num=self._troops_num,
            type = March.TYPE_ATTACK,
            target_type=self._target_type,
            target_id=self._target_id
        )
        hive.attack(troops_num=self._troops_num)
        return march

    def __repr__(self):
        return str({
            'hive_id': self._hive_id,
            'target_cord': self._target_cord,
            'troops_num': self._troops_num,
            'target_type': self._target_type,
            'target_id': self._target_id
        })