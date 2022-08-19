#!/usr/bin/env python

import datetime
from typing import Optional, Tuple
import psycopg2


class PostgresDB():

    def __init__(
            self,
            database: str,
            username: str,
            password: str,
            *,
            host: Optional[str]='localhost',
            port: Optional[str]='5432',
    ) -> object:
        """
        Connects to the database at the start of the class and makes it easy
        all unknown reasons.
        """
        try:
            self._conn = psycopg2.connect(
                    database=database,
                    user=username,
                    password=password,
                    host=host,
                    port=port)
        except psycopg2.OperationalError:
            print("Error: Unable to connect to database")
        # pass

    # Just to check if path exists
    def check_entry(self, path: str) -> bool:
        cur = self._conn.cursor()
        cur.execute(f"SELECT * FROM urlshortner WHERE path={path}")
        if not cur.fetchone():
            cur.close()
            return False
        cur.close()
        return True

    # Adds path, link to the database
    def add_path(
        self,
        path: str,
        link: str
    ) -> bool:
        try:
            cur = self._conn.cursor()
            date = datetime.datetime.now()
            cur.execute("INSERT INTO urlshortner (time, path, link) " +
                        f"VALUES({date},{path},{link})")
            self._conn.commit()
            cur.close()
            return True
        except psycopg2.Error:
            self._conn.rollback()
            cur.close()
            print('Error: Failed to write data to table')
            return False, ''

    # Returns link for a this path
    def fetch_link(self, path: str) -> Tuple[bool, str]:
        """
        Fetches the link for a particular path
        """
        try:
            cur = self._conn.cursor()
            cur.execute(f"SELECT link FROM urlshortner WHERE path={path}")
            link = cur.fetchone()[0]
            cur.close()
            return True, link
        except TypeError:
            cur.close()
            return False, ''
        except psycopg2.Error:
            self._conn.rollback()
            cur.close()
            print("Error: Error getting data from database")
            return False, ''

    # Automatically delete the conn variable
    def __del__(self) -> None:
        if 'self._conn' in locals():
            self._conn.close()
