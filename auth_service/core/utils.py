import datetime as dt
import secrets
import string

from user_agents import parse
from enum import Enum


class DeviceType(Enum):
    WEB = 'Браузер'
    MOBILE = 'Телефон'
    SMART = 'Смарт-ТВ'


def useragent_device_parser(useragent: str) -> DeviceType | None:
    user_agent = parse(useragent)
    if str(user_agent).find("TV") != -1:
        return DeviceType.SMART
    if user_agent.is_mobile or user_agent.is_tablet:
        return DeviceType.MOBILE
    if user_agent.is_pc:
        return DeviceType.WEB

    return DeviceType.WEB


def get_unix_timedelta(unix_time: str | dt.datetime | int):
    end_timestamp = unix_time
    if isinstance(unix_time, (int, str)):
        end_timestamp = dt.datetime.fromtimestamp(float(unix_time)).timestamp()

    return end_timestamp - dt.datetime.now().timestamp()


def get_random_password():
    alphabet = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(alphabet) for i in range(8))
    return password
