#!/usr/bin/env python

import datetime
import psycopg2

class DatabaseManager():

    def __init__(self, database, username, password):
        """
        Connects to the database at the start of the class and makes it easy
        all unknown reasons.
        """
        try:
            self._conn = psycopg2.connect(
                    database = database,
                    user = username,
                    password = password)
        except:
            print("Error: Unable to connect to database")
        #pass

    #Just to check if path exists
    def check_entry(self, path):
        cur = self._conn.cursor()
        cur.execute("SELECT * FROM test_shortner WHERE path=%s", (path, ))
        if not cur.fetchone():
            cur.close()
            return False
        else:
            cur.close()
            return True
    
    #Adds path, link to the database
    def add_path(self, path, link):
        try:
            cur = self._conn.cursor()
            dt = datetime.datetime.now()
            cur.execute("INSERT INTO test_shortner (time, path, link) VALUES(%s,%s,%s)", (dt, path, link))
            self._conn.commit()
            cur.close()
            return True
        except:
            self._conn.rollback()
            cur.close()
            print('Error: Failed to write data to table')

    #Returns link for a this path
    def fetch_link(self, path):
        """
        Fetches the link for a particular path
        """
        try:
            cur = self._conn.cursor()
            cur.execute("SELECT link FROM test_shortner WHERE path=%s", (path, ))
            link = cur.fetchone()[0]
            cur.close()
            return True, link
        except TypeError:
            cur.close()
            return False, ''
        except:
            self._conn.rollback()
            cur.close()
            print("Error: Error getting data from database")

    #Automatically delete the conn variable
    def __del__(self):
        self._conn.close()
