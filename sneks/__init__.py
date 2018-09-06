from gym.envs.registration import register

register(
    id='snek-v1',
    entry_point='sneks.envs:SingleSnek',
    kwargs = {
        'obs_type' : 'raw'
    }
)

register(
    id='snek-rgb-v1',
    entry_point='sneks.envs:SingleSnek',
    kwargs = {
        'obs_type' : 'rgb'
    }
)

register(
    id='snek-layered-v1',
    entry_point='sneks.envs:SingleSnek',
    kwargs = {
        'obs_type' : 'layered'
    }
)

register(
    id='snek-rgb-zoom5-v1',
    entry_point='sneks.envs:SingleSnek',
    kwargs = {
        'obs_type' : 'rgb',
        'obs_zoom': 5
    }
)

register(
    id='babysnek-v1',
    entry_point='sneks.envs:SingleSnek',
    kwargs = {
        'die_on_eat' : True
    }
)

register(
    id='hungrysnek-v1',
    entry_point='sneks.envs:SingleSnek',
    kwargs = {
        'dynamic_step_limit': 100
    }
)
