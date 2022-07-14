#!/usr/bin/env python

class DatabaseManager():

    """
    Takes the database details and returns the database object
    """
    def getDatabase(ctx, db_details):
        if (db_details['dbType'] == 'sqlite'):
            from lib.db.sqlite3db import SQLite3DB
            return SQLite3DB(db_details['dbLoc'])
        elif (db_details['dbType'] == 'postgresql'):
            from lib.db.postgresdb import PostgresDB
            return PostgresDB(db_details['dbName'], db_details['username'],
                              db_details['password'], db_details['host'],
                              db_details['port'])
