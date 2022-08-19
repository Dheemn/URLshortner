#!/usr/bin/env python3

from lib.responses import CommonResponses


# This gives the list of blacklisted paths(temporary just to get the
# app working)
class Blacklist():

    def __init__(self):
        self._blacklist = [
                "/favicon.ico",
                ]
        self._common_response = CommonResponses()

    def hole(self, path: str):
        path = "/" + path
        for i in self._blacklist:
            if i == path:
                return self._common_response.type('403')
        return None
