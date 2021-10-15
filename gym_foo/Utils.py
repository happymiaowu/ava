from gym_foo.model.battlefield_detail import BattleField
from gym_foo.model.hive import Hive
import hashlib
from gym_foo.model.march import March

def get_status_rewards_from_detail(detail: BattleField):
    self_score = detail.get_self_score()
    opp_score = detail.get_opp_score()
    rewards = int(self_score) - int(opp_score)
    a = ','.join([str(x) for x in detail.get_self_marches()])
    b = ','.join([str(x) for x in detail.get_opp_marches()])
    c = ','.join([str(x) for x in detail.get_towers()])
    d = ','.join([str(x) for x in detail.get_opp_hives()])
    e = ','.join([str(x) for x in detail.get_self_hives()])
    f = ','.join([str(x) for x in detail.get_self_rallies()])
    g = ','.join([str(x) for x in detail.get_opp_rallies()])
    h = ','.join([str(x) for x in detail.get_scout_reports()])
    all_s = a + b + c + d + e + f + g + h
    hh = hashlib.sha256()
    hh.update(all_s.encode())
    all_hasd = hh.hexdigest()
    return rewards, all_hasd

def can_hive_atk(hive: Hive):
    if hive.get_using_march_num() == hive.get_max_march_num():
        return False
    if hive.get_troops_num() == 0:
        return False
    return True


def get_status_rewards_from_detail_v2(detail: BattleField, self_hive: Hive):
    self_score = detail.get_self_score()
    opp_score = detail.get_opp_score()
    rewards = int(self_score) - int(opp_score)


    march = '%d,%d,%d,%d' % (
        len(list(filter(lambda x: x.get_target_type() == March.TARGET_TYPE_TOWER, detail.get_self_marches()))),
        len(list(filter(lambda x: x.get_target_type() == March.TARGET_TYPE_TOWER and detail.get_towers()[int(x.get_target_id())].is_wonder(), detail.get_self_marches()))),
        len(list(filter(lambda x: x.get_target_type() == March.TARGET_TYPE_HIVE, detail.get_self_marches()))),
        len(list(filter(lambda x: x.get_target_type() == March.TARGET_TYPE_RALLY, detail.get_self_marches())))
    )

    opp_march = '%d,%d,%d,%d' % (
        len(list(filter(lambda x: x.get_target_type() == March.TARGET_TYPE_TOWER, detail.get_opp_marches()))),
        len(list(filter(lambda x: x.get_target_type() == March.TARGET_TYPE_TOWER and detail.get_towers()[int(
            x.get_target_id())].is_wonder(), detail.get_opp_marches()))),
        len(list(filter(lambda x: x.get_target_type() == March.TARGET_TYPE_HIVE, detail.get_opp_marches()))),
        len(list(filter(lambda x: x.get_target_type() == March.TARGET_TYPE_RALLY, detail.get_opp_marches())))
    )

    tower = ','.join(list(map(lambda x: str(x.who_occupied()), detail.get_towers())))

    # self_hive_buff = ','.join(list(map(lambda x: str(x.get_buff()), detail.get_self_hives())))
    self_hive_cord = ','.join(list(map(lambda x: str(x.get_cord()), detail.get_self_hives())))
    # self_hive_can_atk = ','.join(list(map(lambda x: str(can_hive_atk(x)), detail.get_self_hives())))

    self_rally = '%d,%d,%d,%d' % (
        len(list(filter(lambda x: x.get_target_type() == March.TARGET_TYPE_TOWER, detail.get_self_rallies()))),
        len(list(filter(lambda x: x.get_target_type() == March.TARGET_TYPE_TOWER and detail.get_towers()[int(x.get_target_id())].is_wonder(), detail.get_self_rallies()))),
        len(list(filter(lambda x: x.get_target_type() == March.TARGET_TYPE_HIVE, detail.get_self_rallies()))),
        len(list(filter(lambda x: x.get_target_type() == March.TARGET_TYPE_RALLY, detail.get_self_rallies())))
    )

    opp_rally = '%d,%d,%d,%d' % (
        len(list(filter(lambda x: x.get_target_type() == March.TARGET_TYPE_TOWER, detail.get_opp_rallies()))),
        len(list(filter(lambda x: x.get_target_type() == March.TARGET_TYPE_TOWER and detail.get_towers()[int(x.get_target_id())].is_wonder(), detail.get_opp_rallies()))),
        len(list(filter(lambda x: x.get_target_type() == March.TARGET_TYPE_HIVE, detail.get_opp_rallies()))),
        len(list(filter(lambda x: x.get_target_type() == March.TARGET_TYPE_RALLY, detail.get_opp_rallies())))
    )

    hive_str = '%s,%s,%s' % (
        str(self_hive.get_buff()), str(self_hive.get_cord()), str(can_hive_atk(self_hive))
    )


    all_s = ','.join([march,
                      # opp_march,
                      tower,
                      # self_hive_cord,
                      # self_rally,
                      # opp_rally,
                      hive_str,
                      # str(detail.get_round_left()),
                      # str(rewards)
                      ])

    return rewards, all_s




