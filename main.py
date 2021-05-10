from flask import Flask, redirect
from markupsafe import escape

import os

from lib.database import DatabaseManager
from lib.path import PathManager
from lib.configparse import ConfigParse

confParse = ConfigParse('postconfig.ini')
dbDetail = confParse.readDB()

def create_app():
    db = DatabaseManager(dbDetail)
    pathM = PathManager(db)
    app = Flask(__name__)
        

    @app.route('/')
    def home():
        return "<h1>Home</h1>", 200

    @app.route('/<string:path>')
    def path_en(path):
        rdirect = pathM.fetch(path)
        return rdirect

    @app.route('/new/<string:link>')
    def new_link(link):
        return pathM.pathAdd(link)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run()
