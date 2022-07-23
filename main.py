from flask import Flask,  request

from lib.database import DatabaseManager
from lib.path import PathManager
from lib.configparse import ConfigParse


confParse = ConfigParse('config.ini')
dbDetail = confParse.readDB()
common = confParse.readCommon()


def create_app():
    db = DatabaseManager.getDatabase(dbDetail)
    pathM = PathManager(db)
    app = Flask(__name__)

    @app.route('/')
    def home():
        index_page = open('static/index.html', 'r')
        return index_page.read(), 200

    @app.route('/<string:path>')
    def path_en(path):
        rdirect = pathM.fetch(path)
        return rdirect

    @app.route('/new/', methods=['POST'])
    def new_link():
        link = request.form['url']
        return pathM.pathAdd(link)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host=common['serverHost'])
