#!/usr/bin/env python

import re
import string
from random import choice

from flask import redirect

from src.blacklist import Blacklist
from src.responses import CommonResponses


class PathManager():
    """
    Class to generate paths for links and add them to database
    """

    def __init__(self, database_object):
        self._db = database_object
        self._common_responses = CommonResponses()

    def _path_gen(self) -> str:
        return ''.join(choice(string.ascii_uppercase + string.ascii_lowercase
                              + string.digits) for i in range(6))

    def _link_check(self, link: str) -> str:
        # Regex for this '^http*.\:\/\/'
        regex_check = re.compile(r'^http*.\:\/\/')
        if not regex_check.match(link):
            return 'http://'+link
        return link

    def path_add(self, link: str) -> str:
        """
        Checks and adds the path
        """
        while True:
            path = self._path_gen()
            if self._db.check_entry(path) is False:
                self._db.add_path(path=path, link=link)
                return path
            continue

    def fetch(self, path: str) -> str:
        """
        Fetch the link for path
        @params:
        path - the (currently) 6 character long string to represent the
                shortlink
        """
        # status_code = 200
        # This if statement validates that the path is of proper length then
        # proceed with search, or else yeet it
        if len(path) != 6:
            return self._common_responses.type('403')
        blacklist_responses = Blacklist().hole(path)
        if blacklist_responses:
            return blacklist_responses
        stat, link = self._db.fetch_link(path)
        if stat is True:
            return redirect(self._link_check(link), 302)
        return self._common_responses.type('404')
