#!/usr/bin/env python

from typing import Dict
from lib.db.postgresdb import PostgresDB
from lib.db.sqlite3db import SQLite3DB


def get_database(db_details: Dict[str, str]) -> object:
    """
    Takes the database details and returns the database object
    """
    if db_details["dbType"] == "sqlite":
        return SQLite3DB(db_details["dbLoc"])
    elif db_details["dbType"] == "postgresql":
        return PostgresDB(
            database=db_details["dbName"],
            username=db_details["username"],
            password=db_details["password"],
            host=db_details["host"],
            port=db_details["port"],
        )
