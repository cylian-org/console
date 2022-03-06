import glob
import os
import sys
import yaml

from console import CONSOLE_SYSTEM_BASE

###
### Constants
###

DOT_SEPARATOR = '.'

ENVIRONMENT_SEPARATOR = '__'
ENVIRONMENT_PREFIX = 'CONSOLE' + ENVIRONMENT_SEPARATOR

_config = {}

###
### Helpers
###

def _merge(a, b, path=None):
    """Merges b into a"""
    if path is None:
        path = []
    for key in b:
        if key in a and isinstance(a[key], dict) and isinstance(b[key], dict):
            _merge(a[key], b[key], path + [str(key)])
        else:
            a[key] = b[key]
    return a

###
### Init config
###

def init():
    """Init config module"""

    ### Load environment variables
    for (k,v) in os.environ.items():
        if k.startswith(ENVIRONMENT_PREFIX):
            set(k[len(ENVIRONMENT_PREFIX):].lower().replace(ENVIRONMENT_SEPARATOR,DOT_SEPARATOR), v)

    ### Load console config files
    for file in glob.glob(os.path.join(CONSOLE_SYSTEM_BASE,'config', '*.yaml')):
        load(file)

    ### Load default config files
    for file in glob.glob(os.path.join('config', '*.yaml')):
        load(file)

    ### Load environment specific config files
    for file in glob.glob(os.path.join('config', getOrElse('env', 'default'), '*.yaml')):
        load(file)

###
### Set config data
###

def set(key, value):
    keys = key.split(DOT_SEPARATOR)

    # Init pointer
    _pointer = _config

    # Walk through data - Create dict if required
    if len(keys) > 1:
        for k in keys[:-1]:
            if not k in _pointer:
                _pointer[k] = {}
            _pointer = _pointer[k]
    
    # Update value
    _pointer[ keys[-1] ] = value

def load(file):
    global _config

    # Load Yaml config
    with open(file, 'r') as handler:
        data = yaml.safe_load(handler)

    # Merge data
    _config = _merge(_config, data)

###
### Get config data
###

def get(key):
    _result = _config

    # Walk through data
    for k in key.split(DOT_SEPARATOR):
        _result = _result[k]

    # Completed
    return _result

def getOrElse(key, otherwise=None):
    try:
        return get(key)
    except KeyError:
        return otherwise

###
### Debug
###

def dump():
    print(yaml.dump(_config))
