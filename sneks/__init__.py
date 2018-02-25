from gym.envs.registration import register

register(
    id='snek-v1',
    entry_point='sneks.envs:SingleSnek',
)

register(
    id='snek-rgb-v1',
    entry_point='sneks.envs:SingleSnek',
    kwargs = {
        'obs_type' : 'rgb'
    }
)

register(
    id='babysnek-v1',
    entry_point='sneks.envs:SingleBabySnek',
)
