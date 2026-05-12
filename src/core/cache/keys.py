from dataclasses import dataclass


@dataclass
class CacheKeys:
    ratelimit = "limit:ip"
    email_verification_code = "email_verification_code"


@dataclass
class BrokerKeys:
    """celery broker"""


cache_keys = CacheKeys()
broker_keys = BrokerKeys()
