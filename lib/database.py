#!/usr/bin/env python

from lib.db.postgresdb import PostgresDB
from lib.db.sqlite3db import SQLite3DB


def get_database(db_details) -> object:
    """
    Takes the database details and returns the database object
    """
    if db_details["dbType"] == "sqlite":
        return SQLite3DB(db_details["dbLoc"])
    elif db_details["dbType"] == "postgresql":
        return PostgresDB(
            db_details["dbName"],
            db_details["username"],
            db_details["password"],
            db_details["host"],
            db_details["port"],
        )
