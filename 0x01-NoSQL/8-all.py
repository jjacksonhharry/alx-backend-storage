#!/usr/bin/env python3
"""
function that lists all documents in a collection
"""

def list_all(mongo_collection):
    """lists all documents in a collection"""
    all_documents = []

    for document in mongo_collection.find():
        all_documents.append(document)

    return all_documents
