from bot import users
from bot.helpers.db_manager import DbManager


def get_readable_time(seconds):
    periods = [('d', 86400), ('h', 3600), ('m', 60), ('s', 1)]
    result = ''
    for period_name, period_seconds in periods:
        if seconds >= period_seconds:
            period_value, seconds = divmod(seconds, period_seconds)
            result += f'{int(period_value)}{period_name} '
    return result.strip()


async def update_users(user_id: int, key: str, value: any):
    users.setdefault(user_id, {})[key] = value
    await DbManager().update_users(user_id)
