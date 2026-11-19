import redis
import json
import logging
from typing import Optional, Any
from app.core.config import settings

logger = logging.getLogger("aethera.cache")

class RedisCache:
    def __init__(self):
        self.client = None
        self.is_active = False
        
        # Resolve Redis connection endpoint
        redis_url = settings.REDIS_URL or f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/0"
        
        try:
            self.client = redis.from_url(redis_url, socket_timeout=1.0)
            self.client.ping()
            self.is_active = True
            logger.info("Successfully connected to Redis cache.")
        except Exception as e:
            logger.warning(f"Redis cache connection failed: {e}. Running in pass-through (no-cache) mode.")
            self.client = None
            self.is_active = False

    def get(self, key: str) -> Optional[Any]:
        if not self.is_active or not self.client:
            return None
        try:
            val = self.client.get(key)
            if val:
                return json.loads(val)
        except Exception as e:
            logger.error(f"Redis get error: {e}")
        return None

    def set(self, key: str, value: Any, expire: int = 3600) -> bool:
        if not self.is_active or not self.client:
            return False
        try:
            self.client.setex(key, expire, json.dumps(value))
            return True
        except Exception as e:
            logger.error(f"Redis set error: {e}")
        return False

    def delete(self, key: str) -> bool:
        if not self.is_active or not self.client:
            return False
        try:
            self.client.delete(key)
            return True
        except Exception as e:
            logger.error(f"Redis delete error: {e}")
        return False

cache_manager = RedisCache()
