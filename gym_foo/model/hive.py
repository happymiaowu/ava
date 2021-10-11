import random
from gym_foo.model.common import common
from gym_foo.model.troops import Troops
from gym_foo.model.march import March
from gym_foo.model.single_march import SingleMarch
import uuid
from gym_foo.model.hide_hive import HideHive
from gym_foo.model.troops_list import TroopsList
from gym_foo.model.report.scout_hive_report import ScoutHiveReport

# 城堡
class Hive():

    TEL_COLDDOWN = 300
    MAX_TEL_TIMES = 5

    def __init__(self,
                 id,
                 team,
                 max_march_num = None,
                 max_troop_num = None,
                 max_rally_size = None,
                 buff = None,
                 troops_num = None,
                 cord = None,
                 tel_times = MAX_TEL_TIMES,
                 recall_times = 5,
                 speedup_times = 5,
                 ):
        # ID
        self._id = id

        # 哪个队
        self._team = team

        # 最大出兵数
        self._max_march_num = random.randint(4, 6) if max_march_num is None else max_march_num

        # 使用出兵数
        self._using_march_num = 0

        # 最大带兵量
        self._max_troop_num = random.randint(8000, 20000) if max_troop_num is None else max_troop_num

        # 集结兵量
        self._rally_size = random.randint(40000, 100000) if max_rally_size is None else max_rally_size

        # 加成
        self._buff = random.randint(1, 10) if buff is None else buff

        # 家里兵量
        self._troops_num = random.randint(40000, 100000) if troops_num is None else troops_num

        # 坐标
        self._cord = cord

        # 迁城次数
        self._tel_times = tel_times

        # 迁城倒计时
        self._tel_countdown = None

        # 召回次数
        self._recall_times = recall_times

        # 加速次数
        self._speedup_times = speedup_times

        # 驻守
        self._rein_troops = TroopsList(
            troops_list=[],
            header_hive_id=self._id
        )

    def get_buff(self):
        return self._buff

    def get_teleport_times(self):
        return self._tel_times

    def get_id(self):
        return self._id

    def get_max_troops_num(self):
        return self._max_troop_num

    def get_troops_num(self):
        return self._troops_num

    def get_rein_troops(self):
        return self._rein_troops

    def get_hive_troops_list(self):
        return TroopsList(
            troops_list=[Troops(hive_id=self._id, troops_num=self._troops_num)] + self._rein_troops.get_troops_list(),
            header_hive_id=self._id
        )

    def add_rein_troops(self, march: SingleMarch):
        self._rein_troops.add_troops(Troops(march.get_hive_id(), march.get_troops_num()))

    def get_using_march_num(self):
        return self._using_march_num

    def get_max_march_num(self):
        return self._max_march_num

    def random_teleport(self, empty_cord):
        self.teleport(random.choice(empty_cord), is_random=True)

    def teleport(self, new_cord, is_random=False):
        if self._tel_times == 0 and is_random == False:
            raise Exception('no teleport times.')

        if not common.check_cord_valid(new_cord):
            raise Exception('teleport position invalid.')

        # 计算迁城次数
        self._tel_times -= 1
        if self._tel_countdown == None:
            self._tel_countdown = self.TEL_COLDDOWN

        # 迁城
        self._cord = new_cord

    def set_troops_num(self, troops_list: TroopsList):
        for troops in troops_list.get_troops_list():
            if troops.get_hive_id() == self._id:
                self._troops_num = troops.get_troops_num()
            else:
                self._rein_troops.set_single_troop_num(troops.get_hive_id(), troops.get_troops_num())


    def attack(self, troops_num):
        # 兵数
        if troops_num > self._troops_num:
            raise Exception('troops num is exceed!')
        # 最大行军数量
        if self._using_march_num >= self._max_march_num:
            raise Exception('march num is exceed!, hive_id: %s, using_march_num: %d, max_march_num: %d' % (self._id, self._using_march_num, self._max_march_num))

        self._using_march_num += 1
        self._troops_num -= troops_num


    def get_cord(self):
        return self._cord

    #TODO
    def generate_hiding_result(self):
        return HideHive(
            id = self._id,
            team = self._team,
            cord=self._cord,
        )

    def next_round(self):
        # 处理迁城恢复次数
        if self._tel_countdown == None:
            return

        self._tel_countdown -= 1
        if self._tel_countdown == 0:
            self._tel_times += 1
            self._tel_countdown = None if self._tel_times == self.MAX_TEL_TIMES else self.TEL_COLDDOWN


    # 驻防友军迁城导致军队回家
    def kick_march(self, hive_id):
        self._rein_troops.remove_troops(hive_id=hive_id)

    # 生成侦查报告
    def generate_scout_report(self, scout_hive_id, round):
        return ScoutHiveReport(
            scout_hive_id=scout_hive_id,
            target_hive_id=self._id,
            cord=self._cord,
            team=self._team,
            round=round,
            buff=self._buff,
            rein_troops=self._rein_troops,
            troops_num=self._troops_num
        )

    # 城堡的守军被召回
    def recall_march(self, hive):
        march = None
        for troops in self._rein_troops.get_troops_list():
            if troops.get_hive_id() == hive.get_id():
                march = SingleMarch(
                    start_cord=self._cord,
                    target_cord=hive.get_cord(),
                    hive_id=hive.get_id(),
                    troops_num=troops.get_troops_num(),
                    type=March.TYPE_BACK,
                    target_type=March.TARGET_TYPE_HIVE,
                    target_id=hive.get_id()
                )
                continue
        self._rein_troops.remove_troops(hive_id=hive.get_id())
        if march is None:
            raise Exception('Troops not found, cannot recall')
        return march

    def recall_suddenly(self, troops_num):
        print('recall suddenly')
        self._using_march_num -= 1
        self._troops_num += troops_num

    def __repr__(self):
        return str({
            'id': self._id,
            'team': self._team,
            'cord': self._cord,
            'tel_times': self._tel_times,
            'tel_colddown': self._tel_countdown,
            'using_march_num': self._using_march_num,
            'troops_num': self._troops_num
        })