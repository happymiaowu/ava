

class Action():

    def __init__(self, hive_id):
        self._hive_id = hive_id

    def get_hive_id(self):
        return self._hive_id

    def do(self, **kwargs):
        pass
