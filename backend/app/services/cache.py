import json
import logging
from typing import Optional, Any
from redis import Redis
from redis.exceptions import RedisError
from ..core.config import settings

logger = logging.getLogger(__name__)

# Redis client instance (will be initialized if Redis is enabled)
redis_client: Optional[Redis] = None


def get_redis_client() -> Optional[Redis]:
    """
    Get or create Redis client connection.

    Returns:
        Redis client if enabled and connected, None otherwise
    """
    global redis_client

    if not settings.REDIS_ENABLED:
        return None

    if redis_client is None:
        try:
            redis_client = Redis.from_url(
                settings.REDIS_URL,
                decode_responses=True,
                socket_connect_timeout=5,
                socket_timeout=5
            )
            # Test connection
            redis_client.ping()
            logger.info("Redis connection established")
        except RedisError as e:
            logger.error(f"Failed to connect to Redis: {e}")
            redis_client = None

    return redis_client


def close_redis_connection():
    """Close Redis connection if it exists."""
    global redis_client
    if redis_client:
        redis_client.close()
        redis_client = None
        logger.info("Redis connection closed")


async def get_cached(key: str) -> Optional[Any]:
    """
    Get value from cache.

    Args:
        key: Cache key

    Returns:
        Cached value if exists, None otherwise
    """
    client = get_redis_client()
    if not client:
        return None

    try:
        value = client.get(key)
        if value:
            return json.loads(value)
        return None
    except RedisError as e:
        logger.error(f"Redis GET error for key {key}: {e}")
        return None
    except json.JSONDecodeError as e:
        logger.error(f"Failed to decode cached value for key {key}: {e}")
        return None


async def set_cached(key: str, value: Any, ttl: Optional[int] = None) -> bool:
    """
    Set value in cache.

    Args:
        key: Cache key
        value: Value to cache (will be JSON serialized)
        ttl: Time to live in seconds (uses default from settings if not provided)

    Returns:
        True if successful, False otherwise
    """
    client = get_redis_client()
    if not client:
        return False

    try:
        serialized = json.dumps(value)
        ttl_seconds = ttl if ttl is not None else settings.CACHE_TTL_SECONDS
        client.setex(key, ttl_seconds, serialized)
        return True
    except (RedisError, TypeError, ValueError) as e:
        logger.error(f"Redis SET error for key {key}: {e}")
        return False


async def delete_cached(key: str) -> bool:
    """
    Delete value from cache.

    Args:
        key: Cache key

    Returns:
        True if successful, False otherwise
    """
    client = get_redis_client()
    if not client:
        return False

    try:
        client.delete(key)
        return True
    except RedisError as e:
        logger.error(f"Redis DELETE error for key {key}: {e}")
        return False


async def delete_pattern(pattern: str) -> bool:
    """
    Delete all keys matching a pattern.

    Args:
        pattern: Pattern to match (e.g., "user:*")

    Returns:
        True if successful, False otherwise
    """
    client = get_redis_client()
    if not client:
        return False

    try:
        keys = client.keys(pattern)
        if keys:
            client.delete(*keys)
        return True
    except RedisError as e:
        logger.error(f"Redis DELETE pattern error for {pattern}: {e}")
        return False


def cache_key_for_user_tasks(user_id: int, filters: dict) -> str:
    """
    Generate cache key for user tasks with filters.

    Args:
        user_id: User ID
        filters: Dictionary of filters applied

    Returns:
        Cache key string
    """
    # Sort filters to ensure consistent key generation
    sorted_filters = sorted(filters.items())
    filter_str = "_".join(f"{k}:{v}" for k, v in sorted_filters if v is not None)
    return f"tasks:user:{user_id}:{filter_str}" if filter_str else f"tasks:user:{user_id}:all"


async def invalidate_user_tasks_cache(user_id: int) -> bool:
    """
    Invalidate all cached task queries for a user.

    Args:
        user_id: User ID

    Returns:
        True if successful, False otherwise
    """
    return await delete_pattern(f"tasks:user:{user_id}:*")
