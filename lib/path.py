#!/usr/bin/env python

from lib.blacklist import Blacklist
from lib.database import DatabaseManager
from lib.responses import CommonResponses
from random import choice
from flask import redirect

import string

class PathManager():
    """
    Class to generate paths for links and add them to database
    """
    
    def __init__(self, db):
        self._db = db
        #self._db = DatabaseManager('urlshortner', 'urlshortner', 'testuser')
        self._commonR = CommonResponses()

    def _pathGen(self):
        return ''.join(choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for i in range(6))

    def pathAdd(self, link):
        """
        Checks and adds the path
        """
        while(True):
            path = self._pathGen()
            if ( self._db.check_entry(path) == False ):
                self._db.add_path(path = path, link = link)
                return path
            else:
                continue

    #Function to restrict length of path to certain characters
    #def _path_len(self, path):
    #    if ( len(path) != 6):
    #        return 403

    def fetch(self, path):
        """
        Fetch the link for path
        """
        status_code = 200
        #This if statement validates that the path is of proper length
        if ( len(path) != 6 ):
            return self._commonR.type('403')
        bResponse = Blacklist().hole(path)
        if bResponse:
            return bResponse
        stat, link = self._db.fetch_link(path)
        if ( stat == True):
            return redirect(link, 302)
        else:
            return self._commonR.type('404')


