__version__ = "unknown"
try:
    from version import __version__
except ImportError:
    pass

import sys
import yaml
import string
import os

DEFAULT_ENV_PREFIX = "DJANGO_SETTINGS_ENV_"
SECRET_KEY_FILE = "secret_key_file"

def load_yaml_settings(context, files):
    settings = {}
    for p in files:
        with open(p) as fd:
            t = string.Template(fd.read())
            y = yaml.load(t.safe_substitute(context))
            settings.update(y)
    return settings

def read_write_secret_key_file(settings):
    try:
        with open(settings[SECRET_KEY_FILE]) as rfd:
            settings["secret_key"] = rfd.read().strip()
        return settings["secret_key"]
    except IOError:
        try:
            from random import choice
            settings["secret_key"] = ''.join([choice(string.letters + string.digits + string.punctuation) for i in range(50)])
            with open(settings[SECRET_KEY_FILE], "w") as wfd:
                wfd.write(settings["secret_key"])
        except IOError:
            pass

def get_settings_from_env(prefix=None, env=None):
    if not env:
        env = os.environ
    if not prefix:
        prefix = DEFAULT_ENV_PREFIX
    settings = {}
    for key,val in filter(lambda k: k[0].startswith(prefix), env.items()):
        settings[key.replace(prefix, "")] = yaml.load(val)
    return settings

def load(context, files, load_env = True, add_python_path = True):
    for key, val in os.environ.items():
        context["ENV_%s" % key] = val
    settings = load_yaml_settings(context, files)
    if add_python_path and "pythonpath" in settings:
        sys.path.extend([pp for pp in settings["pythonpath"]])
    if load_env:
        settings.update(get_settings_from_env())
    if "secret_key" not in settings and SECRET_KEY_FILE in settings:
        read_write_secret_key_file(settings)
    def upper_keys(d):
        if type(d) is dict:
            return dict((k.upper(), upper_keys(v)) for k, v in d.iteritems())
        return d
    return upper_keys(settings)
