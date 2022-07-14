#!/usr/bin/env python

from lib.blacklist import Blacklist
# from lib.database import DatabaseManager
from lib.responses import CommonResponses
from random import choice
from flask import redirect

import re
import string


class PathManager():
    """
    Class to generate paths for links and add them to database
    """

    def __init__(self, db):
        self._db = db
        self._commonR = CommonResponses()

    def _pathGen(self):
        return ''.join(choice(string.ascii_uppercase + string.ascii_lowercase
                              + string.digits) for i in range(6))

    def _link_check(self, link):
        # Regex for this '^http*.\:\/\/'
        p = re.compile('^http*.\:\/\/')
        if not p.match(link):
            return 'http://'+link
        return link

    def pathAdd(self, link):
        """
        Checks and adds the path
        """
        while(True):
            path = self._pathGen()
            if (self._db.check_entry(path) is False):
                self._db.add_path(path=path, link=link)
                return path
            else:
                continue

    def fetch(self, path):
        """
        Fetch the link for path
        """
        # status_code = 200
        # This if statement validates that the path is of proper length
        if(len(path) != 6):
            return self._commonR.type('403')
        bResponse = Blacklist().hole(path)
        if bResponse:
            return bResponse
        stat, link = self._db.fetch_link(path)
        if (stat is True):
            return redirect(self._link_check(link), 302)
        else:
            return self._commonR.type('404')
