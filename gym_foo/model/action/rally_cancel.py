from gym_foo.model.action.action import Action
from gym_foo.model.rally_waiting import RallyWaiting
from gym_foo.model.hive import Hive
from typing import Dict

class RallyCancel(Action):

    def __init__(self, hive_id, rally_id):
        super().__init__(hive_id)
        self._rally_id = rally_id

    def get_rally_id(self):
        return self._rally_id

    def do(self, rally: RallyWaiting, hive_dict: Dict[str, Hive]):
        rally.cancel(hive_dict)

    def __repr__(self):
        return str({
            'hive_id': self._hive_id,
            'rally_id': self._rally_id
        })