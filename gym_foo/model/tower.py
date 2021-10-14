from gym_foo.model.troops_list import TroopsList
from gym_foo.model.troops import Troops
from gym_foo.model.march import March
from gym_foo.model.single_march import SingleMarch
import uuid
from typing import Tuple
from gym_foo.model.report.scout_tower_report import ScoutTowerReport
from gym_foo.model.hive import Hive

# 塔
class Tower():

    def __init__(self,
                 tower_id: str,
                 score: int,
                 cord: Tuple[int, int],
                 occupied: bool = False,
                 is_wonder: bool = False,
                 troops: TroopsList = None
                 ):
        self._id = tower_id
        self._score_per_round = score
        self._cord = cord
        self._occupied = occupied
        self._troops = troops
        self._is_wonder = is_wonder
        self._team = None

    def get_id(self):
        return self._id

    def is_wonder(self):
        return self._is_wonder

    # 查询谁占领
    def who_occupied(self):
        if not self._occupied:
            return None

        return self._team

    # 生成侦查报告
    def generate_scout_report(self, scout_hive_id, round):
        return ScoutTowerReport(
            scout_hive_id=scout_hive_id,
            target_tower_id=self._id,
            cord=self._cord,
            team=self._team,
            round=round,
            rein_troops=self._troops
        )

    # 设置占领
    def set_occupied(self, team, occupied_troops: TroopsList):
        self._team = team
        self._occupied = True
        self._troops = occupied_troops

    def get_cord(self):
        return self._cord

    def add_reinforce(self, march: SingleMarch, hive: Hive):
        self._troops.add_troops(Troops(march.get_hive_id(), march.get_troops_num()), hive)

    # 迁城导致守军回家
    def kick_march(self, hive: Hive) -> None:
        if self._troops is None:
            return
        troops = []
        for occupied in self._troops.get_troops_list():
            if occupied.get_hive_id() == hive.get_id():
                hive.recall_suddenly(troops_num=occupied.get_troops_num())
                continue
            troops.append(occupied)
        if len(troops) == 0:
            self._escape()
        else:
            self._troops = TroopsList(troops_list=troops, header_hive_id=troops[0].get_hive_id())

    # 召回守军
    def recall_march(self, hive):
        troops = []
        march = None
        for occupied in self._troops.get_troops_list():
            if occupied.get_hive_id() == hive.get_id():
                march = SingleMarch(
                    march_id=uuid.uuid4().hex,
                    start_cord=self._cord,
                    target_cord=hive.get_cord(),
                    hive_id=hive.get_id(),
                    troops_num=occupied.get_troops_num(),
                    type=March.TYPE_BACK,
                    target_type=March.TARGET_TYPE_HIVE,
                    target_id=hive.get_id()
                )
                continue
            troops.append(occupied)
        if march is None:
            raise Exception('Troops not found, cannot recall')
        if len(troops) == 0:
            self._escape()
        else:
            self._troops = TroopsList(troops_list=troops, header_hive_id=troops[0].get_hive_id())
        return march

    # 离开
    def _escape(self):
        self._occupied = False
        self._team = None
        self._troops = None

    # 查询每回合积分获取数
    def get_score_per_round(self):
        return self._score_per_round

    # 战斗后更新军队数量
    def set_troops_num(self, troops_list: TroopsList):
        self._troops = troops_list

    def get_troops(self):
        return self._troops

    def generate_hiding_result(self):
        return Tower(
            tower_id=self._id,
            score=self._score_per_round,
            cord=self._cord,
            occupied=self._occupied,
            troops=None,
            is_wonder=self._is_wonder
        )

    def __repr__(self):
        return str({
            'tower_id': self._id,
            'cord': self._cord,
            'is_occupied': self._occupied,
            'who_occupied': self._team,
            'troops': self._troops,
            'is_wonder': self._is_wonder,
            'score_per_round': self._score_per_round
        })
