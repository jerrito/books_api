import redis.asyncio as redis
from redis.exceptions import ConnectionError as RedisConnectionError
from src.config import SettingsConfig
import logging

logger = logging.getLogger(__name__)

JTI_EXPIRY = 3600

# Create Redis client (lazy connection - won't connect until first use)
_token_blocklist: redis.Redis | None = None

def get_redis_client() -> redis.Redis:
    """Get or create Redis client instance."""
    global _token_blocklist
    if _token_blocklist is None:
        _token_blocklist = redis.Redis(
            host=SettingsConfig.REDIS_HOST,
            port=SettingsConfig.REDIS_PORT,
            db=0,
            decode_responses=False,  # Keep bytes for compatibility
            socket_connect_timeout=2,  # 2 second timeout
            socket_timeout=2,
            retry_on_timeout=True,
            health_check_interval=30
        )
    return _token_blocklist

async def add_jti_to_blocklist(jti: str) -> None:
    """Add JTI to Redis blocklist."""
    try:
        client = get_redis_client()
        await client.set(
            name=jti,
            value="",
            ex=JTI_EXPIRY
        )
    except RedisConnectionError as e:
        logger.warning(f"Redis connection failed, cannot add JTI to blocklist: {e}")
        # Optionally raise or handle silently depending on your requirements
        raise


async def get_jti_in_blocklist(jti: str) -> bool:
    """Check if JTI is in Redis blocklist."""
    try:
        client = get_redis_client()
        result = await client.get(jti)
        return True if result is not None else False
    except RedisConnectionError as e:
        logger.warning(f"Redis connection failed, cannot check JTI blocklist: {e}")
        # If Redis is unavailable, assume token is not blocked (fail open)
        # Change to return True if you want to fail closed (block all tokens when Redis is down)
        return False


