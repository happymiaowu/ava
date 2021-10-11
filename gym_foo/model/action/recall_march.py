from gym_foo.model.action.action import Action

class RecallMarch(Action):

    def __init__(self, hive_id, march_id):
        super().__init__(hive_id)
        self._march_id = march_id

    def get_march_id(self):
        return self._march_id

    def do(self, march, hive):
        return march.recall(hive=hive)

    def __repr__(self):
        return str({
            'hive_id': self._hive_id,
            'march_id': self._march_id
        })