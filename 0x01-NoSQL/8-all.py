#!/usr/bin/env python3
"""
 function that lists all documents in a collection
"""


def list_all(mongo_collection):
    """List all documents in a collection"""
    # Initialize an empty list
    docs = []
    # Use the find method with an empty filter
    cursor = mongo_collection.find({})
    # Iterate over the cursor and append each document to the list
    for doc in cursor:
        docs.append(doc)
    # Return the list of documents
    return docs
