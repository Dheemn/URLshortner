#!/usr/bin/env python3

import datetime
import sqlite3
from typing import Tuple


class SQLite3DB():
    """
    This class contains the methods for communication between the SQLite
    database

    Params:

    db_path: string - path to the SQLite database file
    """
    def __init__(self, db_path: str):
        try:
            self._conn = sqlite3.connect(db_path, check_same_thread=False)
        except sqlite3.Error:
            print("Error: Unable to connect to SQLite3 database")
            exit()

    # Check's if the path exists
    def check_entry(self, path: str) -> bool:
        """
        Checks if the shortlink already exists in the database

        Params:

        path: string - the path to be searched
                            (not to be confused with an URL)
        """
        cur = self._conn.cursor()
        cur.execute(f"SELECT * FROM urlshortner WHERE path='{path}';")
        if not cur.fetchone():
            cur.close()
            return False
        else:
            cur.close()
            return True

    # Adds path, link to the database
    def add_path(
        self,
        path: str,
        link: str
    ) -> bool:
        """
        This method adds the path, link(URL) to the database

        Params:

        path: string - the n-character long string to map to URL
        """
        try:
            cur = self._conn.cursor()
            cur_date_time = datetime.datetime.now()
            cur.execute("INSERT INTO urlshortner (time, path, link) " +
                        f"VALUES('{cur_date_time}','{path}','{link}');")
            self._conn.commit()
            cur.close()
            return True
        except sqlite3.Error as error:
            self._conn.rollback()
            cur.close()
            print(f'Error: Failed to write data to table\n{error}')
            return False

    # Returns link for a this path
    def fetch_link(self, path: str) -> Tuple[bool, str]:
        """
        Fetches the link for a particular path
        """
        try:
            cur = self._conn.cursor()
            cur.execute(f"SELECT link FROM urlshortner WHERE path=('{path}');")
            link = cur.fetchone()[0]
            cur.close()
            return True, link
        except TypeError:
            cur.close()
            return False, ''
        except sqlite3.Error:
            self._conn.rollback()
            cur.close()
            print("Error: Error getting data from database")
            return False, ''

    # Closes the connection
    def __del__(self) -> None:
        print('Closing conn connection')
        self._conn.close()
