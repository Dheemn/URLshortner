#!/usr/bin/env python

class DatabaseManager():

    #Class that returns the database object according to the type of database used

    def getDatabase(db_details):
        if ( db_details['dbType'] == 'default' ):
            from lib.db.sqlite3db import SQLite3DB
            return SQLite3DB(db_details['dbLoc'])
        elif (db_details['dbType'] == 'postgresql'):
            from lib.db.postgresdb import PostgresDB
            return PostgresDB(db_details['dbName'], db_details['username'], db_details['password'])
