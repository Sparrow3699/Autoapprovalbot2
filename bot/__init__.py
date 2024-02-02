from logging import getLogger, FileHandler, StreamHandler, basicConfig, INFO, ERROR
from os import environ
from pyrogram import Client, enums
from socket import setdefaulttimeout
from sys import exit
from time import time
from uvloop import install


install()
setdefaulttimeout(600)

basicConfig(format='%(asctime)s: [%(levelname)s: %(filename)s - %(lineno)d] ~ %(message)s',
            handlers=[FileHandler('log.txt'), StreamHandler()],
            datefmt='%d-%b-%y %I:%M:%S %p',
            level=INFO)

getLogger('pyrogram').setLevel(ERROR)

LOGGER = getLogger(__name__)

start_time = time()

users = {}

if not (BOT_TOKEN := environ.get('BOT_TOKEN', '')):
    LOGGER.error('BOT_TOKEN variable is missing! Exiting now')
    exit(1)

bot_id = BOT_TOKEN.split(':', 1)[0]

if OWNER_ID := environ.get('OWNER_ID', ''):
    OWNER_ID = int(OWNER_ID)
else:
    LOGGER.error('OWNER_ID variable is missing! Exiting now')
    exit(1)

if TELEGRAM_API := environ.get('TELEGRAM_API', ''):
    TELEGRAM_API = int(TELEGRAM_API)
else:
    LOGGER.error('TELEGRAM_API variable is missing! Exiting now')
    exit(1)

if not (TELEGRAM_HASH := environ.get('TELEGRAM_HASH', '')):
    LOGGER.error('TELEGRAM_HASH variable is missing! Exiting now')
    exit(1)

SUDO = {int(uid) for uid in environ.get('SUDO', '') if uid.isdigit()}
CHAT_IDS = {int(cid) for cid in environ.get('CHAT_IDS', '') if cid.startswith('-100')}

CMD_BROADCAST = environ.get('CMD_BROADCAST', 'bc')
CMD_LOG = environ.get('CMD_LOG', 'log')
CMD_RESTART = environ.get('CMD_RESTART', 'restart')
CMD_START = environ.get('CMD_START', 'start')
CMD_USERS = environ.get('CMD_USERS', 'users')

APPROVE_MESSAGE_TEXT = environ.get('APPROVE_MESSAGE_TEXT', 'Congratulation, you have been approved to join the channel!')
UPSTREAM_REPO = environ.get('UPSTREAM_REPO', '')
UPSTREAM_BRANCH = environ.get('UPSTREAM_BRANCH', 'master')
UPDATE_EVERYTHING = environ.get('UPDATE_EVERYTHING', 'False').lower() == 'true'

bot: Client = Client('bot', TELEGRAM_API, TELEGRAM_HASH,
                     bot_token=BOT_TOKEN, workers=1000,
                     max_concurrent_transmissions=1000,
                     parse_mode=enums.ParseMode.HTML).start()

bot_loop = bot.loop