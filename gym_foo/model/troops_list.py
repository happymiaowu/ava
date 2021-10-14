from gym_foo.model.troops import Troops
from typing import List

class TroopsList:

    def __init__(self, troops_list: List[Troops], header_hive_id):
        self._troops_list = troops_list
        self._header_hive_id = header_hive_id

    def get_troops_list(self) -> List[Troops]:
        return self._troops_list

    def is_hive_in(self, hive_id):
        for troops in self._troops_list:
            if troops.get_hive_id() == hive_id:
                return True
        return False

    def add_troops(self, new_troops: Troops, hive):
        is_found = False
        for troops in self._troops_list:
            if troops.get_hive_id() == new_troops.get_hive_id():
                troops.set_troops_num(troops.get_troops_num() + new_troops.get_troops_num())
                hive.decr_march_num()
                is_found = True
        if not is_found:
            self._troops_list.append(new_troops)

    def remove_troops(self, hive_id):
        troops_list = []
        rm_troops = None
        for troops in self._troops_list:
            if troops.get_hive_id() == hive_id:
                rm_troops = troops
                continue
            troops_list.append(troops)
        self._troops_list = troops_list
        return rm_troops

    def _change_header(self):
        self.header_hive_id = self._troops_list[0].get_hive_id()

    def get_header_hive_id(self):
        return self._header_hive_id

    def count_troops_num(self):
        return sum([troops.get_troops_num() for troops in self._troops_list])

    def set_single_troop_num(self, hive_id, troops_num):
        for troops in self._troops_list:
            if hive_id == troops.get_hive_id():
                troops.set_troops_num(troops_num)

    def __repr__(self):
        return str({
            'troop_list': self._troops_list,
            'header_hive_id': self._header_hive_id
        })