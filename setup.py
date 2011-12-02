from __future__ import with_statement
import os
import os.path
import re

PKG = "django_settings_yaml"
VERSION_PY = os.path.join(PKG, "version.py")
VERSION_TEMPLATE = """# This file is generated from information obtained via git describe 
# Distribution tarballs contain a pre-generated copy of this file.

__version__ = '%s'
"""

try:
    from ez_setup import use_setuptools
except ImportError:
    pass
else:
    use_setuptools(download_delay=0)

from setuptools import setup, find_packages, Command
from setuptools.command.sdist import _sdist

rel_file = lambda *args: os.path.join(os.path.dirname(os.path.abspath(__file__)), *args)

def get_readme():
    return open(rel_file('README')).read()

def get_requirements():
    data = open(rel_file('pipfile')).read()
    lines = map(lambda s: s.strip(), data.splitlines())
    return filter(None, lines)

def git_describe():
    try:
        import subprocess
        p = subprocess.Popen(["git", "describe", "--dirty", "--always"],
                             stdout=subprocess.PIPE)
        result = p.communicate()[0].strip()
        if p.returncode == 0:
            return result.strip()
    except EnvironmentError:
        pass
    return None

def read_version_from_version_module():
    try:
        with open(VERSION_PY) as f:
            for line in f.readlines():
                mo = re.match("__version__ = '([^']+)'", line)
                if mo:
                    return mo.group(1)
    except IOError:
        pass
    return "dev"

if os.path.isdir(".git"):
    version = git_describe()
    if version:
        with open(VERSION_PY, "w") as v:
            v.write(VERSION_TEMPLATE % version)

setup_options = dict(
    name              = PKG,
    version           = read_version_from_version_module(),
    author            = "Kyle Gibson",
    author_email      = "kyle.gibson@frozenonline.com",
    description       = "Load django settings from YAML",
    license           = "MIT",
    url               = "http://github.com/kylegibson/django_settings_yaml",
    packages          = find_packages(),
    long_description  = get_readme(),
    install_requires  = get_requirements(),
    classifiers       = [
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
		"Operating System :: Unix",
		"Programming Language :: Python",
		"Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
    ],
    zip_safe=False,
)

setup(**setup_options)
