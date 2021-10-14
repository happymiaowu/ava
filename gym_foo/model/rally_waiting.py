from gym_foo.model.troops_list import TroopsList
from gym_foo.model.troops import Troops
from gym_foo.model.rally_march import RallyMarch
from gym_foo.model.march import March
from gym_foo.model.hive import Hive
from gym_foo.model.tower import Tower
from gym_foo.model.single_march import SingleMarch
from typing import Dict
import uuid

class RallyWaiting():

    TARGET_TYPE_TOWER = 0     # 目标为塔
    TARGET_TYPE_HIVE = 1      # 目标为堡

    def __init__(self, hive_id, troops_num, target_type, target_id, pending_times):
        self._hive_id = hive_id
        self._troops = TroopsList(troops_list=[Troops(hive_id=hive_id, troops_num=troops_num)], header_hive_id=hive_id)
        self._target_type = target_type
        self._target_id = target_id
        self._pending_times = pending_times
        self._id = uuid.uuid4().hex

    def get_id(self):
        return self._id

    def get_hive_id(self):
        return self._hive_id

    def get_target_type(self):
        return self._target_type

    def get_target_id(self):
        return self._target_id

    def get_troops(self):
        return self._troops

    def join(self, hive_id, troops_num, hive: Hive):
        self._troops.add_troops(Troops(hive_id=hive_id, troops_num=troops_num), hive)

    def get_pending_times(self):
        return self._pending_times

    def cancel(self, hive_dict: Dict[str, Hive]):
        back_troops = []
        for troops in self._troops.get_troops_list():
            if troops.get_hive_id() == self._hive_id:
                hive_dict[self._hive_id].recall_suddenly(troops_num=troops.get_troops_num())
            else:
                back_troops.append(
                    SingleMarch(
                        start_cord=hive_dict[self._hive_id].get_cord(),
                        target_cord=hive_dict[troops.get_hive_id()].get_cord(),
                        hive_id=troops.get_hive_id(),
                        type=March.TYPE_BACK,
                        troops_num=troops.get_troops_num(),
                        target_type=March.TARGET_TYPE_HIVE,
                        target_id=troops.get_hive_id()
                    )
                )
        return back_troops


    def next_round(self, start_hive: Hive, target_hive: Hive =None, target_tower:Tower = None):
        if self._pending_times == 0:
            if len(self._troops.get_troops_list()) == 1:
                print('rally canceled.')
                return None
            return RallyMarch(
                start_cord=start_hive.get_cord(),
                target_cord=target_hive.get_cord() if self._target_type == RallyWaiting.TARGET_TYPE_HIVE else target_tower.get_cord(),
                hive_id=self._hive_id,
                type=March.TYPE_ATTACK,
                troops=self._troops,
                target_type=self._target_type,
                target_id=self._target_id
            )

        self._pending_times -= 1
        return None

    def __repr__(self):
        return str({
            'id': self._id,
            'hive_id': self._hive_id,
            'troops': self._troops,
            'target_type': self._target_type,
            'target_id': self._target_id,
            'pending_times': self._pending_times
        })