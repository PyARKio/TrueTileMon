# -- coding: utf-8 --
from __future__ import unicode_literals
import subprocess


__author__ = 'PyARK'
__version__ = "1.0.1"
__email__ = "fedoretss@gmail.com"
__status__ = "Production"

_check_pipenv = 'pipenv'
_check_pip3 = 'pip3'
_check_python_version = 'python -V'
_install_pipenv = 'pip install pipenv'
_deploy_env = 'pipenv install'
_get_path_to_env = 'pipenv --venv'
_get_path_to_project = 'pipenv --where'


def send_to_cmd(_cmd):
    _out = None
    _err = None
    proc = subprocess.Popen(_cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    out, err = proc.communicate()
    # print(out)
    # print(err)
    if out or out == b'':
        _out = out.decode()
        # print(_out)
    if err:
        _err = err.decode()
        # print(_err)
    return _out, _err


# ----  The presence of the PipEnv is being checked  ----
print('Setup.py - The presence of the PipEnv is being checked...')
out, err = send_to_cmd(_check_pipenv)
if out or out == '':
    if out == '':
        print('Setup.py - Installing pipenv...')
        out, err = send_to_cmd(_install_pipenv)
    else:
        print('Setup.py - PipEnv is already exist')


# ----  Deploying environment  ----
print('Setup.py - Deploying environment...')
out, err = send_to_cmd(_get_path_to_env)
if out or out == '':
    if out == '':
        out, err = send_to_cmd(_deploy_env)
    else:
        print('Setup.py - The environment was already deployed')


# ----  Finding path to Pip Environment and Project  ----
print('Setup.py - Finding path to Pip Environment and Project...')
out, err = send_to_cmd(_get_path_to_env)
path_to_env = '"{}/Scripts/python.exe"'.format(out.split('\r\r\n')[0])

out, err = send_to_cmd(_get_path_to_project)
path_to_project = '"{}/Runner.py"'.format(out.split('\r\r\n')[0])
_title = out.split('\r\r\n')[0].split('\\')[-1]


# ----  Create {}.bat file  ----
print('Setup.py - Create {}.bat file...'.format(_title))
_bat = open('{}.bat'.format(_title), 'w')
_bat.write('@echo off\nTITLE {}\nCOLOR 0a\r\n'.format(_title))
_bat.write('{} {}'.format(path_to_env, path_to_project))
_bat.write('\r\npause\n')
_bat.close()
