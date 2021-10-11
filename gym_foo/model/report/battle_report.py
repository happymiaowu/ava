from gym_foo.model.troops_list import TroopsList

class BattleReport():

    def __init__(self,
                 march_id: str,
                 attack_troops_before: TroopsList,
                 attack_troops_after: TroopsList,
                 defend_troops_before: TroopsList,
                 defend_troops_after: TroopsList,
                 attack_buff: int,
                 defend_buff: int,
                 is_attack_win: bool,
                 ):

        self._march_id = march_id
        self._attack_troops_before = attack_troops_before
        self._attack_troops_after = attack_troops_after
        self._defend_troops_before = defend_troops_before
        self._defend_troops_after = defend_troops_after
        self._attack_buff = attack_buff
        self._defend_buff = defend_buff
        self._is_attack_win = is_attack_win

    def get_march_id(self):
        return self._march_id

    def get_attack_troops_before(self):
        return self._attack_troops_before

    def get_attack_troops_after(self):
        return self._attack_troops_after

    def get_defend_troops_before(self):
        return self._defend_troops_before

    def get_defend_troops_after(self):
        return self._defend_troops_after

    def get_attack_buff(self):
        return self._attack_buff

    def get_defend_buff(self):
        return self._defend_buff

    def is_attack_win(self):
        return self._is_attack_win

    def __repr__(self):
        return str({
            'march_id': self._march_id,
            'attack_troops_before': self._attack_troops_before,
            'attack_troops_after': self._attack_troops_after,
            'defend_troops_before': self._defend_troops_before,
            'defend_troops_after': self._defend_troops_after,
            'attack_buff': self._attack_buff,
            'defend_buff': self._defend_buff,
            'is_attack_win': self._is_attack_win
        })


