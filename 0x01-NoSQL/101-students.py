#!/usr/bin/env python3
"""
function that returns all students sorted by average score
"""


def top_students(mongo_collection):
    """Return all students sorted by average score"""
    # Use the aggregate method with a pipeline of stages
    pipeline = [
        {"$unwind": "$topics"},
        {"$group": {
            "_id": "$name",
            "averageScore": {"$avg": "$topics.score"}
        }},
        {"$sort": {"averageScore": -1}}
    ]
    cursor = mongo_collection.aggregate(pipeline)
    # Initialize an empty list
    docs = []
    # Iterate over the cursor and append each document to the list
    for doc in cursor:
        docs.append(doc)
    # Return the list of documents
    return docs
