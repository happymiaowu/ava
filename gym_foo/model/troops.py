

class Troops():

    def __init__(self, hive_id, troops_num):
        self._hive_id = hive_id
        self._troops_num = troops_num

    def get_hive_id(self):
        return self._hive_id

    def get_troops_num(self):
        return self._troops_num

    def set_troops_num(self, troops_num):
        self._troops_num = troops_num

    def __repr__(self):
        return str({
            'hive_id': self._hive_id,
            'troops_num': self._troops_num
        })