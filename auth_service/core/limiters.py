from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from core.settings import settings

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=[settings.limiter_config],
    storage_uri="memory://",
)
