import pickle

import redis
from models import InvoiceModel

_CACHE_JOIN_KEY = "LARGE-JOIN-KEY"


class CacheService:
    """
    A service to handle caching using Redis.
    """

    def __init__(self, redis_client: redis.Redis):
        self.redis_client = redis_client
        self.redis_client.ping()

    def set_invoice(self, invoice: InvoiceModel, ttl_secs=30):
        """set invoice on cache"""
        self.redis_client.set(
            str(invoice.invoice_id), pickle.dumps(invoice), ex=ttl_secs
        )

    def get_invoice(self, invoide_id: int) -> InvoiceModel | None:
        """get invoice from cache, returns none on cache miss"""
        cached_value = self.redis_client.get(str(invoide_id))
        if cached_value is not None:
            return pickle.loads(cached_value)
        return None

    def set_join(self, val: str, ttl_secs=30):
        """set join on cache"""
        self.redis_client.set(_CACHE_JOIN_KEY, val, ex=ttl_secs)

    def get_join(self) -> str | None:
        """get join from cache, returns none on cache miss"""
        cached_value = self.redis_client.get(_CACHE_JOIN_KEY)
        return cached_value
