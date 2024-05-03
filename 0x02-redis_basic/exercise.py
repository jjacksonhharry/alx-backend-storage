#!/usr/bin/env python3
"""
Redis for caching, and the decorators count_calls
and call_historyfor tracking the usage and
history of function calls.
"""

import redis
from uuid import uuid4
from typing import Union, Callable, Optional
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """
    Decorator to count the number of times a method is called.

    Args:
        method (Callable): The method to be decorated.

    Returns:
        Callable: The decorated method.
    """
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Wrapper function for the decorated method."""
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    """
    Decorator to store the history of inputs and outputs of a method.

    Args:
        method (Callable): The method to be decorated.

    Returns:
        Callable: The decorated method.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Wrapper function for the decorated method."""
        input_str = str(args)
        self._redis.rpush(method.__qualname__ + ":inputs", input_str)
        output_str = str(method(self, *args, **kwargs))
        self._redis.rpush(method.__qualname__ + ":outputs", output_str)
        return output_str

    return wrapper


def replay(fn: Callable):
    """
    Function to display the history of calls of a particular function.

    Args:
        fn (Callable): The function whose call history is to be displayed.
    """
    r = redis.Redis()
    function_name = fn.__qualname__
    value = r.get(function_name)
    try:
        value = int(value.decode("utf-8"))
    except Exception:
        value = 0

    print("{} was called {} times:".format(function_name, value))
    inputs = r.lrange("{}:inputs".format(function_name), 0, -1)
    outputs = r.lrange("{}:outputs".format(function_name), 0, -1)

    for input, output in zip(inputs, outputs):
        try:
            input = input.decode("utf-8")
        except Exception:
            input = ""

        try:
            output = output.decode("utf-8")
        except Exception:
            output = ""

        print("{}(*{}) -> {}".format(function_name, input, output))


class Cache:
    """
    Cache class for storing data using Redis.

    Attributes:
        _redis (redis.Redis): Instance of the Redis client.
    """

    def __init__(self):
        """
        Initialize the Cache instance with a Redis client and
        flush the Redis database.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store data in the cache and return a randomly generated key.

        Args:
            data (Union[str, bytes, int, float]): The data to be
            stored in the cache.

        Returns:
            str: The randomly generated key used to store the
            data in the cache.
        """
        random_key = str(uuid4())
        self._redis.set(random_key, data)
        return random_key

    def get(self, key: str,
            fn: Optional[Callable] = None) -> Union[str, bytes, int, float]:
        """
        Retrieve data from the cache using the provided key.

        Args:
            key (str): The key used to retrieve the data from the cache.
            fn (Optional[Callable]): An optional function to convert
            the retrieved data. Defaults to None.

        Returns:
            Union[str, bytes, int, float]: The retrieved data from the cache.
        """
        value = self._redis.get(key)
        if fn:
            value = fn(value)
        return value

    def get_str(self, key: str) -> str:
        """
        Retrieve a string value from the cache using the provided key.

        Args:
            key (str): The key used to retrieve the string value
            from the cache.

        Returns:
            str: The string value retrieved from the cache.
        """
        value = self._redis.get(key)
        return value.decode("utf-8")

    def get_int(self, key: str) -> int:
        """
        Retrieve an integer value from the cache using the provided key.

        Args:
            key (str): The key used to retrieve the integer
            value from the cache.

        Returns:
            int: The integer value retrieved from the cache.
        """
        value = self._redis.get(key)
        try:
            value = int(value.decode("utf-8"))
        except Exception:
            value = 0
        return value
