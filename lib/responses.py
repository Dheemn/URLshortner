#!/usr/bin/env python3

# from flask import Response


class CommonResponses():

    def __init__(self):
        # self.code = code
        pass

    # Response for 403 forbidden request
    def forbidden(self):
        page = open(
            'static/403.html',
            mode='r',
            encoding='utf-8',
        ).read()
        return page, 403

    # Response for 400 bad request
    def bad_request(self):
        page = open(
            'static/400.html',
            mode='r',
            encoding='utf-8',
        ).read()
        return page, 400

    # Response for 404 not found
    def not_found(self):
        page = open(
            'static/404.html',
            mode='r',
            encoding='utf-8',
        ).read()
        return page, 404

    # Response selector
    def type(self, code):
        code = str(code)
        if code == '404':
            return self.not_found()
        elif code == '403':
            return self.forbidden()
        elif code == '400':
            return self.bad_request()
