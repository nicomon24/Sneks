from gym.envs.registration import register

register(
    id='snek-v1',
    entry_point='sneks.envs:SingleSnek',
)

register(
    id='babysnek-v1',
    entry_point='sneks.envs:SingleBabySnek',
)
