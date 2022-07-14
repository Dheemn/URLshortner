#!/usr/bin/env python3

from lib.responses import CommonResponses


# This gives the list of blacklisted paths(temporary just to get the
# app working)
class Blacklist():

    def __init__(self):
        self._blacklist = [
                "/favicon.ico",
                ]
        self._cR = CommonResponses()

    def hole(self, path):
        path = "/"+path
        for i in self._blacklist:
            if (i == path):
                return self._cR.type('403')
        return None
