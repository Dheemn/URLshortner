from flask import Flask,  request

from lib.database import DatabaseManager
from lib.path import PathManager
from lib.configparse import ConfigParse


config_parse = ConfigParse('config.ini')
db_detail = config_parse.readDB()
common = config_parse.readCommon()


def create_app():
    db_object = DatabaseManager.getDatabase(db_detail)
    path_manager = PathManager(db_object)
    app = Flask(__name__)

    @app.route('/')
    def home():
        index_page = open(
                        'static/index.html',
                        'r',
                        encoding='utf-8')
        return index_page.read(), 200

    @app.route('/<string:path>')
    def path_en(path):
        rdirect = path_manager.fetch(path)
        return rdirect

    @app.route('/new/', methods=['POST'])
    def new_link():
        link = request.form['url']
        return path_manager.pathAdd(link)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host=common['serverHost'])
