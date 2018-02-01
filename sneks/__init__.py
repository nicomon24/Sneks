from gym.envs.registration import register

register(
    id='snek-v1',
    entry_point='sneks.envs:SingleSnek',
)
