from gym.envs.registration import register

register(
    id='ava-v1',
    entry_point='gym_foo.envs:AvaEnv',
)