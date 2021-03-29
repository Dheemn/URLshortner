from flask import Flask, redirect
from markupsafe import escape

import os
import codecs

from lib.database import DatabaseManager
from lib.path import PathManager


def create_app():
    db = DatabaseManager(<Database_name>, <Database_user>, <Database_user_password>)
    pathM = PathManager(db)
    app = Flask(__name__)
    app.config['secret_key'] = b"\xc0\xf7';\x9a\xd3\xa09G\x8c\x10eXi\xe4\x83" #Just for dev purposes
    print(app.config['secret_key'])
    

    @app.route('/')
    def home():
        return "<h1>Home</h1>", 200

    @app.route('/<string:path>')
    def path_en(path):
        #bResponse = Blacklist().hole(path)
        #if bResponse:
        #    return bResponse
        rdirect = pathM.fetch(path)
        return rdirect

    @app.route('/new/<string:link>')
    def new_link(link):
        return pathM.pathAdd(link)

    return app


if __name__ == "__main__":
    #db = DatabaseManager('urlshortner', 'urlshortner', 'testuser')
    #pathM = PathManager(db)
    app = create_app()
    app.run()