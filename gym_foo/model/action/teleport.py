from gym_foo.model.action.action import Action

class Teleport(Action):

    def __init__(self, hive_id, new_cord):
        super().__init__(hive_id)
        self._new_cord = new_cord

    def do(self, hive, empty_cord):
        hive.teleport(new_cord=self._new_cord, empty_cord=empty_cord)

    def get_new_cord(self):
        return self._new_cord

    def __repr__(self):
        return str({
            'hive_id': self._hive_id,
            'new_cord': self._new_cord
        })