#!/usr/bin/env python3
"""
get_page function along with caching and
tracking URL access counts using Redis
"""

import requests
import redis
import time
from functools import wraps


def cache_result(func):
    """
    Decorator to cache the result of a function using Redis.

    Args:
        func (Callable): The function to be decorated.

    Returns:
        Callable: The decorated function.
    """
    @wraps(func)
    def wrapper(url):
        """
        Wrapper function for caching the result of the original function.

        Args:
            url (str): The URL to be cached.

        Returns:
            str: The cached result.
        """
        r = redis.Redis()
        cached_result = r.get(url)
        if cached_result:
            return cached_result.decode("utf-8")
        result = func(url)
        r.setex(url, 10, result)
        return result
    return wrapper


@cache_result
def get_page(url: str) -> str:
    """
    Fetches HTML content from a given URL using the requests
    module and caches the result.

    Args:
        url (str): The URL to fetch the HTML content from.

    Returns:
        str: The HTML content of the page.
    """
    r = redis.Redis()
    r.incr("count:" + url)
    response = requests.get(url)
    return response.text
