#!/usr/bin/env python3
"""
Provides some stats about Nginx logs stored in MongoDB
"""

from pymongo import MongoClient


def log_stats(mongo_collection):
    """Displays some stats about Nginx logs in MongoDB"""

    # Total number of logs
    total_logs = mongo_collection.count_documents({})

    print("{} logs".format(total_logs))

    # Methods
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    for method in methods:
        count = mongo_collection.count_documents({"method": method})
        print("\tmethod {}: {}".format(method, count))

    # Number of logs with method=GET and path=/status
    status_check = nginx_collection.count_documents(
        {"method": "GET", "path": "/status"}
    )
    print("{} status check".format(sts))
