from dataclasses import dataclass


@dataclass
class CacheKeys:
    ratelimit = "limit:ip"


@dataclass
class BrokerKeys:
    """celery broker"""

    pass


cache_keys = CacheKeys()
broker_keys = BrokerKeys()
