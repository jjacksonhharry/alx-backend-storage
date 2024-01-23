#!/usr/bin/env python3
"""
Returns the list of schools having a specific topic
"""


def schools_by_topic(mongo_collection, topic):
    """Get the list of schools having a specific topic"""
    # Use the find method with a filter based on the topic
    schools = list(mongo_collection.find({"topics": topic}))
    return schools
