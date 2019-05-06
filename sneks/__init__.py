from gym.envs.registration import register
import itertools

VERSION = '-v1'

# ========= SETTINGS =========
# Settings include all possible combinations of environments.
# Expressed as a dictionary of lists, in each list there is a tuple
# (label, values) where values are aggregated together to get the final
# args passed to the environment.
# ============================
SETTINGS = {
    'ENV_TYPE': [
        ('snek', {}),
        ('hungrysnek', {'dynamic_step_limit': 100}),
        ('babysnek', {'die_on_eat' : True})
    ],
    'SIZES': [
        ('-16', {'size': (16, 16)}),
        ('-32', {'size': (32, 32)}),
        ('-64', {'size': (64, 64)}),
    ],
    'OBSERVATION_TYPES': [
        ('-raw', {'obs_type': 'raw', 'obs_zoom': 1}),
        ('-rgb', {'obs_type': 'rgb', 'obs_zoom': 1}),
        ('-rgb5', {'obs_type': 'rgb', 'obs_zoom': 5}),
    ],
    'WALLS': [
        ('', {'add_walls': True}),
        ('-NoWalls', {'add_walls': False})
    ]
}
# Settings key, also fix the order of options
SETTINGS_KEY = ['ENV_TYPE', 'OBSERVATION_TYPES', 'SIZES', 'WALLS']

for setting_index in itertools.product(*[range(len(SETTINGS[key])) for key in SETTINGS_KEY]):
    # Get the setting
    env_id = ''
    setting = {}
    for i, key in enumerate(SETTINGS_KEY):
        # Get the label and settings dict
        label, value = SETTINGS[key][setting_index[i]]
        # Add to label
        env_id += label
        # Add to settings dict
        setting = {**setting, **value}
    # Add version to id
    env_id += VERSION
    # Register the environment
    register(
        id=env_id,
        entry_point='sneks.envs:SingleSnek',
        kwargs = setting
    )
