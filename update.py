from logging import FileHandler, StreamHandler, basicConfig, error as log_error, info as log_info, INFO
from os import path as ospath, environ, remove
from subprocess import run as srun
from sys import exit

from pip._internal.operations.freeze import freeze

if ospath.exists('log.txt'):
    with open('log.txt', 'r+') as f:
        f.truncate(0)

if ospath.exists('rlog.txt'):
    remove('rlog.txt')

basicConfig(format='%(asctime)s: [%(levelname)s: %(filename)s - %(lineno)d] ~ %(message)s',
            handlers=[FileHandler('log.txt'), StreamHandler()],
            datefmt='%d-%b-%y %I:%M:%S %p',
            level=INFO)

if BOT_TOKEN := environ.get('BOT_TOKEN', ''):
    bot_id = BOT_TOKEN.split(':', 1)[0]
else:
    log_error('BOT_TOKEN variable is missing! Exiting now')
    exit(1)

if environ.get('UPDATE_EVERYTHING', 'False').lower() == 'true':
    cmd = ['pip3', 'install', '--no-cache-dir', '--upgrade']
    cmd.extend((package for dist in freeze(local_only=True) if (package := dist.split('==')[0])))
    srun(cmd)

if (UPSTREAM_REPO := environ.get('UPSTREAM_REPO')) and (UPSTREAM_BRANCH := environ.get('UPSTREAM_BRANCH', 'master')):
    if ospath.exists('.git'):
        srun(['rm', '-rf', '.git'])
    update = srun([f'git init -q \
                     && git config --global user.email e.luckm4n@gmail.com \
                     && git config --global user.name R4ndomUsers \
                     && git add . \
                     && git commit -sm update -q \
                     && git remote add origin {UPSTREAM_REPO} \
                     && git fetch origin -q \
                     && git reset --hard origin/{UPSTREAM_BRANCH} -q'], shell=True)
    if update.returncode == 0:
        log_info(f'Successfully updated with latest commit from UPSTREAM_REPO ~ {UPSTREAM_BRANCH.upper()} Branch.')
    else:
        log_error('Something went wrong while updating, check UPSTREAM_REPO if valid or not!')
