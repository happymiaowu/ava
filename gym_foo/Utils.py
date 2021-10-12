from gym_foo.model.battlefield_detail import BattleField
import hashlib


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





