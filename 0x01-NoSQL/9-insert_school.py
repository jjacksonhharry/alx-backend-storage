#!/usr/bin/env python3
"""
Python function that inserts a new document
in a collection based on kwargs
"""


def insert_school(mongo_collection, **kwargs):
    """Insert a new document in a collection based on kwargs"""
    # Use the insert_one method with the kwargs dictionary
    result = mongo_collection.insert_one(kwargs)
    # Return the _id of the inserted document
    return result.inserted_id
