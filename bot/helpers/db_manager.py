from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import PyMongoError

from bot import bot_id, bot_loop, users, DATABASE_URL, LOGGER


class DbManager:
    def __init__(self):
        self._err = False
        self._db = None
        self._conn = None
        self._connect()

    def _connect(self):
        if not DATABASE_URL:
            self._err = True
            return
        try:
            self._conn = AsyncIOMotorClient(DATABASE_URL)
            self._db = self._conn.autoapprove
        except PyMongoError as e:
            LOGGER.error('Error in DB connection: %s', e)
            self._err = True

    async def db_load(self):
        if self._err:
            return
        # Users
        if await self._db.users[bot_id].find_one():
            rows = self._db.users[bot_id].find({})
            async for row in rows:
                uid = row['_id']
                del row['_id']
                users[uid] = row
            LOGGER.info('All users has been imported from Database.')

    async def update_users(self, user_id):
        if self._err:
            return
        await self._db.users[bot_id].replace_one({'_id': user_id}, users.get(user_id, {}), upsert=True)

    async def delete_user(self, chat_id: int):
        if users.pop(chat_id, None) and not self._err:
            await self._db.users[bot_id].delete_one({'_id': chat_id})


try:
    bot_loop.create_task(DbManager().db_load())
except Exception as e:
    LOGGER.error(e, exc_info=True)