#!/usr/bin/env python3
"""
Module with tools for request caching and tracking.
"""
import requests
import redis
from functools import wraps

# Initialize Redis client
redis_client = redis.Redis()


def cache_with_count(expiration: int = 10):
    """
    Caches the output of fetched data.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            url = args[0]
            count_key = f"count:{url}"
            cache_key = f"cache:{url}"

            # Check if the result is already cached
            cached_result = redis_client.get(cache_key)
            if cached_result:
                # Increment access count
                redis_client.incr(count_key)
                return cached_result.decode()

            # If not cached, call the original function
            result = func(*args, **kwargs)

            # Cache the result with expiration time
            redis_client.setex(cache_key, expiration, result)

            # Initialize access count to 1
            redis_client.incr(count_key)

            return result

        return wrapper

    return decorator


@cache_with_count()
def get_page(url: str) -> str:
    """
    Returns the content of a URL
    """
    response = requests.get(url)
    return response.text
