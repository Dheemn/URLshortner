#!/usr/bin/env python3

import datetime
import sqlite3


class SQLite3DB():
    """
    This class contains the methods for communication between the SQLite
    database
    @params:
        db_path: string - path to the SQLite database file
    """
    def __init__(self, db_path):
        try:
            self._conn = sqlite3.connect(db_path, check_same_thread=False)
        except:
            print("Error: Unable to connect to SQLite3 database")
            exit()

    # Check's if the path exists
    def check_entry(self, path):
        """
        Checks if the shortlink already exists in the database
        @params:
            path: string - the path to be searched
                            (not to be confused with an URL)
        """
        cur = self._conn.cursor()
        cur.execute("SELECT * FROM urlshortner WHERE path=(?)", (path, ))
        if not cur.fetchone():
            cur.close()
            return False
        else:
            cur.close()
            return True

    # Adds path, link to the database
    def add_path(self, path, link):
        """
        This method adds the path, link(URL) to the database
        @params:
            path: string - the n-character long string to 
        """
        try:
            cur = self._conn.cursor()
            dt = datetime.datetime.now()
            cur.execute("INSERT INTO urlshortner (time, path, link) VALUES(?,?,?)",
                            (dt, path, link))
            self._conn.commit()
            cur.close()
            return True
        except:
            self._conn.rollback()
            cur.close()
            print('Error: Failed to write data to table')

    # Returns link for a this path
    def fetch_link(self, path):
        """
        Fetches the link for a particular path
        """
        try:
            cur = self._conn.cursor()
            cur.execute("SELECT link FROM urlshortner WHERE path=(?)",
                            (path, ))
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

    # Closes the connection
    def __del__(self):
        print('Closing conn connection')
        self._conn.close()
        
