from gym_foo.model.rally_march import RallyMarch
from gym_foo.model.rally_waiting import RallyWaiting
from gym_foo.model.action.action import Action
from gym_foo.model.hive import Hive
from typing import List
from gym_foo.model.march import March

class JoinRally(Action):

    def __init__(self, hive_id, rally_id, troops_num):
        super().__init__(hive_id)
        self._rally_id = rally_id
        self._troops_num = troops_num

    def do(self, start_hive: Hive, rally_hive: Hive, rally: RallyWaiting, march_list: List[March]):
        for march in march_list:
            if start_hive.get_id() == march.get_hive_id() and march.get_target_id() == rally.get_id() and march.get_target_type() == March.TARGET_TYPE_RALLY:
                raise Exception('Already join rally.')
        start_hive.attack(troops_num=self._troops_num)
        return March(
            start_cord=start_hive.get_cord(),
            target_cord=rally_hive.get_cord(),
            hive_id=start_hive.get_id(),
            type=March.TYPE_JOIN_RALLY,
            target_type=March.TARGET_TYPE_HIVE,
            target_id=self._rally_id
        )

    def __repr__(self):
        return str({
            'hive_id': self._hive_id,
            'rally_id': self._rally_id,
            'troops_num': self._troops_num
        })


