from gym.envs.registration import register

SIZES = [16, 32, 64]
OBSERVATION_TYPES = ['raw', 'rgb', 'rgb5', 'layered']
COMBINATIONS = [(size, obs_type) for size in SIZES for obs_type in OBSERVATION_TYPES]

def get_obs_and_zoom(obs_type):
    if obs_type == 'rgb5':
        return 'rgb', 5
    else:
        return obs_type, 1

# Type: snek
for (size, obs_type) in COMBINATIONS:
    obs, zoom = get_obs_and_zoom(obs_type)
    register(
        id='snek-' + obs_type + '-' + str(size) + '-v1',
        entry_point='sneks.envs:SingleSnek',
        kwargs = {
            'obs_type' : obs,
            'obs_zoom': zoom,
            'size': (size, size)
        }
    )

# Type: babysnek
for (size, obs_type) in COMBINATIONS:
    obs, zoom = get_obs_and_zoom(obs_type)
    register(
        id='babysnek-' + obs_type + '-' + str(size) + '-v1',
        entry_point='sneks.envs:SingleSnek',
        kwargs = {
            'die_on_eat' : True,
            'obs_type' : obs,
            'obs_zoom': zoom,
            'size': (size, size)
        }
    )

# Type: hungysnek
for (size, obs_type) in COMBINATIONS:
    obs, zoom = get_obs_and_zoom(obs_type)
    register(
        id='hungrysnek-' + obs_type + '-' + str(size) + '-v1',
        entry_point='sneks.envs:SingleSnek',
        kwargs = {
            'dynamic_step_limit': 100,
            'obs_type' : obs,
            'obs_zoom': zoom,
            'size': (size, size)
        }
    )
