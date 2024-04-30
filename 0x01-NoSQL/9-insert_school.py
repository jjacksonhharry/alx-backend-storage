#!/usr/bin/env python3
"""
function that inserts a new document in a collection
"""

def insert_school(mongo_collection, **kwargs):
    """
    inserts a new document in a collection
    """
    return mongo_collection.insert(kwargs)
