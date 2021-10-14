from gym_foo.model.single_march import SingleMarch
from gym_foo.model.rally_march import RallyMarch
from gym_foo.model.troops_list import TroopsList
from gym_foo.model.tower import Tower
from gym_foo.model.march import March
from gym_foo.model.troops import Troops
from gym_foo.model.hive import Hive
from typing import Dict
from gym_foo.model.report.battle_report import BattleReport

def battle(troops_list1: TroopsList, troops_list2: TroopsList, header_buff1: int, header_buff2: int, attack_march: March):
    troops_num1 = troops_list1.count_troops_num()
    troops_num2 = troops_list2.count_troops_num()
    troops_power1 = troops_num1 * header_buff1
    troops_power2 = troops_num2 * header_buff2

    is_first_win = troops_power1 >= troops_power2
    left_rate_1 = troops_power1 / (troops_power1 + troops_power2)
    left_rate_2 = troops_power2 / (troops_power1 + troops_power2)
    troops_left1 = []
    for troops in troops_list1.get_troops_list():
        troops_left1.append(Troops(hive_id=troops.get_hive_id(), troops_num=int(troops.get_troops_num() * left_rate_1)))
    troops_left2 = []
    for troops in troops_list2.get_troops_list():
        troops_left2.append(Troops(hive_id=troops.get_hive_id(), troops_num=int(troops.get_troops_num() * left_rate_2)))

    return is_first_win, \
           TroopsList(troops_list=troops_left1, header_hive_id=troops_list1.get_header_hive_id()), \
           TroopsList(troops_list=troops_left2, header_hive_id=troops_list2.get_header_hive_id()), \
           BattleReport(
               march_id=attack_march.get_march_id(),
               attack_troops_before=troops_list1,
               defend_troops_before=troops_list2,
               attack_troops_after=TroopsList(troops_list=troops_left1, header_hive_id=troops_list1.get_header_hive_id()),
               defend_troops_after=TroopsList(troops_list=troops_left2, header_hive_id=troops_list2.get_header_hive_id()),
               attack_buff=header_buff1,
               defend_buff=header_buff2,
               is_attack_win=is_first_win
            )


def occupied_tower(tower: Tower, march: March, hive_dict: Dict[str, Hive]):
    if tower.who_occupied() is None:
        march.occupied_tower(tower)
        return [], None
    elif tower.who_occupied() == int(march.get_hive_id().split('_')[0]) and type(march) == SingleMarch:
        tower.add_reinforce(march, hive_dict[march.get_hive_id()])
        return [], None
    elif tower.who_occupied() == int(march.get_hive_id().split('_')[0]) and type(march) != SingleMarch:
        # 原地解散
        back_march_list = []
        for troop in march.get_troops_list():
            back_march_list.append(SingleMarch(
                start_cord=tower.get_cord(),
                target_cord=hive_dict[troop.get_hive_id()].get_cord(),
                hive_id=troop.get_hive_id(),
                type=March.TYPE_BACK,
                troops_num=troop.get_troops_num(),
                target_type=March.TARGET_TYPE_HIVE,
                target_id=troop.get_hive_id()
            ))
        return back_march_list, None
    else:
        is_tower_win, tower_left, march_left, battle_report = \
            battle(tower.get_troops(),
                   march.get_troops_list(),
                   hive_dict[tower.get_troops().get_header_hive_id()].get_buff(),
                   hive_dict[march.get_hive_id()].get_buff(),
                   march)
        # 更新军队数量
        if is_tower_win:
            tower.set_troops_num(troops_list=tower_left)
            lose_troops = march_left.get_troops_list()
        else:
            march.set_troops_list(march_left)
            march.occupied_tower(tower)
            lose_troops = tower_left.get_troops_list()
        # 失败军队回家
        lose_march_list = []
        for troop in lose_troops:
            lose_march_list.append(
                SingleMarch(
                    start_cord=tower.get_cord(),
                    target_cord=hive_dict[troop.get_hive_id()].get_cord(),
                    hive_id=troop.get_hive_id(),
                    type=March.TYPE_BACK,
                    troops_num=troop.get_troops_num(),
                    target_type=March.TARGET_TYPE_HIVE,
                    target_id=troop.get_hive_id()
                )
            )
        return lose_march_list, battle_report

def attack_hive(hive: Hive, march:March, hive_dict: Dict[str, Hive]):
    is_hive_win, hive_left, march_left, battle_report = \
        battle(hive.get_hive_troops_list(),
               march.get_troops_list(),
               hive.get_buff(),
               hive_dict[march.get_hive_id()].get_buff(),
               march)

    if is_hive_win:
        hive.set_troops_num(troops_list=hive_left)
        lose_troops = march_left.get_troops_list()
    else:
        march.set_troops_list(march_left)
        lose_troops = hive_left.get_troops_list()
    lose_march_list = []
    for troops in lose_troops:
        lose_march_list.append(
            SingleMarch(
                start_cord=hive.get_cord(),
                target_cord=hive_dict[troops.get_hive_id()].get_cord(),
                hive_id=troops.get_hive_id(),
                type=March.TYPE_BACK,
                troops_num=troops.get_troops_num(),
                target_type=March.TARGET_TYPE_HIVE,
                target_id=troops.get_hive_id()
            )
        )
    return lose_march_list, battle_report
